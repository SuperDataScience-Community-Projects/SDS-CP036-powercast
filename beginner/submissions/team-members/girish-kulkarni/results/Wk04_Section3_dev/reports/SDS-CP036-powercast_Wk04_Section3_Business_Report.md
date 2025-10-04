
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
