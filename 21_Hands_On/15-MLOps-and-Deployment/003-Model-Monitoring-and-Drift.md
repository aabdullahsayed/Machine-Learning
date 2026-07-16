# 003 - Model Monitoring and Drift

## Concept
Once a model is deployed, its performance can silently degrade over time as the real world changes — this is called drift. Monitoring means continuously tracking input data distributions, prediction distributions, and (when available) actual outcomes to catch this early.

## Why It Matters
A model that scored 95% accuracy at launch can quietly drop to 70% six months later if the underlying data shifts — without monitoring, nobody notices until it causes a real business problem.

## Hands-On

```python
import numpy as np
import pandas as pd
from scipy.stats import ks_2samp

# 1. Simulate a training reference distribution and incoming production data
np.random.seed(42)
train_feature = np.random.normal(loc=50, scale=10, size=1000)

# Case A: production data with the same distribution (no drift)
prod_no_drift = np.random.normal(loc=50, scale=10, size=200)

# Case B: production data that has drifted (mean shifted)
prod_drifted = np.random.normal(loc=65, scale=10, size=200)

# 2. Kolmogorov-Smirnov test - detects if two samples come from different distributions
def check_drift_ks(reference, current, alpha=0.05):
    statistic, p_value = ks_2samp(reference, current)
    drifted = p_value < alpha
    return {"statistic": round(statistic, 4), "p_value": round(p_value, 4), "drift_detected": drifted}

print("No-drift case:", check_drift_ks(train_feature, prod_no_drift))
print("Drifted case:", check_drift_ks(train_feature, prod_drifted))

# 3. Population Stability Index (PSI) - a common industry metric for drift magnitude
def calculate_psi(reference, current, bins=10):
    breakpoints = np.linspace(0, 100, bins + 1)
    ref_percents = np.percentile(reference, breakpoints)
    ref_percents[0], ref_percents[-1] = -np.inf, np.inf

    ref_counts, _ = np.histogram(reference, bins=ref_percents)
    cur_counts, _ = np.histogram(current, bins=ref_percents)

    ref_pct = ref_counts / len(reference) + 1e-6
    cur_pct = cur_counts / len(current) + 1e-6

    psi = np.sum((cur_pct - ref_pct) * np.log(cur_pct / ref_pct))
    return psi

psi_no_drift = calculate_psi(train_feature, prod_no_drift)
psi_drifted = calculate_psi(train_feature, prod_drifted)
print(f"PSI (no drift): {psi_no_drift:.4f}")   # < 0.1 typically considered stable
print(f"PSI (drifted): {psi_drifted:.4f}")      # > 0.25 typically flagged as significant drift

# 4. Monitoring prediction distribution over time (a proxy when true labels are delayed/unavailable)
def monitor_prediction_distribution(predictions, label=""):
    unique, counts = np.unique(predictions, return_counts=True)
    dist = dict(zip(unique.tolist(), (counts / counts.sum()).round(3).tolist()))
    print(f"[{label}] prediction distribution: {dist}")

week1_preds = np.random.choice([0, 1], size=500, p=[0.7, 0.3])
week8_preds = np.random.choice([0, 1], size=500, p=[0.4, 0.6])  # class balance shifted
monitor_prediction_distribution(week1_preds, "Week 1")
monitor_prediction_distribution(week8_preds, "Week 8 - investigate!")

# 5. A simple monitoring log structure you'd write to a database/dashboard each day
log_entry = {
    "date": "2026-07-15",
    "n_predictions": 1500,
    "avg_confidence": 0.87,
    "psi_scores": {"feature_1": 0.03, "feature_2": 0.29},
    "accuracy_last_7d": 0.91,  # only computable once true labels arrive
}
print(log_entry)
```

## Exercise
1. Run the PSI calculation across all 30 features of the breast cancer dataset comparing a clean split vs. an artificially shifted split — which features are most sensitive to shift?
2. Build a small dashboard-style summary (a DataFrame) that logs PSI per feature per day for a week of simulated data.
3. Research and briefly describe "concept drift" vs. "data drift" — write 2-3 sentences distinguishing them.

## Key Takeaways
- Data drift (input distributions change) and concept drift (the relationship between inputs and outputs changes) are different problems and need different responses.
- PSI < 0.1 is usually fine, 0.1–0.25 worth watching, > 0.25 usually triggers investigation or retraining in industry practice.
- When true labels are delayed or unavailable, prediction distribution and confidence scores are useful proxy signals for catching problems early.
