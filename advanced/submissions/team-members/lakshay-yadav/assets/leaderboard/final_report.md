# Phase 3 Model Tuning Report

## Summary
- Total configs evaluated: 30
- Final leaderboard size: 3 models

## Top Models (by RMSE)
| config | model | rmse | mae | r2 | orig_rmse | orig_mae | orig_r2 | ckpt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| lb144_hr6 | GRUModel | 0.09931149072026214 | 0.06715454906225204 | 0.9890754818916321 | 612.0640285133575 | 416.9034118652344 | 0.9803093075752258 | C:\Users\ABCD\_ML projects(SDS)\SDS-CP036-powercast\advanced\submissions\team-members\lakshay-yadav\assets\models\GRUModel_lb144_hr6_01fee3_best.pt |
| lb144_hr6 | LSTMModel | 0.10136222808848228 | 0.0723712369799614 | 0.9886196851730347 | 630.3428382634327 | 450.134521484375 | 0.9802725315093994 | C:\Users\ABCD\_ML projects(SDS)\SDS-CP036-powercast\advanced\submissions\team-members\lakshay-yadav\assets\models\LSTMModel_lb144_hr6_7cb338_best.pt |
| lb144_hr6 | TCNModel | 0.2997210382822246 | 0.23292867839336395 | 0.900496780872345 | 1811.9510892957348 | 1433.9990234375 | 0.8280623555183411 | C:\Users\ABCD\_ML projects(SDS)\SDS-CP036-powercast\advanced\submissions\team-members\lakshay-yadav\assets\models\TCNModel_lb144_hr6_115532_best.pt |

## Notes
- Results are based on **scaled training** with Week 3 scalers.
- Metrics reported on **original target scale** for interpretability.
- Best checkpoints are saved in `assets/best_checkpoints/`.
