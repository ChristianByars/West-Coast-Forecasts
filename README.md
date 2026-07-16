# Heat-Waves — Sept 2022 California heat wave: AIFS v2 vs SFNO vs Aurora (vs ERA5)

Compares **three AI weather models** — ECMWF **AIFS v2**, NVIDIA/Makani **SFNO**, and Microsoft
**Aurora** — all run via NVIDIA **earth2studio**, initialized from the same **ERA5** state and
verified against ERA5 over the record-breaking **September 2022 California heat wave** (peak ~Sep 6).
Each forecast is global; it is analyzed at three scales — **global, CONUS, California**.

- **Models:** one ~12-day global deterministic run per model, all initialized **2022-08-30 00Z**
  (~7-day lead to the peak), driven through one `deterministic()` pipeline via a `MODELS` registry.
- **Comparison variable:** 2 m temperature (`t2m`) only — the one field every model emits.
- **Metric:** absolute daily-Tmax thresholds (100 °F / 104 °F, ≥ 3 consecutive days) + per-model
  model−ERA5 bias / RMSE / MAE.
- **Reference result:** AIFS v2 California peak-day (Sep 6) bias **−0.12 °C**, RMSE **1.32 °C** — it
  captured the heat dome a week ahead; SFNO and Aurora are compared against the same truth.

**Two visualization modes:** a *comparison grid* (peak-day maps, every model + ERA5 + differences,
per region) and *per-model deep dives* (grouped city time series + error growth for one model at a
time), plus a cross-model RMSE/bias skill overlay.

## Files

| File | Purpose |
|------|---------|
| `HeatWaves.ipynb` | The deliverable notebook (run top-to-bottom). |
| `aifs2_era5.py` | Patches earth2studio's CDS lexicon so AIFS v2's 16 extra inputs resolve from ERA5 (10 hPa level + snow depth real; 11 ocean-wave inputs zero-filled — immaterial to a land heat-wave forecast). Imported by the notebook; **AIFS v2 only** (SFNO/Aurora need no patch). |
| `pyproject.toml` / `uv.lock` | Dedicated venv: earth2studio (git `main`, for AIFS2/SFNO/Aurora) + `[aifs2]`, torch 2.6.0+cu124, cached flash-attn. |
| `data/` | Per-model forecast Zarr (`aifs_*`, `sfno_*`, `aurora_*`) + ERA5 verification (regenerated on first run; AIFS v2's is reused). |
| `figures/` | Output maps and plots. |

## Run

```bash
cd /home/jovyan/West-Coast
uv sync                      # one-time: build the venv
# open HeatWaves.ipynb with the "Heat-Waves (AIFS2)" kernel, or:
uv run jupyter nbconvert --to notebook --execute --inplace \
    --ExecutePreprocessor.kernel_name=heat-waves HeatWaves.ipynb
```

The first run downloads each model's checkpoint and full ERA5 initial state from the Copernicus CDS
(needs `~/.cdsapirc`); both are cached, so re-runs are fast. AIFS v2's forecast is already cached and
is reused as-is; the **first SFNO and Aurora runs** download weights and run a global 12-day forecast
(Aurora is the heavy one).

## Notes / caveats

- All models are **global**; "regional" = cropping the one global run to CONUS / California.
- Adding a model is one row in the `MODELS` registry (cell 1): the class, a `patch` flag (AIFS v2
  only), a `regrid` flag, and a Zarr filename `prefix`. To bound GPU memory, `run_forecast(key, init)`
  loads each model on a cache miss and frees it before the next.
- **Aurora** runs on a 720×1440 grid (no south pole); its output is interpolated onto the ERA5
  721×1440 latitude grid before differencing (1-D lat interp, pole extrapolated — immaterial here).
- Daily Tmax is derived from 6-hourly samples for **every** model and ERA5 (matched sampling), so the
  comparison is fair; it slightly underestimates the true afternoon peak equally for all.
- Ocean-wave inputs are zero-filled at initialization for AIFS v2 (see `aifs2_era5.py`); negligible
  for a California land 2 m-temperature forecast.
- To extend into a lead-time sweep, `run_forecast(key, init_time)` is a function — loop it over
  earlier inits per model.
