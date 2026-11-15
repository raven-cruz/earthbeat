
import json
import requests
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

with open("./keys/keys.json") as f:
    api_key = json.load(f)["weather-api"]["key"]

city = input("enter city: ")

response = requests.get(
    "https://api.weatherapi.com/v1/current.json",
    params={"key": api_key, "q": f"{city}"},
    timeout=15
)
response.raise_for_status()

data = response.json()
print(json.dumps(data, indent=2))

# TEMP VISUALIZER
def visualize_temp(temp):
    cmap = plt.get_cmap("RdYlBu_r")

    color = cmap(max(-40, min(temp, 140)) / 140)

    fig, ax = plt.subplots()
    ax.set_facecolor(color)
    ax.text(0.5, 0.5, f"{temp} F",
        ha="center", 
        va="center", 
        fontsize=32, 
    )
    ax.set_xticks([])
    ax.set_yticks([])
    plt.show()

visualize_temp(data["current"]["temp_f"])
