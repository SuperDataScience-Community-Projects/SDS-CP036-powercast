
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
