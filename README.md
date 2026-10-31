# West Coast Weather Forecasts — AI Models vs ERA5

![Peak-day maximum temperature over California: SFNO and Aurora against ERA5](docs/images/maps_peakday_california.png)

Two notebooks compare AI weather models with ERA5 on West Coast extremes, using [NVIDIA Earth2Studio](https://github.com/NVIDIA/earth2studio): `HeatWaves.ipynb` runs NVIDIA's SFNO and Microsoft's Aurora on the September 2022 California heat wave (peak around 6 September), and `Flooding.ipynb` runs ECMWF's AIFS v2, initialized 3, 7 and 10 days before the New Year 2022–23 atmospheric river. AIFS v2 is used only in the flood notebook.

## Results at a glance

Bias is always model − ERA5. The heat-wave table scores daily maximum 2 m temperature in °C at global, CONUS and California scales, on the peak day and averaged over the event window (31 August – 9 September 2022). The flood table scores event-total precipitation (Dec 31 – Jan 1) over the West Coast box in mm for each lead time. ERA5 is the reference for both, but ERA5 precipitation is itself model-derived (reanalysis output, not gauge or radar data), so these numbers measure agreement with ERA5, not with observed rainfall.

**Heat wave: daily maximum 2 m temperature against ERA5, by region and model**

<!-- HeatWaves_metrics:START -->
_Filled in after the verified run._
<!-- HeatWaves_metrics:END -->

**Flood: AIFS v2 event-total precipitation against ERA5, by lead time**

<!-- Flooding_metrics:START -->
_Filled in after the verified run._
<!-- Flooding_metrics:END -->

![Daily-maximum temperature RMSE and bias over California for SFNO and Aurora against ERA5, by forecast day](docs/images/skill_comparison_california.png)

*Heat wave: how the error of each model against ERA5 grows with forecast day over California; the dotted line marks the peak.*

![Heat-wave day counts over California for SFNO, Aurora and ERA5 at the 100 °F and 104 °F thresholds](docs/images/heatwave_daycount_california.png)

*Heat wave: days that belong to a run of three or more consecutive days above each threshold, model against ERA5.*

![AIFS v2 and ERA5 event-total precipitation over the West Coast for 3, 7 and 10 days of lead time, with the difference](docs/images/precip_eventtotal_leadsweep.png)

*Flood: event-total precipitation (Dec 31 – Jan 1) from AIFS v2 at each lead time next to ERA5, with AIFS v2 − ERA5 in the last column.*

![Event-total precipitation at five flood locations: ERA5 and AIFS v2 at 3, 7 and 10 days of lead time](docs/images/precip_eventtotal_by_location.png)

*Flood: event totals at the exact grid cell of five flood-affected locations, ERA5 against AIFS v2 at each lead time.*

## Models and data

| Model | Developer | Notebook | Initial condition |
|---|---|---|---|
| SFNO | NVIDIA | `HeatWaves.ipynb` | ERA5 (Copernicus CDS), 2022-08-30 00Z, 12-day forecast |
| Aurora | Microsoft | `HeatWaves.ipynb` | ERA5 (Copernicus CDS), 2022-08-30 00Z, 12-day forecast |
| AIFS v2 | ECMWF | `Flooding.ipynb` | ERA5 (Copernicus CDS) at 2022-12-21, 2022-12-24 and 2022-12-28 00Z; the 11 ocean-wave inputs are zero-filled |
| ERA5 | ECMWF reanalysis | both | reference: daily maximum 2 m temperature (from 6-hourly samples) and total precipitation (hourly accumulations) |

## Quick start

Requires Python 3.12, [uv](https://docs.astral.sh/uv/), and an NVIDIA GPU with about 48 GB of VRAM (developed and tested on an L40).

```bash
git clone https://github.com/ChristianByars/West-Coast-Forecasts.git
cd West-Coast-Forecasts
uv sync
uv run python -m ipykernel install --user --name west-coast --display-name "west-coast"
```

`uv sync` expects two prebuilt wheels (flash-attn and torch-harmonics) in a `wheels/` folder; see [docs/environment.md](docs/environment.md).

Open a notebook in JupyterLab and select the **west-coast** kernel, then run all cells.

## Notebooks

<!-- RUNS:START -->
_Runtime and GPU memory are filled in after the verified run._
<!-- RUNS:END -->

| Notebook | Event | Models | Verified against |
|---|---|---|---|
| `HeatWaves.ipynb` | September 2022 California heat wave | SFNO, Aurora | ERA5 daily maximum 2 m temperature at global, CONUS and California scales |
| `Flooding.ipynb` | New Year 2022–23 atmospheric-river flood | AIFS v2 at 3, 7 and 10 days of lead | ERA5 daily and event-total precipitation over the West Coast |

## Repository layout

```text
HeatWaves.ipynb       SFNO vs Aurora: September 2022 California heat wave
Flooding.ipynb        AIFS v2 lead-time sweep: New Year 2022-23 atmospheric river
aifs2_era5.py         lets earth2studio initialize AIFS v2 from ERA5 (CDS lexicon patch)
metrics.py            area-weighted skill metrics
tests/                unit tests for metrics.py
docs/images/          figures shown in this README
docs/results/         CSV metric tables written by the notebooks
docs/environment.md   pinned versions and install notes
data/                 generated forecasts and ERA5 downloads (gitignored)
figures/              generated figures (gitignored)
```

## Environment notes

Pinned versions, install caveats, and fixes are in [docs/environment.md](docs/environment.md).

## References

- [NVIDIA Earth2Studio](https://github.com/NVIDIA/earth2studio) and its [documentation](https://nvidia.github.io/earth2studio/)
- [ERA5 hourly data on single levels](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels) (Copernicus Climate Data Store)
- [AIFS Single v2 model card](https://huggingface.co/ecmwf/aifs-single-2.0) (ECMWF)
- [uv](https://docs.astral.sh/uv/)
