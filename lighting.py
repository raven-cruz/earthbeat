
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from astral import Observer
from astral.sun import elevation, azimuth
import matplotlib.pyplot as plt

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


def main():
    latitude = 40.7128
    longitude = -74.0060
    date = "2026-11-14"
    time = "18:30"
    timezone_name = "America/New_York"

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

    print(scene)
    visualize_light_colors(sun_color, sky_color)

main()
