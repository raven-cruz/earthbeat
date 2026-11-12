from datetime import datetime
from noaa_historical_weather import get_air_temperature

time = datetime(1900, 1, 1)
directory = "2m"
filename = "air.2m"
temp_c = get_air_temperature(40.0, 74.0, time, directory, filename)

print(f"air temperature: {temp_c:.1f} C")