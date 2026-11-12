"""
Weather estimates from NOAA 20CRv3 via OPeNDAP.
https://psl.noaa.gov/data/20thC_Rean
"""

import atexit
import random
import threading
import time
from collections import OrderedDict
from functools import lru_cache

import xarray as xr

BASE_URL = "https://psl.noaa.gov/thredds/dodsC/Datasets/20thC_ReanV3"

MAX_OPEN_DATASETS = 4
MAX_RETRIES = 6

datasets = OrderedDict()        # reuse open remote datasets
noaa_lock = threading.RLock()   # serialize noaa requests

# reuse an open dataset for the same year + variable
def open_air_temperature_dataset(timestamp, directory, filename):
    key = (timestamp.year, directory, filename)

    with noaa_lock:
        if key in datasets:
            datasets.move_to_end(key)
            return datasets[key]

        suffix = "SI" if timestamp.year <= 1980 else "MO"
        url = f"{BASE_URL}/{directory}{suffix}/{filename}.{timestamp.year}.nc"
        print(url)

        dataset = xr.open_dataset(url, engine="netcdf4")
        datasets[key] = dataset

        # close the oldest dataset if the cache is full
        if len(datasets) > MAX_OPEN_DATASETS:
            _, old_dataset = datasets.popitem(last=False)
            old_dataset.close()

        return dataset


# handle http 429
# written by GPT 6 Luna
def is_rate_limited(error):
    current = error
    while current is not None:
        if getattr(current, "status_code", None) == 429: return True
        if getattr(current, "code", None) == 429: return True

        message = str(current).lower()
        if "429" in message or "too many requests" in message or "-77" in message:
            return True

        current = current.__cause__ or current.__context__

    return False

# retry rate-limited requests w/ exponential backoff
# written by GPT 6 Luna
def retry(operation):
    for attempt in range(MAX_RETRIES + 1):
        try:
            return operation()
        except Exception as error:
            if not is_rate_limited(error) or attempt == MAX_RETRIES:
                raise

            delay = 2 ** attempt + random.uniform(0, 1)

            # Honor a numeric Retry-After header when available.
            headers = getattr(error, "headers", None)
            if headers:
                retry_after = headers.get("Retry-After")
                if retry_after:
                    try:
                        delay = max(delay, float(retry_after))
                    except ValueError:
                        pass

            time.sleep(delay)

# cache temperature lookups in memory
# written by GPT 6 Luna
@lru_cache(maxsize=4096)
def _cached_temperature(latitude, longitude, timestamp, directory, filename):
    def fetch():
        # One remote operation at a time within this process.
        with noaa_lock:
            dataset = open_air_temperature_dataset(
                timestamp, directory, filename
            )
            return get_air_temp_from_dataset(
                dataset, latitude, longitude, timestamp
            )

    return retry(fetch)

# return temp in fahrenheit
def get_air_temperature(latitude, longitude, timestamp, directory, filename, dataset=None):
    longitude %= 360
    print(latitude, longitude)

    if dataset is None:
        return _cached_temperature(latitude, longitude, timestamp, directory, filename)

    return retry(
        lambda: get_air_temp_from_dataset(dataset, latitude, longitude, timestamp)
    )


def get_air_temp_from_dataset(dataset, latitude, longitude, timestamp):
    # normalize longitude to match dataset range
    longitude_min = float(dataset["lon"].min())
    if longitude_min >= 0:
        longitude %= 360
    else:
        longitude = (longitude + 180) % 360 - 180
    
    with noaa_lock:
        temperature = dataset["air"].sel(
            time = timestamp,
            lat = latitude,
            lon = longitude,
            method = "nearest",
        )

        # (KELVIN − 273.15) × 9/5 + 32 = FARENHEIT
        return (float(temperature.item()) - 273.15) * 9 / 5 + 32

# CLOSE CACHED DATASETS
# written by GPT 6 Luna
def close_cached_datasets():
    with noaa_lock:
        for dataset in datasets.values():
            dataset.close()
        datasets.clear()

    _cached_temperature.cache_clear()

atexit.register(close_cached_datasets)
