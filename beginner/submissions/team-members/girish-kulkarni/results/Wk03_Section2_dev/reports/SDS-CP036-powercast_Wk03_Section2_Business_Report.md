# SDS-CP036-powercast – Week 3 Section 2: MLflow Experiment Tracking & Evaluation

Profile: `dev`

### Key Questions Answered

**Q: Which evaluation metrics did you use to assess model performance, and why are they appropriate for this problem?**  
**A:** We report **RMSE** (penalizes bigger errors), **MAE** (average absolute miss in original units), and **MAPE** (percent error, easy to read for business). Together they show both **size of mistakes** and **relative impact**.

**Q: How did you use MLflow (or another tool) to track your experiments and results?**  
**A:** When MLflow is available, we:
- Create a local tracking store under `results/Wk03_Section2_dev/mlruns` and an experiment named `Powercast_Wk03_S2_dev`.
- Log **parameters** (model type, seasonal settings, lags) and **metrics** (RMSE/MAE/MAPE) **per zone**.
- Attach **artifacts** (actual vs predicted plots) to each run for quick visual review.  
If MLflow isn’t available, we still write a consolidated CSV: `results/Wk03_Section2_dev/reports/experiment_metrics.csv`.

**Q: What insights did you gain from comparing actual vs. predicted curves for each zone?**  
**A:** The plots in `results/Wk03_Section2_dev/plots/` make **pattern fit** transparent:
- If the model tracks the **daily peaks and troughs**, it’s capturing seasonality.
- If forecasts **lag changes** or **flatten peaks**, we switch/tune models (e.g., enable XGBoost for non‑linear spikes, use native‑freq SARIMAX in `final`).

### What’s included in this run
- Zones modeled: 1  
- Data window: Last 90 days  
- Test horizon: 7 day(s) × native steps/day = 1008 steps

**Artifacts for reviewers**
- Metrics table: `results/Wk03_Section2_dev/reports/experiment_metrics.csv`  
- MLflow runs (if enabled): `results/Wk03_Section2_dev/mlruns`  
- Visuals: `results/Wk03_Section2_dev/plots/`

### Business Value (Executive View)
- **Traceability:** Every run is documented with parameters, metrics, and plots.  
- **Faster decisions:** Side‑by‑side runs quickly identify the **champion** model per zone.  
- **Governance‑ready:** Local MLflow store + CSV provide an audit trail suitable for leadership reviews.
