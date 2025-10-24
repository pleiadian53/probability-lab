
from __future__ import annotations
import pandas as pd
import polars as pl
import numpy as np

def read_table(path: str, engine: str | None = None):
    if path.endswith(('.parquet', '.pq')):
        return pl.read_parquet(path) if engine!='pandas' else pd.read_parquet(path)
    else:
        return pl.read_csv(path) if engine!='pandas' else pd.read_csv(path)

def to_numpy(series) -> np.ndarray:
    if isinstance(series, pl.Series):
        return series.drop_nulls().to_numpy()
    if isinstance(series, pd.Series):
        return series.dropna().to_numpy()
    raise TypeError("Pass a pandas or polars Series.")

def make_synthetic_survival(n=1000, scale=10.0, shape=1.5, censor_rate=0.3, seed=0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    # Weibull time-to-event
    u = rng.random(n)
    t = scale * (-np.log(1-u))**(1/shape)
    # Right censoring
    c = rng.exponential(scale=scale, size=n)
    observed = t <= c
    time = np.where(observed, t, c)
    df = pd.DataFrame({"time": time, "event": observed.astype(int)})
    return df
