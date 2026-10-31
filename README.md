# West Coast Weather Forecasts — AI Weather Models vs ERA5

Two notebooks comparing AI weather forecast models against ERA5 reanalysis on real West Coast
extreme weather events.

## Notebooks

### `HeatWaves.ipynb` — September 2022 California Heat Wave

Compares three AI weather models AIFSv2, SFNO, and Aurora on the
record breaking heat wave that hit Sacramento and the rest of California in September 2022. Each
model is analyzed at global, continental US, and California scales, with peak-day comparison maps,
per-model deep dives, and a cross-model skill overlay.

### `Flooding.ipynb` — Dec 2022 – Jan 2023 West Coast Flood

Forecasts the New Year atmospheric river that flooded the Sacramento area on Dec 31 2022 – Jan 1 2023,
using AIFS v2 initialized at three different lead times (3, 7, and 10 days) to see how far ahead the
model could see the event coming.

## Files

| File | Purpose |
|------|---------|
| `HeatWaves.ipynb` | Heat wave analysis notebook. |
| `Flooding.ipynb` | Flood lead-time sweep notebook. |
| `data/` | Cached forecast and reanalysis data (not tracked in git). |
| `figures/` | Output maps and plots (not tracked in git). |
