import subprocess
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from astral import Observer
from astral.sun import elevation, azimuth
import json
from pathlib import Path
from utils.lighting import calculate_brightness, calculate_light_colors
from utils.weather import fetch_current_weather, normalize_weather

BLENDER_PATH = "/Applications/Blender.app/Contents/MacOS/Blender"


def calculate_lighting():
    latitude = float(input("latitude: ") or 40.0)
    longitude = float(input("longitude: ") or -74.0)
    date = input("date (YYYY-MM-DD): ") or datetime.now().strftime("%Y-%m-%d")
    time = input("time (HH:MM): ") or datetime.now().strftime("%H:%M")
    timezone_name = input("timezone (e.g., America/New_York): ") or "America/New_York"

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

    weather_data = fetch_current_weather(latitude, longitude)
    weather = normalize_weather(weather_data)

    lighting = {
        "id": f"{date} {time}_{latitude},{longitude}",
        "sun_elevation": sun_elevation,
        "sun_azimuth": sun_azimuth,
        "sun_intensity": sun_intensity,
        "sky_brightness": sky_brightness,
        "sun_color": sun_color,
        "sky_color": sky_color,
        "weather": weather
    }

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