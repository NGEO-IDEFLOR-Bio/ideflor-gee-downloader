import sys
import os

# Add scripts directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from gee_utils import initialize_gee, get_sentinel_image, get_landsat_image, get_download_url
from db_utils import get_car_geometry_db

def test_sentinel_download():
    print("\n--- Testing Sentinel Download ---")
    car_code = "PA-1504802-FCEA8FAD347340D8BD6D3143A9623468"
    region = get_car_geometry_db(car_code)
    
    # Example: 2024, June to August
    year = 2024
    start_month = 6
    end_month = 8
    
    img = get_sentinel_image(region, year, start_month, end_month)
    if img:
        url = get_download_url(img, region, scale=10)
        print(f"Sentinel URL: {url}")
    else:
        print("Failed to get Sentinel image.")

def test_landsat_download():
    print("\n--- Testing Landsat Download ---")
    car_code = "PA-1504802-FCEA8FAD347340D8BD6D3143A9623468"
    region = get_car_geometry_db(car_code)
    
    # Example: 2023, Semester 2
    year = 2023
    semester = 2
    
    img, bands = get_landsat_image(region, year, semester)
    if img:
        url = get_download_url(img, region, scale=30)
        print(f"Landsat URL: {url}")
    else:
        print("Failed to get Landsat image.")

if __name__ == "__main__":
    try:
        initialize_gee()
        test_sentinel_download()
        test_landsat_download()
    except Exception as e:
        print(f"An error occurred: {e}")
