"""
weather estimates from NOAA 20CRv3, via OPeNDAP
https://psl.noaa.gov/data/20thC_Rean 
"""

import xarray as xr

BASE_URL = "https://psl.noaa.gov/thredds/dodsC/Datasets/20thC_ReanV3"

# open the dataset once (to reduce calls)
def open_air_temperature_dataset(timestamp, directory, filename):
    directory_suffix = "SI" if timestamp.year <= 1980 else "MO"
    url = f"{BASE_URL}/{directory}{directory_suffix}/{filename}.{timestamp.year}.nc"
    return xr.open_dataset(url)

def get_air_temperature(latitude, longitude, timestamp, directory, filename, dataset=None):
    if dataset is None:
        with open_air_temperature_dataset(timestamp, directory, filename) as dataset:
            longitude_min = float(dataset["lon"].min().item())
        
            # normalize longitude to match dataset range
            if longitude_min >= 0:
                longitude %= 360
            else:
                longitude = (longitude + 180) % 360 - 180

            temperature = dataset["air"].sel(
                time = timestamp,
                lat = latitude,
                lon = longitude,
                method = "nearest",
            )
        
    # (KELVIN − 273.15) × 9/5 + 32 = FARENHEIT
    return (float(temperature.item()) - 273.15) * 9 / 5 + 32
