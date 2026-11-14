
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from astral import Observer
from astral.sun import elevation, azimuth

def calculate_brightness(sun_elevation):
    # DIRECT SUN: 0 at horizon, 1 at 60deg
    # TODO: calculate intensity based on smth real. these numbers are arbitrary 
    sun_intensity = max(0, min(1, sun_elevation / 60))

    # AMBIENT SKY: starts brightening at -6deg
    # source: "civil twilight" (https://en.wikipedia.org/wiki/Dawn)
    sky_brightness = max(0, min(1, (sun_elevation + 6) / 66))

    return sun_intensity, sky_brightness

def main():
    latitude = 40.7128
    longitude = -74.0060
    date = "2026-11-14"
    time = "12:30"
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

    scene = {
        "latitude": latitude,
        "longitude": longitude,
        "datetime": local_datetime,
        "datetime_utc": utc_datetime,
        "timezone": timezone_name,
        "sun_elevation": sun_elevation,
        "sun_azimuth": sun_azimuth,
        "sun_intensity": sun_intensity,
        "sky_brightness": sky_brightness
    }

    print(scene)

main()
