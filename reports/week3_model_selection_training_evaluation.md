# Week 3 — Model Selection, Training, and Evaluation Framework

## Purpose
A systematic framework for selecting, training, evaluating, and deploying machine-learning models for retail. This is a proposed framework; actual performance must be established through experiments on suitable data.

## Use cases and algorithms
- **Demand forecasting / sales prediction:** seasonal-naive baseline, Linear Regression with features, Random Forest, Gradient Boosting.
- **Customer churn / campaign response:** DummyClassifier, Logistic Regression, Decision Tree, Random Forest.
- **Customer segmentation:** K-Means, hierarchical clustering, DBSCAN where suitable.
- **Recommendations:** popularity baseline, item-item similarity, collaborative filtering, content-based methods when metadata exists.
- **Return/fraud review support:** classification or anomaly detection, with human review for consequential decisions.

## Workflow
```text
Business question and success metric
               |
Define target, prediction unit, horizon, and decision owner
               |
Collect -> profile -> validate -> clean
               |
Split train / validation / test without leakage
               |
Build baseline -> train candidate models
               |
Cross-validation + hyperparameter tuning
               |
Evaluate against baseline and business thresholds
               |
Error analysis and stakeholder review
               |
Controlled deployment -> monitoring -> retraining decision
```

## Data preparation
1. Define each row's meaning, target, and prediction time.
2. Profile missingness, duplicates, dates, distributions, outliers, and target balance.
3. Remove target-leaking fields and information unavailable at prediction time.
4. Fit imputation, scaling, encoding, and feature selection only within training folds using Scikit-learn Pipeline/ColumnTransformer.
5. Use chronological holdouts or time-series validation for forecasting; use stratified splits for independent classification when suitable.
6. Keep the final test set untouched until final evaluation.
7. Record dataset version, features, random seeds, and package versions.

## Metrics
- **MAE:** average absolute error in target units.
- **RMSE:** penalises large errors more heavily than MAE.
- **Accuracy:** fraction correct; may mislead for imbalanced classes.
- **Precision:** fraction of predicted positives that are truly positive.
- **Recall:** fraction of actual positives found.
- **F1:** harmonic mean of precision and recall.
- **ROC-AUC / PR-AUC:** ranking quality across thresholds; PR-AUC can help with rare positives.
- **Silhouette score:** cluster separation diagnostic, not proof of business value.
- **Precision@K / Recall@K:** recommendation ranking metrics.

## Benchmarking
1. Establish a simple baseline.
2. Use identical splits for all candidates.
3. Tune only on training/validation data.
4. Compare primary/secondary metrics and runtime.
5. Review errors by store, category, season, and customer group where permitted.
6. Report fold variability and avoid repeated selection against the final test set.
7. For forecasts, compare against last-period or seasonal-naive predictions over multiple forecast origins where possible.

## Pseudocode
```text
load and validate dataset
define target, prediction unit, eligible features
split by time or stratification as appropriate
build preprocessing pipeline
evaluate baseline
for each candidate model and parameter set:
    fit using training folds
    calculate task-appropriate metrics
select using pre-defined criteria
evaluate once on untouched test set
review errors, leakage, privacy, and cost
save model, preprocessing, metadata, and report
deploy in controlled mode and monitor drift
```

## Testing and risk mitigation
- Unit-test feature engineering, schema checks, and metrics.
- Test duplicates, missingness, invalid values, distribution changes, and leakage.
- Confirm the full preprocessing/model pipeline works on unseen rows.
- Compare against baseline and examine subgroup errors.
- Mitigate seasonality, stock-out censoring, promotion effects, imbalance, overfitting, drift, privacy exposure, and historical bias.
- Use access controls, human review for high-impact decisions, monitoring, and rollback to a baseline/prior model.

## Deployment and monitoring
Start with controlled batch scoring. Monitor data freshness, schema failures, missing features, prediction distributions, forecast errors, precision/recall, latency, and business KPIs. Define alert thresholds, rollback, and review/retraining criteria before release. Retraining must be validated before release.

## Limitations
This document is a strategy and evaluation plan, not a claim of trained or deployed production models. Results depend on suitable, authorised, representative retail data.
