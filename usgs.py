import requests
import pandas as pd
import matplotlib.pyplot as plt

# earthquakes from the past 24 hours
url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"

response = requests.get(url, timeout=15)
response.raise_for_status()
data = response.json()

earthquakes = []
for quake in data["features"]:
    props = quake["properties"]
    lon, lat, depth = quake["geometry"]["coordinates"]

    earthquakes.append({
        "location": props["place"],
        "magnitude": props["mag"],
        "latitude": lat,
        "longitude": lon,
        "depth_km": depth,
        "time": pd.to_datetime(props["time"], unit="ms", utc=True)
    })

df = pd.DataFrame(earthquakes)
print(df.head(10))

# TEMP VISUALIZER
plt.figure()
plt.scatter(
    df["longitude"],
    df["latitude"],
    s=df["magnitude"] ** 2,
    c=df["depth_km"],
    cmap="rainbow_r",
)

plt.colorbar(label="depth (km)")
plt.xlabel("longitude")
plt.ylabel("latitude")
plt.title("earthquakes in the past 24 hours")
plt.show()
