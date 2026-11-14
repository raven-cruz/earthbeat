## Atmosphere Visualizer
>Goal: Use real weather and geological data to create a generative visualizer.

- MVP: a cool orb representing the planet at a given time
- best: a tool that can be used to get accurate conditions for a given date, past or future (weather and lighting especially)

**Current state**: extracts historical temperatures using [NOAA's 20th Centural Reanalysis Project](https://psl.noaa.gov/data/20thC_Rean)
- Known bug: NOAA hates requests I guess? Even after my caching workaround (see below, under `AI use disclosure > "Too Many Requests" fix`), I'm still running into errors (or loadtime is annoying long). My next big task is fixing this, which might mean abandoning NOAA. 