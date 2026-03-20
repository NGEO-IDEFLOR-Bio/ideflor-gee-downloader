import ee
import os
from dotenv import load_dotenv

def get_car_geometry_mock(car_code):
    """
    Returns a mock ee.Geometry for the specific test CAR.
    In a real scenario, this would query the PostGIS database.
    """
    # Specific test CAR provided by the user
    test_car = "PA-1504802-FCEA8FAD347340D8BD6D3143A9623468"
    
    if car_code == test_car:
        # Coordinates extracted from the user's WKT
        coords = [
            [-54.0292538888889, -1.70762083333333], [-54.0299021548834, -1.70194216654557], 
            [-54.0275752777778, -1.70235416666667], [-54.0275972222222, -1.69943916666667], 
            [-54.0275925, -1.69583083333333], [-54.0276033333333, -1.69221194444444], 
            [-54.0257080555556, -1.69208944444444], [-54.0255525, -1.69207416666667], 
            [-54.0231763888889, -1.69190111111111], [-54.0194411111111, -1.69179805555556], 
            [-54.0090066666667, -1.69362472222222], [-54.0098836111111, -1.69616861111111], 
            [-54.0106744444444, -1.69956305555556], [-54.0114675, -1.70224833333333], 
            [-54.0127169444444, -1.70497916666667], [-54.0042388888889, -1.70369222222222], 
            [-54.0042344444444, -1.70659777777778], [-54.0140338888889, -1.70784527777778], 
            [-54.0207391666667, -1.70373555555556], [-54.0208844444444, -1.70345444444444], 
            [-54.0221402777778, -1.70134972222222], [-54.0292538888889, -1.70762083333333]
        ]
        return ee.Geometry.Polygon([coords])
    else:
        raise ValueError(f"CAR code {car_code} not found in mock data.")

def wkt_to_ee_geometry(wkt):
    """
    Parses a WKT string into an ee.Geometry object.
    Attempts to use QGIS API first, then falls back to shapely (useful for CLI/Server).
    """
    import ee
    import json
    
    # Method 1: QGIS (Main way for the plugin)
    try:
        from qgis.core import QgsGeometry
        geom = QgsGeometry.fromWkt(wkt)
        if not geom.isNull():
            return ee.Geometry(json.loads(geom.asJson()))
    except (ImportError, Exception):
        pass

    # Method 2: Shapely (Fallback for CLI/Server)
    try:
        import shapely.wkt
        from shapely.geometry import mapping
        shapely_geom = shapely.wkt.loads(wkt)
        return ee.Geometry(mapping(shapely_geom))
    except (ImportError, Exception) as e:
        raise ValueError(f"Não foi possível converter WKT para GEE: {e}. "
                         "No QGIS isso deve funcionar nativamente. Em servidores, instale 'shapely'.")

def get_car_geometry_db(car_code):
    """
    Connects to the database and retrieves geometry (as WKT and ee.Geometry) for the given CAR.
    """
    import psycopg2
    
    # Ensure .env is loaded
    script_dir = os.path.dirname(os.path.abspath(__file__))
    plugin_dir = os.path.dirname(script_dir)
    env_path = os.path.join(plugin_dir, '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
    else:
        load_dotenv()

    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_DATABASE'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT', '5432')
        )
        cur = conn.cursor()
        query = "SELECT ST_AsText(geom) FROM ngeo.tb_sicar WHERE codigo_car = %s"
        cur.execute(query, (car_code,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        
        if row:
            wkt = row[0]
            # Use the new helper to convert WKT to GEE
            ee_geom = wkt_to_ee_geometry(wkt)
            return ee_geom, wkt
        else:
            # Fallback to mock for testing if explicitly PA test car
            if car_code == "PA-1504802-FCEA8FAD347340D8BD6D3143A9623468":
                mock_geom = get_car_geometry_mock(car_code)
                return mock_geom, None
            raise ValueError(f"Código CAR {car_code} não encontrado no banco de dados.")
            
    except Exception as e:
        # If DB fails, fallback to mock if it's the test car
        if car_code == "PA-1504802-FCEA8FAD347340D8BD6D3143A9623468":
            return get_car_geometry_mock(car_code), None
        raise e
