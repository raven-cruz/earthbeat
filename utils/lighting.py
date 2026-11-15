import matplotlib.pyplot as plt
import json
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
from astral import Observer
from astral.sun import elevation, azimuth
from utils.weather import fetch_weather, normalize_weather

def calculate_brightness(sun_elevation):
    # DIRECT SUN: 0 at horizon, 1 at 60deg
    # TODO: calculate intensity based on smth real. these numbers are arbitrary 
    sun_intensity = max(0, min(1, sun_elevation / 60))

    # AMBIENT SKY: starts brightening at -6deg
    # source: "civil twilight" (https://en.wikipedia.org/wiki/Dawn)
    sky_brightness = max(0, min(1, (sun_elevation + 6) / 66))

    return sun_intensity, sky_brightness

def lerp_color(start, end, t):
    t = max(0, min(1, t))
    return tuple(
        start[i] + (end[i] - start[i]) * t
        for i in range(3)
    )

def calculate_light_colors(sun_elevation):
    # orange at horizon, warm white at 45deg+
    sun_color = lerp_color(
        (1.0, 0.67, 0.40),
        (1.0, 0.96, 0.90),
        sun_elevation / 45
    )

    # dark blue at -6, light blue at 45deg+
    sky_color = lerp_color(
        (0.25, 0.35, 0.50),
        (0.65, 0.80, 1.00),
        (sun_elevation + 6) / 51
    )

    return sun_color, sky_color

# temp 
def visualize_light_colors(sun_color, sky_color):
    fig, axes = plt.subplots(1, 2, figsize=(8, 3))

    axes[0].set_facecolor(sun_color)
    axes[0].set_title("sunlight")

    axes[1].set_facecolor(sky_color)
    axes[1].set_title("sky")

    for ax in axes:
        ax.set_xticks([])
        ax.set_yticks([])

    plt.tight_layout()
    plt.show()

def calculate_lighting():
    ### INPUT ###
    latitude = float(input("latitude: ") or 40.0)
    longitude = float(input("longitude: ") or -74.0)
    date = input("date (YYYY-MM-DD): ") or datetime.now().strftime("%Y-%m-%d")
    time = input("time (HH:MM): ") or "12:00"
    timezone_name = input("timezone (e.g., America/New_York): ") or "America/New_York"

    local_datetime = datetime.strptime(
        f"{date} {time}", "%Y-%m-%d %H:%M"
    ).replace(tzinfo=ZoneInfo(timezone_name))

    utc_datetime = local_datetime.astimezone(timezone.utc)

    observer = Observer(latitude=latitude, longitude=longitude)

    ### SUN ###
    # sun position and brightness
    sun_elevation = elevation(observer, utc_datetime)
    sun_azimuth = azimuth(observer, utc_datetime)

    sun_intensity, sky_brightness = calculate_brightness(sun_elevation)
    sun_color, sky_color = calculate_light_colors(sun_elevation)

    ### WEATHER ###
    record, source, weather_time = fetch_weather(latitude, longitude, local_datetime)
    weather = normalize_weather(record, source, weather_time)

    # affects lighting
    cloud = weather["cloud_cover"] / 100    # convert cloud cover from 0–100 to 0–1
    sun_intensity *= 1 - (0.85 * cloud)     # clouds block direct sunlight
    sky_brightness *= 1 - (0.35 * cloud)    # clouds dim the sky less than direct sunlight
    sky_color = lerp_color(sky_color, (0.6, 0.65, 0.7),cloud)   # shift sky color toward gray when cloudy
    shadow_angle = 2 + (12 * cloud)         # clouds produce softer shadows


    lighting = {
        "id": f"{date} {time}_{latitude},{longitude}",
        "sun_elevation": sun_elevation,
        "sun_azimuth": sun_azimuth,
        "sun_intensity": sun_intensity,
        "sky_brightness": sky_brightness,
        "sun_color": sun_color,
        "sky_color": sky_color,
        "weather": weather,
        "shadow_angle": shadow_angle
    }

    # save lighting stuff to json for blender renderer
    render_dir = Path("renders")
    render_dir.mkdir(exist_ok=True)

    with open(render_dir / "lighting.json", "w") as f:
        json.dump(lighting, f, indent=2)