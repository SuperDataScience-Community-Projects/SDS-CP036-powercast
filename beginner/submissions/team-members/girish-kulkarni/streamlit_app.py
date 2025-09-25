import io, re, json, pickle, importlib.util
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# --- Paths (fallbacks if no upload) ---
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "Tetuan City power consumption.csv"
MODELS_DIR = BASE_DIR / "models" / "Wk04_dev"   # change to Wk04_final when ready

st.set_page_config(page_title="Powercast – Forecasting", layout="wide")

# ========= Uploader UI (left sidebar) =========
st.sidebar.header("Dataset")
uploaded = st.sidebar.file_uploader("Upload CSV data", type=["csv"])
use_uploaded = st.sidebar.checkbox("Use uploaded file (if provided)", value=True, disabled=(uploaded is None))
st.sidebar.caption("Tip: Keep the original columns (e.g., 'DateTime', 'Zone 1 Power Consumption', etc.).")

# --- Helpers ---
def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [re.sub(r"\\s+", " ", c.strip()) for c in df.columns]
    return df

@st.cache_data(show_spinner=False)
def load_data_from_bytes(b: bytes) -> pd.DataFrame:
    df = pd.read_csv(io.BytesIO(b))
    df = _normalize_columns(df)
    if "DateTime" not in df.columns:
        alts = [c for c in df.columns if c.lower() == "datetime"]
        if alts:
            df = df.rename(columns={alts[0]: "DateTime"})
        else:
            raise ValueError("No 'DateTime' column found in uploaded file.")
    df["DateTime"] = pd.to_datetime(df["DateTime"])
    df = df.sort_values("DateTime").set_index("DateTime")
    return df

@st.cache_data(show_spinner=False)
def load_data_from_path() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    df = _normalize_columns(df)
    if "DateTime" not in df.columns:
        alts = [c for c in df.columns if c.lower() == "datetime"]
        if alts:
            df = df.rename(columns={alts[0]: "DateTime"})
        else:
            raise ValueError("No 'DateTime' column found in default dataset.")
    df["DateTime"] = pd.to_datetime(df["DateTime"])
    df = df.sort_values("DateTime").set_index("DateTime")
    return df

@st.cache_resource(show_spinner=False)
def load_artifacts():
    arts = []
    if MODELS_DIR.exists():
        for p in MODELS_DIR.glob("*.pkl"):
            meta = p.with_suffix(".meta.json")
            meta_obj = json.loads(meta.read_text()) if meta.exists() else {}
            arts.append({"name": p.stem, "pkl": p, "meta": meta_obj})
    return arts

def dynamic_runner():
    runner_py = MODELS_DIR / "inference_runner.py"
    if runner_py.exists():
        spec = importlib.util.spec_from_file_location("runner", runner_py)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    # Fallback minimal runner
    class Fallback:
        def predict_xgb_lags(self, model_obj, recent_values, horizon=1, max_lag=24):
            history = list(recent_values); preds = []
            for _ in range(horizon):
                feats = [history[-k] for k in range(1, max_lag+1)]
                pred = float(model_obj.predict(np.array(feats).reshape(1, -1)))
                preds.append(pred); history.append(pred)
            return np.array(preds)
    return Fallback()

def load_pickle(path: Path):
    with open(path, "rb") as f:
        return pickle.load(f)

def zone_columns(df):
    return [c for c in df.columns if re.match(r"Zone\\s+\\d+\\s+Power\\s+Consumption", c)]

def metrics(y_true, y_pred):
    y_true = np.asarray(y_true, float); y_pred = np.asarray(y_pred, float)
    mae = float(np.mean(np.abs(y_true - y_pred)))
    rmse = float(np.sqrt(np.mean((y_true - y_pred)**2)))
    denom = np.where(y_true == 0, 1e-8, np.abs(y_true))
    mape = float(np.mean(np.abs((y_true - y_pred)/denom)) * 100)
    return rmse, mae, mape

# --- Decide which dataset to use ---
try:
    if uploaded and use_uploaded:
        df = load_data_from_bytes(uploaded.getvalue())
        st.success(f"Using uploaded file: {uploaded.name}  •  rows={len(df):,}")
    else:
        df = load_data_from_path()
        st.info(f"Using default dataset: {DATA_PATH.name}  •  rows={len(df):,}")
except Exception as e:
    st.error(f"Failed to load data: {e}")
    st.stop()

# Optional preview
with st.expander("Preview first 10 rows (after normalization)"):
    st.dataframe(df.head(10))

# --- UI ---
st.title("⚡ Powercast – Demand Forecasting")
zones = zone_columns(df)
if not zones:
    st.error("No 'Zone X Power Consumption' columns found.")
    st.stop()

# infer native step
if len(df.index) >= 2:
    step = df.index[1] - df.index[0]
else:
    step = pd.Timedelta(minutes=10)

col1, col2, col3 = st.columns([1,1,1])
with col1:
    zone = st.selectbox("Zone", zones, index=0)
with col2:
    horizon = st.number_input("Forecast horizon (steps)", min_value=1, max_value=288, value=72, step=12,
                              help="One step = one row in the native data (typically 10 minutes).")
with col3:
    mode = st.selectbox("Model", ["Auto (Champion)", "XGB (lags)", "SARIMAX stub", "Baseline (naïve)"])

arts = load_artifacts()
runner = dynamic_runner()

# Pick artifact
chosen = None
if mode == "Auto (Champion)":
    for pref in ["XGB", "SARIMAX"]:
        for a in arts:
            if zone.replace(" ", "_") in a["name"] and pref in a["name"]:
                chosen = a; break
        if chosen: break
elif mode == "XGB (lags)":
    for a in arts:
        if zone.replace(" ", "_") in a["name"] and "XGB" in a["name"]:
            chosen = a; break
elif mode == "SARIMAX stub":
    for a in arts:
        if zone.replace(" ", "_") in a["name"] and "SARIMAX" in a["name"]:
            chosen = a; break

st.write("---")
# Forecast
if mode == "Baseline (naïve)" or not chosen:
    if not chosen and mode != "Baseline (naïve)":
        st.warning("No matching artifact found for the selected model; using baseline.")
    history = df[zone].dropna().values
    yhat = np.repeat(history[-1], int(horizon))
    idx = pd.date_range(df.index[-1] + step, periods=int(horizon), freq=step)
    y_true = df[zone].iloc[-int(horizon):].values if len(df)>=int(horizon) else np.array([])
    rmse, mae, mape = metrics(y_true, yhat[:len(y_true)]) if len(y_true)>0 else (np.nan, np.nan, np.nan)
else:
    model_obj = load_pickle(chosen["pkl"])
    meta = chosen["meta"]
    if meta.get("type") == "xgb_lags":
        max_lag = meta.get("max_lag", 24)
        recent = df[zone].dropna().values[-max_lag:]
        yhat = runner.predict_xgb_lags(model_obj, recent, horizon=int(horizon), max_lag=max_lag)
        idx = pd.date_range(df.index[-1] + step, periods=int(horizon), freq=step)
        y_true = df[zone].iloc[-int(horizon):].values if len(df)>=int(horizon) else np.array([])
        rmse, mae, mape = metrics(y_true, yhat[:len(y_true)]) if len(y_true)>0 else (np.nan, np.nan, np.nan)
    else:
        # SARIMAX stub: no refit, emit flat forecast from last value
        history = df[zone].dropna().values
        yhat = np.repeat(history[-1], int(horizon))
        idx = pd.date_range(df.index[-1] + step, periods=int(horizon), freq=step)
        y_true = df[zone].iloc[-int(horizon):].values if len(df)>=int(horizon) else np.array([])
        rmse, mae, mape = metrics(y_true, yhat[:len(y_true)]) if len(y_true)>0 else (np.nan, np.nan, np.nan)

# Plot
fig, ax = plt.subplots(figsize=(10,4))
past = df[zone].iloc[-int(horizon)*2:] if len(df)>=int(horizon)*2 else df[zone]
ax.plot(past.index, past.values, label="Actual (recent)")
ax.plot(idx, yhat, label="Forecast")
ax.set_title(f"{zone} – Forecast")
ax.set_xlabel("Time"); ax.set_ylabel("Power")
ax.legend(); st.pyplot(fig)

# Metrics
st.subheader("Quick metrics (if last-horizon ground truth exists)")
m1, m2, m3 = st.columns(3)
m1.metric("RMSE", f"{rmse:,.0f}" if rmse==rmse else "—")
m2.metric("MAE",  f"{mae:,.0f}" if mae==mae else "—")
m3.metric("MAPE", f"{mape:,.2f}%" if mape==mape else "—")

# Download
out = pd.DataFrame({"forecast": yhat}, index=idx)
st.download_button("Download forecast CSV", out.to_csv().encode("utf-8"),
                   file_name=f"{zone.replace(' ','_')}_forecast.csv", mime="text/csv")

st.caption("Upload a CSV in the sidebar to try new data. If none provided, the default dataset is used. "
           "Models are loaded from models/Wk04_dev/.")