
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
