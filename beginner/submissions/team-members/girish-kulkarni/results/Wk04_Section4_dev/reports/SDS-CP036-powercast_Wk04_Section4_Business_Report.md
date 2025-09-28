
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
