import requests
import json

def fetch_current_weather(latitude, longitude):
    with open("./keys/keys.json") as f:
        api_key = json.load(f)["weather-api"]["key"]

    response = requests.get(
        "https://api.weatherapi.com/v1/current.json",
        params={
            "key": api_key,
            "q": f"{latitude},{longitude}"
        },
        timeout=15
    )

    response.raise_for_status()
    return response.json()


def normalize_weather(weather_data):
    current = weather_data["current"]

    return {
        "condition": current["condition"]["text"],
        "temperature_c": current["temp_c"],
        "cloud_cover": current["cloud"],
        "precipitation_mm": current["precip_mm"],
        "visibility_km": current["vis_km"],
        "humidity": current["humidity"],
        "wind_kph": current["wind_kph"],
        "observed_at": current["last_updated"]
    }
