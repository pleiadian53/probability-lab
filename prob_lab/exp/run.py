
from __future__ import annotations
import os
from typing import Any
import numpy as np
import pandas as pd

from omegaconf import DictConfig, OmegaConf
import hydra
from hydra.utils import to_absolute_path as abspath

try:
    from prob_lab.data.loaders import read_table
    from prob_lab.distributions.scipy_wrappers import fit_scipy
    from prob_lab.visualize.plot import pdf_ecdf_overlay, qq_plot
    from prob_lab.distributions import extreme_value as evt
except Exception:
    pass

def _load_series(path: str, column: str, engine: str) -> np.ndarray:
    df = pd.read_csv(abspath(path))
    return df[column].dropna().to_numpy()

@hydra.main(config_path='../../conf', config_name='config', version_base='1.3')
def main(cfg: DictConfig) -> None:
    print("\n[Probability Lab] Experiment config:\n" + OmegaConf.to_yaml(cfg))
    outdir = os.getcwd()
    os.makedirs(outdir, exist_ok=True)

    x = _load_series(cfg.data.path, cfg.data.column, cfg.data.engine)

    results = {}
    if cfg.fit.mle:
        fr = fit_scipy(cfg.fit.dist, x)
        results['mle'] = fr
        print(f"MLE {cfg.fit.dist}: params={fr.params}, loc={fr.loc:.4f}, scale={fr.scale:.4f}, AIC={fr.aic:.2f}")

    if cfg.extreme.enabled:
        if cfg.extreme.mode == 'block_maxima':
            fr_ev = evt.fit_block_maxima(x, block_size=cfg.extreme.block_size)
            results['extreme'] = fr_ev
            print(f"EVT GEV (block={cfg.extreme.block_size}): shape={fr_ev.params[0]:.4f}, loc={fr_ev.loc:.4f}, scale={fr_ev.scale:.4f}")
        elif cfg.extreme.mode == 'peaks_over_threshold':
            thr = float(cfg.extreme.threshold)
            if 0 < thr < 1:
                thr_val = float(np.quantile(x, thr))
            else:
                thr_val = thr
            fr_ev = evt.fit_gpd_threshold(x, threshold=thr_val)
            results['extreme'] = fr_ev
            print(f"EVT GPD (u={thr_val:.4f}): shape={fr_ev.params[0]:.4f}, scale={fr_ev.scale:.4f}")

    if cfg.viz.cdf_overlay and 'mle' in results:
        fr = results['mle']
        pdf_ecdf_overlay(x, cfg.fit.dist, fr.params, fr.loc, fr.scale, path=os.path.join(outdir, 'cdf_overlay.png'), title=f"{cfg.fit.dist} CDF vs ECDF")
    if cfg.viz.qq and 'mle' in results:
        fr = results['mle']
        qq_plot(x, cfg.fit.dist, fr.params, fr.loc, fr.scale, path=os.path.join(outdir, 'qq.png'), title=f"{cfg.fit.dist} QQ Plot")

    # Save summary
    try:
        import json
        def _clean(fr):
            if hasattr(fr, "__dict__"):
                d = fr.__dict__.copy()
                for k in list(d.keys()):
                    if k.endswith("_"):
                        d.pop(k)
                return d
            return fr
        summ = {k: _clean(v) for k, v in results.items()}
        with open(os.path.join(outdir, "summary.json"), "w") as f:
            json.dump(summ, f, indent=2, default=str)
    except Exception as e:
        print("[warn] summary.json:", e)

if __name__ == "__main__":
    main()
