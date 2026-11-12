from datetime import datetime
from noaa_historical_weather import (
    get_air_temperature,
    open_air_temperature_dataset,
)
# from pick import pick

def test_noaa_with_inputs():
    directory = "2m"
    filename = "air.2m"

    lat = input("latitude: ")
    lon = input("longitude: ")
    date = input("date (YYYY-MM-DD): ")
    time = input("time (HH:MM): ")

    timestamp = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    with open_air_temperature_dataset(timestamp, directory, filename) as dataset:
        temp_f = get_air_temperature(
            float(lat), float(lon), timestamp, directory, filename, dataset
        )

    print(f"air temperature on {date} at {time}: {temp_f:.1f} F")

def test_noaa_no_inputs():
    directory = "2m"
    filename = "air.2m"

    lat = 40
    lon = 74
    date = "1900-01-01"
    time = "00:00"

    timestamp = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    with open_air_temperature_dataset(timestamp, directory, filename) as dataset:
        temp_f = get_air_temperature(
            float(lat), float(lon), timestamp, directory, filename, dataset
        )

    print(f"air temperature on {date} at {time}: {temp_f:.1f} F")

test_noaa_no_inputs()