## Atmosphere Visualizer (WIP)
>Goal: Use real weather and geological data to create a generative visualizer.

- MVP: a cool orb representing the planet at a given time
- best: a tool that can be used to get accurate conditions for a given date, past or future (weather and lighting especially)

**Current state:** Takes a date, time, and location to calculate sun position, intensity, and color, then uses those values to generate a basic lighting preview in Blender. Currently supports sunlight and ambient sky lighting; weather and moonlight integration are planned.

### Setup

Install requirements:

```
pip install -r requirements.txt
```

`tool.py` expects Blender at `/Applications/Blender.app/Contents/MacOS/Blender`. Update `BLENDER_PATH` in that file if Blender is installed elsewhere.

>This is a temp visualizer. I'll replace this logic ASAP

### Run

```
python tool.py
```

Enter latitude, signed longitude (west is negative), date (`YYYY-MM-DD`), time (`HH:MM`, 24-hour), and a timezone such as `America/New_York`.

The tool writes lighting data to `renders/lighting.json` and a Blender preview image to `renders`.
