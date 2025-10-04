# SDS-CP036-powercast – Week 3 Section 1: Model Selection & Training

Profile: `dev`

### Key Questions Answered

**Q: Which machine learning models did you choose for forecasting power consumption, and what motivated your selections?**  
**A:** This run uses a **toggle-based approach**:
- **Baseline (Naïve):** Sets a minimum viable benchmark.
- **SARIMAX:** Time‑series model capturing daily cycles; in `dev` we fit **hourly** to keep training fast and then upsample.
- **Prophet** (optional): Captures trends/seasonality with built‑in holidays (if configured); fit hourly for speed and upsample.
- **XGBoost (lags)** (optional): Non‑linear patterns via lag features (e.g., last 24 time steps), forecasted recursively.

**Q: How did you structure your models to handle the multi-zone prediction task (separate models vs. multi-output)?**  
**A:** We train **separate per‑zone models**. Zones differ in behavior; per‑zone models are easier to tune and explain. `dev` runs 1 zone(s) for speed; `preprod/final` scale to all three.

**Q: What challenges did you encounter during model training, and how did you address them?**  
**A:** The main risks are **runtime** and **stability** with 10‑minute data. We addressed them by:
- Detecting native frequency and **downshifting to hourly** where appropriate.
- Capping iterations and window sizes for heavy models.
- Limiting CPU threads to avoid numeric library contention.

### What’s included in this run

- Data window: Last 90 days  
- Zones modeled: 1  
- Test horizon: 7 day(s) × native steps/day = 1008 steps

**Artifacts**  
- Model comparison (MAE/RMSE/MAPE): `results/Wk03_Section1_dev/reports/model_comparison.csv`  
- Plots: saved under `results/Wk03_Section1_dev/plots/`

### Business Value (Executive View)
- Establishes a **clear accuracy baseline** and optional advanced models for uplift.  
- Delivers **repeatable, time‑boxed** training to enable weekly iteration.  
- Produces **defensible metrics and visuals** for leadership and ops decisions.
