"""Initialize ECMWF AIFS v2 from ERA5 (CDS) for historical cases.

AIFS v2 requires 92 input variables. earth2studio's CDS lexicon covers 76 of them;
the remaining 16 are:

  * 10 hPa pressure level : t10, u10, v10, z10   -> real ERA5 (pressure-levels @ 10 hPa)
  * snow depth            : sd                   -> real ERA5 (single-levels)
  * 11 ocean-wave inputs  : swh, mwp, cdww, cos_mwd, sin_mwd, h1012/h1214/h1417/
                            h1721/h2125/h2530    -> ZERO-FILLED

Why zero-fill the wave inputs?  ERA5 delivers ocean-wave fields on a coarser 0.5 deg
wave grid (361x720), not the 0.25 deg atmospheric grid (721x1440), and several of the
AIFS v2 spectral-band heights (h1012..h2530) are not in the ERA5 catalogue at all.
For a multi-day *land* 2 m-temperature forecast over California, ocean-wave initial
conditions are immaterial, so we set all 11 wave channels to zero (piggybacked on the
already-fetched 2m_temperature request so no extra CDS download and a guaranteed
721x1440, NaN-free field).  This is the one documented approximation in the init.

Usage:
    from aifs2_era5 import patch_cds_lexicon_for_aifs2, ZERO_FILL_WAVE_VARS
    patch_cds_lexicon_for_aifs2()      # call once, before building the CDS data source
"""
from __future__ import annotations

import numpy as np

SL = "reanalysis-era5-single-levels"
PL = "reanalysis-era5-pressure-levels"

# Ocean-wave inputs with no usable same-grid ERA5 source -> zero-filled.
ZERO_FILL_WAVE_VARS = (
    "swh", "mwp", "cdww", "cos_mwd", "sin_mwd",
    "h1012", "h1214", "h1417", "h1721", "h2125", "h2530",
)

# The 16 AIFS v2 inputs missing from earth2studio's CDS lexicon.
_EXTRA_VOCAB = {
    # 10 hPa level (real ERA5)
    "t10": f"{PL}::temperature::10",
    "u10": f"{PL}::u_component_of_wind::10",
    "v10": f"{PL}::v_component_of_wind::10",
    "z10": f"{PL}::geopotential::10",
    # snow depth (real ERA5)
    "sd": f"{SL}::snow_depth::",
    # wave inputs: piggyback on 2m_temperature, zeroed by the modifier below
    **{w: f"{SL}::2m_temperature::" for w in ZERO_FILL_WAVE_VARS},
}


def patch_cds_lexicon_for_aifs2() -> list[str]:
    """Extend earth2studio's CDSLexicon so AIFS v2 can be initialized from ERA5.

    Idempotent. Returns the list of variables that are zero-filled.
    """
    from earth2studio.lexicon import CDSLexicon

    CDSLexicon.VOCAB.update(_EXTRA_VOCAB)
    zero = set(ZERO_FILL_WAVE_VARS)

    def get_item(cls, val: str):
        cds_key = cls.VOCAB[val]
        mod = (lambda x: np.zeros_like(x)) if val in zero else (lambda x: x)
        return cds_key, mod

    CDSLexicon.get_item = classmethod(get_item)
    return list(ZERO_FILL_WAVE_VARS)
