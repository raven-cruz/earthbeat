import subprocess
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from astral import Observer
from astral.sun import elevation, azimuth
import json
from pathlib import Path
from utils.lighting import calculate_brightness, calculate_light_colors
from utils.weather import fetch_current_weather

BLENDER_PATH = "/Applications/Blender.app/Contents/MacOS/Blender"


def calculate_lighting():
    latitude = float(input("latitude: "))
    longitude = float(input("longitude: "))
    date = input("date (YYYY-MM-DD): ")
    time = input("time (HH:MM): ")
    timezone_name = input("timezone (e.g., America/New_York): ")

    local_datetime = datetime.strptime(
        f"{date} {time}", "%Y-%m-%d %H:%M"
    ).replace(tzinfo=ZoneInfo(timezone_name))

    utc_datetime = local_datetime.astimezone(timezone.utc)

    observer = Observer(latitude=latitude, longitude=longitude)

    # sun position and brightness
    sun_elevation = elevation(observer, utc_datetime)
    sun_azimuth = azimuth(observer, utc_datetime)

    sun_intensity, sky_brightness = calculate_brightness(sun_elevation)
    sun_color, sky_color = calculate_light_colors(sun_elevation)

    scene = {
        "latitude": latitude,
        "longitude": longitude,
        "datetime": local_datetime,
        "datetime_utc": utc_datetime,
        "timezone": timezone_name,
        "sun_elevation": sun_elevation,
        "sun_azimuth": sun_azimuth,
        "sun_intensity": sun_intensity,
        "sky_brightness": sky_brightness,
        "sun_color": sun_color,
        "sky_color": sky_color
    }

    lighting = {
        "id": f"{date} {time}_{latitude},{longitude}",
        "sun_elevation": sun_elevation,
        "sun_azimuth": sun_azimuth,
        "sun_intensity": sun_intensity,
        "sky_brightness": sky_brightness,
        "sun_color": sun_color,
        "sky_color": sky_color
    }

    weather_data = fetch_current_weather(latitude, longitude)
    weather = weather_data["current"]

    print("Weather:", weather["condition"]["text"])
    print("Temperature:", weather["temp_c"], "°C")
    print("Cloud cover:", weather["cloud"], "%")
    print("Precipitation:", weather["precip_mm"], "mm")
    print("Visibility:", weather["vis_km"], "km")

    # save lighting stuff to json for blender renderer
    render_dir = Path("renders")
    render_dir.mkdir(exist_ok=True)

    with open(render_dir / "lighting.json", "w") as f:
        json.dump(lighting, f, indent=2)

def main():
    calculate_lighting()

    # run scene render
    subprocess.run([BLENDER_PATH, "--background", "--python", "utils/render.py"], check=True)

if __name__ == "__main__":
    main()