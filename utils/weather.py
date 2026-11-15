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
