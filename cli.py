import argparse
import sys
import os
import logging
from datetime import datetime

# Add scripts directory to path to import our modules
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts'))

from gee_utils import initialize_gee, get_sentinel_image, get_landsat_image, get_download_url, download_image
from db_utils import get_car_geometry_db

# Configure logging for the CLI
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Geo-Download CLI: Baixe cenas Landsat e Sentinel para áreas do CAR.')
    
    # Required arguments
    parser.add_argument('--car', type=str, required=True, help='Código(s) do CAR separados por vírgula')
    
    # Selection arguments
    parser.add_argument('--sat', choices=['landsat', 'sentinel'], default='landsat', help='Satélite para download (padrão: landsat)')
    parser.add_argument('--years', type=str, required=True, help='Anos para download (ex: 2023 ou 2020-2024)')
    
    # Specific options
    parser.add_argument('--semester', type=int, choices=[1, 2], help='Para Landsat: 1º ou 2º semestre (se omitido, baixa ambos)')
    parser.add_argument('--months', type=str, help='Para Sentinel: meses específicos separados por vírgula (ex: 6,7,8)')
    
    # Output configuration
    from dotenv import load_dotenv
    load_dotenv()
    default_output = os.getenv('OUTPUT_DIR', 'downloads')
    
    parser.add_argument('--scale', type=int, help='Escala em metros (Landsat padrão 30, Sentinel padrão 10)')
    parser.add_argument('--output', type=str, default=default_output, help=f'Diretório de saída (padrão: {default_output})')

    args = parser.parse_args()

    # Parse years
    years = []
    if '-' in args.years:
        start, end = map(int, args.years.split('-'))
        years = list(range(start, end + 1))
    else:
        years = [int(y) for y in args.years.split(',')]

    # Parse CARs
    cars = [c.strip() for c in args.car.split(',')]

    # Initialize GEE
    try:
        initialize_gee()
    except Exception as e:
        logger.error(f"Erro ao inicializar GEE: {e}")
        sys.exit(1)

    # Main orchestration
    for car in cars:
        logger.info(f"\n🌍 Processando CAR: {car}")
        try:
            region = get_car_geometry_db(car)
        except Exception as e:
            logger.error(f"  ❌ Erro ao buscar geometria: {e}")
            continue

        car_dir = os.path.join(args.output, car)
        os.makedirs(car_dir, exist_ok=True)

        for year in years:
            if args.sat == 'sentinel':
                # Default months for Sentinel if not provided
                months_to_process = [int(m) for m in args.months.split(',')] if args.months else [6] 
                # Note: In the original request, for Sentinel they wanted year/month.
                # Here we default to June if none provided, or a range.
                
                scale = args.scale if args.scale else 10
                
                for month in months_to_process:
                    logger.info(f"  📅 {year}-{month:02d} (Sentinel)")
                    img = get_sentinel_image(region, year, month, month)
                    if img:
                        url = get_download_url(img, region, scale=scale)
                        filename = f"Sentinel_{year}_{month:02d}.tif"
                        download_image(url, os.path.join(car_dir, filename))
            
            else: # Landsat
                semesters = [args.semester] if args.semester else [1, 2]
                scale = args.scale if args.scale else 30
                
                for sem in semesters:
                    logger.info(f"  📅 {year} S{sem} (Landsat)")
                    img, bands = get_landsat_image(region, year, sem)
                    if img:
                        url = get_download_url(img, region, scale=scale)
                        filename = f"Landsat_{year}_S{sem}.tif"
                        download_image(url, os.path.join(car_dir, filename))

    logger.info("\n✨ Processo concluído!")

if __name__ == "__main__":
    main()
