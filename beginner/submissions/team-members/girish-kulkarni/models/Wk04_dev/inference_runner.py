
import pickle, json
import numpy as np
import pandas as pd
from pathlib import Path

def load_model(path: str):
    with open(path, 'rb') as f:
        return pickle.load(f)

def predict_xgb_lags(model_obj, recent_values, horizon=1, max_lag=24):
    history = list(recent_values)
    preds = []
    for _ in range(horizon):
        feats = [history[-k] for k in range(1, max_lag+1)]
        pred = float(model_obj.predict(np.array(feats).reshape(1,-1)))
        preds.append(pred)
        history.append(pred)
    return np.array(preds)
