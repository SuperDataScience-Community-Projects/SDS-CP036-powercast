# SDS-CP036-powercast – Week 4 (Business Report)

## Table of Contents
- [Section 1 – Hyperparameter Optimization](#sds-cp036-powercast-–-week-4-section-1-hyperparameter-optimization)
- [Section 2 – Retraining & Validation](#sds-cp036-powercast-–-week-4-section-2-retraining--validation)
- [Section 3 – Model Selection & Trade-offs](#sds-cp036-powercast-–-week-4-section-3-model-selection--trade-offs)
- [Section 4 – Model Export & Deployment](#sds-cp036-powercast-–-week-4-section-4-model-export--deployment)
- [Section 5 – Monitoring & Maintenance Planning](#sds-cp036-powercast-–-week-4-section-5-monitoring--maintenance-planning)

# SDS-CP036-powercast – Week 4 Section 1: Hyperparameter Optimization

Profile: `dev`

### Key Questions Answered

**Q: Which hyperparameter tuning methods did you use, and why?**  
**A:** We used **lightweight grid search** tailored to runtime: a small, high-impact set for **XGBoost** (trees & learning rate) and 2 safe candidates for **SARIMAX** ((1,0,1) vs (1,1,1) with daily seasonality). This keeps dev runs **fast** while still exploring the parameters that move the needle.

**Q: What were the most important hyperparameters and how were ranges chosen?**  
**A:**  
- **XGBoost:** `n_estimators`, `max_depth`, `learning_rate` — they control **model capacity** and **how fast it learns**. Ranges are narrow by design for speed, widened in `preprod/final` if needed.  
- **SARIMAX:** difference order `d` and seasonal structure — governs **memory** and **daily cycle** fit.

**Q: How did you avoid data leakage or overfitting during tuning?**  
**A:** We tune on a **validation slice** only (train→validate split in time order). The **test set is untouched** until Section 2. We also **cap model sizes** and use **hourly resampling** for SARIMAX to keep complexity in check.

### Where to look
- Full tuning table: `results/Wk04_Section1_dev/reports/tuning_results.csv`  
- Best-per-zone params: `results/Wk04_Section1_dev/reports/best_params.json`

### Business Value (Executive View)
- **Faster learning loops** by focusing on parameters that matter.  
- **Safer decisions** (no leakage) → test numbers you can trust.  
- **Right-sized models** that balance accuracy and runtime.

# SDS-CP036-powercast – Week 4 Section 2: Retraining & Validation

Profile: `dev`

### Key Questions Answered
**Q: How did you retrain your best models on the full training data after tuning?**  
**A:** We **combined train+validation** and re-fit the chosen model per zone (from Section 1).

**Q: What steps did you take to validate model performance on the test set?**  
**A:** We kept the **chronological test slice untouched** during tuning, then forecasted its horizon and captured **RMSE/MAE/MAPE**.

**Q: Did you observe changes after retraining? How did you interpret them?**  
**A:** Minor metric shifts are expected (more data → steadier estimates). If accuracy improved, the model benefited from more context; if it dipped slightly, that suggests **variance vs. bias** trade-offs and highlights where to adjust features or parameters.

### Artifacts
- Test metrics: `results/Wk04_Section2_dev/reports/retrain_test_metrics.csv`  
- Plots (actual vs predicted) in: `results/Wk04_Section2_dev/plots/`

### Business Value (Executive View)
- **Trustworthy test numbers** (tuning never saw the test data).  
- **Closer-to-production fit** by retraining on the full learning window.

# SDS-CP036-powercast – Week 4 Section 3: Model Selection & Trade-offs

Profile: `dev`

### Key Questions Answered
**Q: What trade-offs did you consider when selecting your final model(s) for each zone?**  
**A:** We weighed **accuracy vs. runtime vs. interpretability**. If a complex model (e.g., XGBoost) beats SARIMAX meaningfully on **MAPE**, it’s chosen; otherwise, we prefer **simpler** models that are easier to operate.

**Q: How did you compare and document performance of different models?**  
**A:** We use the **Section 2 test metrics** and select the lowest **MAPE** per zone (champion). Full details are saved to `results/Wk04_Section3_dev/reports/champion_models.csv`.

**Q: What factors influenced final selection?**  
**A:**  
- **Interpretability:** SARIMAX is clearer for audits; XGB is stronger for non-linear spikes.  
- **Accuracy:** Champion is the lowest-MAPE model per zone.  
- **Compute cost:** Preference for models that meet SLAs with modest resources.

### Outcome
Champion models per zone (lowest MAPE): `results/Wk04_Section3_dev/reports/champion_models.csv`

### Business Value (Executive View)
- **Clear, defendable choices** with traceable criteria.  
- **Right tool for each zone**—maximize accuracy where it matters, keep operations simple where gains are marginal.

# SDS-CP036-powercast – Week 4 Section 4: Model Export & Deployment

Profile: `dev`

### Key Questions Answered
**Q: How did you export your final model(s) for deployment, and what format did you use?**  
**A:** We saved models as **pickled artifacts** under `models/Wk04_dev` with small companion JSON metadata. XGBoost models use the lag‑features interface; SARIMAX uses a lightweight stub to re-fit with fresh data at deploy time.

**Q: What considerations did you take into account for production deployment?**  
**A:** Reproducible artifacts, **minimal dependencies**, and a simple **inference_runner.py** that supports rolling forecasts with lag inputs.

**Q: Did you create any custom functions/classes for inference?**  
**A:** Yes — `predict_xgb_lags` supports recursive multi‑step forecasts, which mirrors our training setup.

### Artifacts
- Saved models: `models/Wk04_dev/`  
- Inference helper: `models/Wk04_dev/inference_runner.py`

### Business Value (Executive View)
- **Portable models** ready for CI/CD.  
- **Clear interface** for engineering hand-off.  
- **Stable behavior** between staging and production.

# SDS-CP036-powercast – Week 4 Section 5: Monitoring & Maintenance Planning

Profile: `dev`

### Key Questions Answered
**Q: How do you plan to monitor model performance and data quality in production?**  
**A:** We track **data health**, **feature drift** (7‑day vs 30‑day statistics), and **MAPE/RMSE/MAE** weekly.

**Q: What thresholds or indicators will prompt a retraining or update?**  
**A:** **15%+ drift** or **MAPE > 10%** for 2 consecutive weeks triggers action.

**Q: How will you handle data drift or pattern changes?**  
**A:** Investigate drivers (weather/events), adjust features/seasonality, and **retrain with recent data** if drift persists.

### Artifacts
- Monitoring snapshot: `results/Wk04_Section5_dev/reports/monitoring_snapshot.csv`  
- Alerts (if any): `results/Wk04_Section5_dev/reports/monitoring_alerts.csv`  
- Playbook: `results/Wk04_Section5_dev/reports/monitoring_playbook.md`

### Business Value (Executive View)
- **Early warning system** to prevent surprises.  
- **Clear thresholds** and **ownership**—so action is fast and consistent.
