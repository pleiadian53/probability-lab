
from __future__ import annotations
import os
import typer
import pandas as pd
from rich import print
from prob_lab.data.loaders import read_table
from prob_lab.distributions.scipy_wrappers import fit_scipy
from prob_lab.visualize.plot import pdf_ecdf_overlay, qq_plot

app = typer.Typer()

@app.command()
def main(csv: str, column: str, dist: str="weibull_min", outdir: str="outputs"):
    os.makedirs(outdir, exist_ok=True)
    df = pd.read_csv(csv)
    x = df[column].dropna().to_numpy()
    fr = fit_scipy(dist, x)
    print(f"[bold cyan]{dist}[/] fit -> params={fr.params}, loc={fr.loc:.3f}, scale={fr.scale:.3f}, AIC={fr.aic:.2f}")
    pdf_ecdf_overlay(x, dist, fr.params, fr.loc, fr.scale, path=os.path.join(outdir, "cdf_overlay.png"), title=f"{dist} CDF vs ECDF")
    qq_plot(x, dist, fr.params, fr.loc, fr.scale, path=os.path.join(outdir, "qq.png"), title=f"{dist} QQ plot")
    print(f"Saved plots to {outdir}/")

if __name__ == "__main__":
    app()
