## Atmosphere Visualizer
>Goal: Use real weather and geological data to create a generative visualizer.

- MVP: a cool orb representing the planet at a given time
- best: a tool that can be used to get accurate conditions for a given date, past or future (weather and lighting especially)

**Current state**: extracts historical temperatures using [NOAA's 20th Centural Reanalysis Project](https://psl.noaa.gov/data/20thC_Rean)
- Known bug: NOAA hates requests I guess? Even after my caching workaround (see below, under `AI use disclosure > "Too Many Requests" fix`), I'm still running into errors (or loadtime is annoying long). My next big task is fixing this, which might mean abandoning NOAA. 

### How to use
> Instructions as of 11/12/26 (WIP)

Currently, the testing code only runs locally, with `Python 3.15.2`.

In `terminal` run these commands to install requirements and run the test code:

``` 
pip install -r requirements.txt
python test.py 
```

Make sure to follow input formatting exactly. Date range is currently 1805-2015.

### AI use disclosure
#### "Too Many Requests" fix
> GitHub Copilot, GPT-6 Luna

I was running into an issue with NOAA rate limiting that I couldn't handle in a timely fashion, so I recruited GitHub Copilot and GPT-6 Luna to help me implement caching to temporarily store NetCDF datasets. 

In implementing my caching workaround, it also implemented [exponential backoff with jitter](https://en.wikipedia.org/wiki/Exponential_backoff) -- which, I admit, I hadn't thought of on my own. As a result, I'm seeing significantly less 429 errors (and I've learned about exponential backoff). Hooray!