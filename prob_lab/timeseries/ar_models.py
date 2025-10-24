
from __future__ import annotations
import numpy as np
from statsmodels.tsa.arima.model import ARIMA

def fit_arima(x: np.ndarray, order=(1,0,0)):
    model = ARIMA(x, order=order)
    res = model.fit()
    return res
