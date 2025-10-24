
import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
from prob_lab.data.loaders import make_synthetic_survival
from prob_lab.distributions.scipy_wrappers import fit_scipy
from prob_lab.visualize.plot import pdf_ecdf_overlay, qq_plot
import matplotlib.pyplot as plt

st.set_page_config(page_title="Probability Lab", layout="wide")
st.title("🧪 Probability Lab — Distribution Explorer")

st.sidebar.header("Data")
mode = st.sidebar.radio("Choose data source", ["Upload CSV", "Synthetic survival (Weibull)"])

if mode == "Upload CSV":
    file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
    if file is not None:
        df = pd.read_csv(file)
else:
    n = st.sidebar.slider("n", 100, 5000, 1000, 100)
    shape = st.sidebar.slider("Weibull shape", 0.5, 3.0, 1.5, 0.1)
    scale = st.sidebar.slider("Weibull scale", 1.0, 30.0, 10.0, 0.5)
    censor = st.sidebar.slider("Censor rate", 0.0, 0.9, 0.3, 0.05)
    df = make_synthetic_survival(n=n, scale=scale, shape=shape, censor_rate=censor, seed=0)

st.write("Preview:", df.head())

col = st.selectbox("Column to fit", df.columns.tolist())
dist = st.selectbox("Distribution", ["expon","weibull_min","lognorm","gamma","gompertz","genextreme","gpd"])

x = df[col].dropna().to_numpy()

try:
    fr = fit_scipy(dist, x)
    st.success(f"{dist} fit: params={fr.params}, loc={fr.loc:.3f}, scale={fr.scale:.3f}, AIC={fr.aic:.2f}")
    c1, c2 = st.columns(2)
    with c1:
        fig1 = pdf_ecdf_overlay(x, dist, fr.params, fr.loc, fr.scale, path=None, title=f"{dist} CDF vs ECDF")
        st.pyplot(fig1, clear_figure=True)
    with c2:
        fig2 = qq_plot(x, dist, fr.params, fr.loc, fr.scale, path=None, title=f"{dist} QQ plot")
        st.pyplot(fig2, clear_figure=True)
except Exception as e:
    st.error(str(e))
