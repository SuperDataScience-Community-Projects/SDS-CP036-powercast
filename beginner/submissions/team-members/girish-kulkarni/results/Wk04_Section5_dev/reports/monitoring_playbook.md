
# Powercast — Monitoring Playbook (Week 4 Section 5)

**What to watch**  
- **Data health:** Missing timestamps, duplicate DateTime, outlier spikes.  
- **Feature drift:** 7‑day vs 30‑day mean/variance for demand and key drivers.  
- **Performance:** Weekly RMSE/MAE/MAPE vs. acceptance thresholds.

**Thresholds & Actions**  
- **Data drift:** |Δmean| > **15%** → open investigation; if sustained 2 weeks, retrain.  
- **Performance:** MAPE > **10%** for 2 consecutive weeks → tune or switch model.  
- **Anomalies:** Unexplained spikes → escalate to operations; annotate holiday/events.

**Who does what**  
- **Data engineering:** Pipeline checks & backfills.  
- **DS/ML:** Retraining, feature updates.  
- **Ops:** Calendar events, demand-side actions.

**Cadence**  
- **Daily:** Data health checks.  
- **Weekly:** Performance dashboard & drift review.  
- **Quarterly:** Architecture review and model refresh planning.
