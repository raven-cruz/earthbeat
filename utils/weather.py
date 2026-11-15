import requests
import json
from datetime import datetime

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

def fetch_weather(latitude, longitude, local_datetime):
    with open("./keys/keys.json") as f:
        api_key = json.load(f)["weather-api"]["key"]

    now = datetime.now(local_datetime.tzinfo)
    days_away = (local_datetime.date() - now.date()).days
    minutes_away = abs(local_datetime.timestamp() - now.timestamp()) / 60

    if minutes_away <= 15:
        endpoint = "current"
    elif days_away == -1:
        endpoint = "history"
    elif 0 <= days_away <= 2:
        endpoint = "forecast"
    else:
        raise ValueError("date is outside the supported range")

    params = {
        "key": api_key,
        "q": f"{latitude},{longitude}"
    }

    if endpoint != "current":
        params["dt"] = local_datetime.date().isoformat()

    if endpoint == "forecast":
        params["days"] = 3

    response = requests.get(
        f"https://api.weatherapi.com/v1/{endpoint}.json",
        params=params,
        timeout=15
    )

    if not response.ok:
        try:
            message = response.json()["error"]["message"]
        except (ValueError, KeyError, TypeError):
            message = response.reason
        raise RuntimeError(f"WeatherAPI error: {message}")

    data = response.json()

    if endpoint == "current":
        record = data["current"]
        return record, endpoint, record["last_updated"]

    # select record nearest to requested time
    hours = data["forecast"]["forecastday"][0]["hour"]
    target = local_datetime.timestamp()

    record = min(hours, key=lambda hour: abs(hour["time_epoch"] - target))

    return record, endpoint, record["time"]



def normalize_weather(record, source, weather_time):
    return {
        "condition": record["condition"]["text"],
        "temperature_c": record["temp_c"],
        "cloud_cover": record["cloud"],
        "precipitation_mm": record["precip_mm"],
        "visibility_km": record["vis_km"],
        "humidity": record["humidity"],
        "wind_kph": record["wind_kph"],
        "source": source,
        "weather_time": weather_time
    }
