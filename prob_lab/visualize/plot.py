
from __future__ import annotations
import numpy as np
from typing import Optional
import matplotlib.pyplot as plt
from scipy import stats

def pdf_ecdf_overlay(x: np.ndarray, dist_name: str, params, loc, scale, path: Optional[str]=None, title: Optional[str]=None):
    x = np.asarray(x)
    x = x[np.isfinite(x)]
    xs = np.linspace(x.min(), x.max(), 400)
    # ECDF
    xs_sorted = np.sort(x)
    ys = np.arange(1, len(xs_sorted)+1)/len(xs_sorted)
    # PDF
    dist = getattr(stats, dist_name)
    pdf = dist.pdf(xs, *params, loc=loc, scale=scale)
    fig = plt.figure()
    plt.step(xs_sorted, ys, where="post", label="ECDF")
    plt.plot(xs, np.cumsum(pdf)/np.sum(pdf), label=f"{dist_name} CDF (normalized)")  # simple comparable overlay
    plt.xlabel("x")
    plt.ylabel("Probability")
    if title:
        plt.title(title)
    plt.legend()
    if path:
        plt.savefig(path, bbox_inches="tight", dpi=200)
    return fig

def qq_plot(x: np.ndarray, dist_name: str, params, loc, scale, path: Optional[str]=None, title: Optional[str]=None):
    x = np.asarray(x)
    x = x[np.isfinite(x)]
    dist = getattr(stats, dist_name)
    q = np.linspace(0.01, 0.99, 99)
    theor = dist.ppf(q, *params, loc=loc, scale=scale)
    samp = np.quantile(x, q)
    fig = plt.figure()
    plt.scatter(theor, samp, s=10)
    lims = [min(theor.min(), samp.min()), max(theor.max(), samp.max())]
    plt.plot(lims, lims, linestyle="--")
    plt.xlabel("Theoretical quantiles")
    plt.ylabel("Sample quantiles")
    if title:
        plt.title(title)
    if path:
        plt.savefig(path, bbox_inches="tight", dpi=200)
    return fig
