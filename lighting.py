
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from astral import Observer
from astral.sun import elevation, azimuth

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

    sun_elevation = elevation(observer, utc_datetime)
    sun_azimuth = azimuth(observer, utc_datetime)

    scene = {
        "latitude": latitude,
        "longitude": longitude,
        "datetime": local_datetime,
        "datetime_utc": utc_datetime,
        "timezone": timezone_name,
        "sun_elevation": sun_elevation,
        "sun_azimuth": sun_azimuth
    }

    print(scene)

main()
