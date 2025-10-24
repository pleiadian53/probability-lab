
from __future__ import annotations
import numpy as np
import pandas as pd
from lifelines import KaplanMeierFitter, WeibullFitter, LogNormalFitter, LogLogisticFitter

def km_curve(df: pd.DataFrame, time_col="time", event_col="event"):
    km = KaplanMeierFitter()
    km.fit(df[time_col], event_observed=df[event_col])
    return km

def parametric_fits(df: pd.DataFrame, time_col="time", event_col="event"):
    fits = {}
    for name, F in [("Weibull", WeibullFitter), ("LogNormal", LogNormalFitter), ("LogLogistic", LogLogisticFitter)]:
        try:
            m = F().fit(df[time_col], df[event_col], label=name)
            fits[name] = m
        except Exception as e:
            fits[name] = e
    return fits
