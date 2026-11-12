from datetime import datetime
from noaa_historical_weather import (
    get_air_temperature,
    open_air_temperature_dataset,
)

time = datetime(1900, 1, 1)
directory = "2m"
filename = "air.2m"
with open_air_temperature_dataset(time, directory, filename) as dataset:
    temp_f = get_air_temperature(40.0, 74.0, time, directory, filename, dataset)

print(f"air temperature: {temp_f:.1f} F")