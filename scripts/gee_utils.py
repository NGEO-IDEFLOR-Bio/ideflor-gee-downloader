import ee
import datetime
import os
import requests
import logging
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def initialize_gee():
    """Initializes Google Earth Engine using a service account credentials file."""
    load_dotenv()
    
    project_id = os.getenv('GEE_PROJECT_ID')
    credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_PATH')
    
    if credentials_path and os.path.exists(credentials_path):
        # Using explicit Service Account credentials
        try:
            credentials = ee.ServiceAccountCredentials(None, credentials_path)
            ee.Initialize(credentials, project=project_id)
            logger.info(f"GEE Initialized with Service Account for project: {project_id}")
        except Exception as e:
            logger.error(f"Failed to initialize GEE with Service Account: {e}")
            raise
    else:
        # Fallback to default credentials
        try:
            ee.Initialize(project=project_id)
            logger.info(f"GEE Initialized with default credentials for project: {project_id}")
        except Exception as e:
            logger.error(f"Failed to initialize GEE: {e}")
            raise

def get_sentinel_image(region, year, start_month, end_month):
    """Retrieves a median Sentinel-2 SR image for a given region and time range."""
    start_date = f"{year}-{start_month:02d}-01"
    # End date handling for median composite
    last_day = 28 # Simplified for all months
    end_date = f"{year}-{end_month:02d}-{last_day}"

    collection = (ee.ImageCollection("COPERNICUS/S2_SR")
                  .filterBounds(region)
                  .filterDate(start_date, end_date)
                  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
                  .select(['B4', 'B3', 'B2']))

    count = collection.size().getInfo()
    if count == 0:
        logger.warning(f"No Sentinel image found for {year}/{start_month}-{end_month} (<10% clouds)")
        return None

    logger.info(f"Found {count} Sentinel images for {year}/{start_month:02d}. Creating median composite...")
    return collection.median()

def get_landsat_image(region, year, semester):
    """Retrieves a median Landsat image for a given region and semester."""
    if semester == 1:
        start_date = f"{year}-01-01"
        end_date = f"{year}-06-30"
    else:
        start_date = f"{year}-07-01"
        end_date = f"{year}-12-30"

    if year <= 2011:
        collection_id = "LANDSAT/LT05/C02/T1_L2"
        band_options = ['SR_B5', 'SR_B4', 'SR_B3']
    elif year <= 2013:
        collection_id = "LANDSAT/LE07/C02/T1_L2"
        band_options = ['SR_B3', 'SR_B2', 'SR_B1']
    elif year <= 2021:
        collection_id = "LANDSAT/LC08/C02/T1_L2"
        band_options = ['SR_B6', 'SR_B5', 'SR_B4']
    else:
        collection_id = "LANDSAT/LC09/C02/T1_L2"
        band_options = ['SR_B4', 'SR_B3', 'SR_B2']

    collection = (ee.ImageCollection(collection_id)
                  .filterBounds(region)
                  .filterDate(start_date, end_date)
                  .filter(ee.Filter.lt('CLOUD_COVER', 10)))

    count = collection.size().getInfo()
    if count == 0:
        logger.warning(f"No Landsat image found for {year} S{semester}")
        return None, None

    logger.info(f"Found {count} Landsat images for {year} S{semester}. Creating median composite...")
    image = collection.median().select(band_options)
    return image, band_options

def get_download_url(image, region, scale=10, scale_factor=2):
    """Generates a GeoTIFF download URL for a clipped image."""
    bounds = region.bounds()
    coords = bounds.coordinates().get(0).getInfo()
    
    xs = [pt[0] for pt in coords]
    ys = [pt[1] for pt in coords]
    xmid = (min(xs) + max(xs)) / 2
    ymid = (min(ys) + max(ys)) / 2
    xrange = (max(xs) - min(xs)) * scale_factor / 2
    yrange = (max(ys) - min(ys)) * scale_factor / 2
    
    expanded_bounds = ee.Geometry.Rectangle([xmid - xrange, ymid - yrange,
                                             xmid + xrange, ymid + yrange])

    url = image.clip(expanded_bounds).getDownloadURL({
        'scale': scale,
        'region': expanded_bounds,
        'format': 'GeoTIFF'
    })
    return url

def download_image(url, output_path):
    """Downloads an image from a GEE URL to a local path."""
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        response = requests.get(url, stream=True, timeout=60)
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            logger.info(f"✅ Download complete: {output_path}")
            return True
        else:
            logger.error(f"❌ Failed to download {output_path}: HTTP {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Error downloading {output_path}: {e}")
        return False
