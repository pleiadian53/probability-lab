
from __future__ import annotations
import numpy as np
from scipy import stats
from .base import FitResult

def fit_block_maxima(x: np.ndarray, block_size: int = 30) -> FitResult:
    blocks = int(np.ceil(len(x)/block_size))
    maxima = np.array([x[i*block_size:(i+1)*block_size].max() for i in range(blocks)])
    c, loc, scale = stats.genextreme.fit(maxima)  # SciPy's genextreme uses sign convention (shape=c)
    loglik = np.sum(stats.genextreme.logpdf(maxima, c, loc=loc, scale=scale))
    n = len(maxima)
    k = 3
    aic = 2*k - 2*loglik
    bic = k*np.log(n) - 2*loglik
    return FitResult("genextreme(block-maxima)", (c,), loc, scale, aic, bic, loglik, n)

def fit_gpd_threshold(x: np.ndarray, threshold: float) -> FitResult:
    exceed = x[x>threshold] - threshold
    c, loc, scale = stats.genpareto.fit(exceed, floc=0.0)  # fix loc=0 on excesses
    loglik = np.sum(stats.genpareto.logpdf(exceed, c, loc=loc, scale=scale))
    n = len(exceed)
    k = 2 + 1  # shape+scale + known loc(0) counts? keep k=2 or 3; here use 2 effective
    aic = 2*(2) - 2*loglik
    bic = (2)*np.log(n) - 2*loglik
    return FitResult("genpareto(excess over threshold)", (c,), 0.0, scale, aic, bic, loglik, n)
