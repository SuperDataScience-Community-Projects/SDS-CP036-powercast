# SDS-CP036-powercast – Week 3 Section 3: Evaluation & Model Interpretation & Insights

Profile: `dev`

### Key Questions Answered

**Q: How did you interpret feature importance or model coefficients, and what did they reveal about power consumption drivers?**  
**A:** We used three complementary lenses:
- **Correlation lens:** Pearson correlations between zone demand and drivers (Temperature, Humidity, Wind Speed, solar diffuse flows). See `results/Wk03_Section3_dev/reports/feature_correlations.csv` and bar charts in `results/Wk03_Section3_dev/plots/`.
- **SARIMAX coefficients:** Lightweight daily-seasonal model on hourly data to expose autoregressive and seasonal strength. See `results/Wk03_Section3_dev/reports/sarimax_coefficients.csv`.
- **XGBoost lag importances:** Non‑linear model with 24 lag features; top bars highlight which recent hours matter most. See `results/Wk03_Section3_dev/reports/xgb_importances.csv` and plots in `results/Wk03_Section3_dev/plots/`.

**Q: Did you observe any systematic errors or biases in your model predictions? How did you investigate and address them?**  
**A:** After forecasting the test window, we computed **residuals = Actual − Predicted** and averaged by **hour of day**. Consistent positive residuals at an hour mean we **under‑predict** that slot (peaks), negatives mean **over‑predict**. See `results/Wk03_Section3_dev/reports/residual_bias_by_hour.csv` and the bias charts in `results/Wk03_Section3_dev/plots/`.  
**Actions:** If evening hours are under‑predicted, we (a) enable native‑freq SARIMAX in `final` to capture sharper cycles, (b) add more lags or calendar/weather features to XGBoost.

**Q: What trade-offs did you consider when selecting your final model(s) for each zone?**  
**A:** We balance **accuracy vs. simplicity vs. speed**:
- **SARIMAX:** fast, explainable, strong daily cycle capture; may miss non‑linear spikes.
- **XGBoost (lags):** better for non‑linear patterns; requires feature care and is heavier than SARIMAX.
The chosen model per zone reflects the smallest footprint that meets accuracy needs, guided by the above diagnostics.

### What this run produced
- Correlation table: `results/Wk03_Section3_dev/reports/feature_correlations.csv`  
- SARIMAX coefficients: `results/Wk03_Section3_dev/reports/sarimax_coefficients.csv`  
- XGBoost importances: `results/Wk03_Section3_dev/reports/xgb_importances.csv`  
- Residual bias by hour: `results/Wk03_Section3_dev/reports/residual_bias_by_hour.csv`  
- Plots: `results/Wk03_Section3_dev/plots/`

### Business Value (Executive View)
- **Clarity on drivers:** Leaders see which **weather/time signals** move demand.  
- **Actionable fixes:** Bias‑by‑hour points to where to **tune models or operations** (staffing, procurement).  
- **Confidence & defensibility:** Simple visuals + tables support decisions in reviews and audits.
