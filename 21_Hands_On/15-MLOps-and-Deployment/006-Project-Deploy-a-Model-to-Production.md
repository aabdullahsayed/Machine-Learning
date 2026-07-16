# 006 - Project: Deploy a Model to Production

## Concept
This project combines every piece of module 15 into one working system: train a model, save it, wrap it in an API, containerize it, add monitoring, and describe how it fits into a CI/CD pipeline — a complete, minimal production deployment.

## Why It Matters
This is the "capstone" of MLOps: the difference between "I can train a good model" and "I can ship a good model that keeps working" is exactly the set of skills this project exercises.

## Hands-On

```python
# --- Step 1: Train and save the model + a fixed evaluation set ---
import pandas as pd
import numpy as np
import joblib
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

data = load_breast_cancer()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = pd.Series(data.target)

X_train, X_eval, y_train, y_eval = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

joblib.dump(model, "model.joblib")
eval_df = X_eval.copy()
eval_df["target"] = y_eval
eval_df.to_csv("eval_holdout.csv", index=False)   # fixed CI quality-gate dataset

print("Eval accuracy:", model.score(X_eval, y_eval))
```

```python
# --- Step 2: app.py - the serving API ---
"""
from fastapi import FastAPI
import joblib
import numpy as np
from datetime import datetime

app = FastAPI(title="Cancer Classifier API")
model = joblib.load("model.joblib")
prediction_log = []   # in production this would be a real database

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}

@app.post("/predict")
def predict(features: list[float]):
    X = np.array(features).reshape(1, -1)
    pred = model.predict(X)[0]
    confidence = model.predict_proba(X)[0].max()

    prediction_log.append({
        "timestamp": datetime.utcnow().isoformat(),
        "prediction": int(pred),
        "confidence": float(confidence),
    })
    return {"prediction": int(pred), "confidence": float(confidence)}

@app.get("/monitoring/summary")
def monitoring_summary():
    if not prediction_log:
        return {"n_predictions": 0}
    confidences = [p["confidence"] for p in prediction_log]
    return {
        "n_predictions": len(prediction_log),
        "avg_confidence": sum(confidences) / len(confidences),
        "min_confidence": min(confidences),
    }
"""
```

```dockerfile
# --- Step 3: Dockerfile ---
# FROM python:3.11-slim
# WORKDIR /app
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
# COPY app.py model.joblib ./
# EXPOSE 8000
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

```python
# --- Step 4: A quality gate script for CI (mirrors module 15-005) ---
import joblib
from sklearn.metrics import accuracy_score

MIN_ACCURACY = 0.90
model = joblib.load("model.joblib")
eval_df = pd.read_csv("eval_holdout.csv")
X_eval = eval_df.drop(columns=["target"])
y_eval = eval_df["target"]

acc = accuracy_score(y_eval, model.predict(X_eval))
print(f"Quality gate check: accuracy={acc:.4f}")
assert acc >= MIN_ACCURACY, f"Model below quality bar: {acc:.4f} < {MIN_ACCURACY}"
print("Quality gate PASSED - safe to deploy.")
```

```python
# --- Step 5: A basic drift check script to run on a schedule (mirrors 15-003) ---
from scipy.stats import ks_2samp

def check_feature_drift(reference_df, new_data_df, alpha=0.05):
    alerts = []
    for col in reference_df.columns:
        _, p_value = ks_2samp(reference_df[col], new_data_df[col])
        if p_value < alpha:
            alerts.append(col)
    return alerts

# Simulate a week of incoming data, some drifted
new_batch = X_eval.copy()
new_batch["mean radius"] *= 1.3
alerts = check_feature_drift(X_train, new_batch)
print("Drift alerts on latest batch:", alerts)
```

## Exercise
1. Actually run the FastAPI app locally, call `/predict` a handful of times, then call `/monitoring/summary` and confirm the counts match.
2. Wire the quality gate script and drift check script into a single `daily_check.py` that prints a PASS/FAIL summary — this is what a real scheduled job would run.
3. Write a one-page runbook (in your own words) describing what a teammate should do if `/monitoring/summary` shows `avg_confidence` dropping steadily over a week.

## Key Takeaways
- A production ML system is training + serving + monitoring + a quality gate, working together — not any single piece alone.
- Logging predictions (even simply, in memory or to a file) is what makes monitoring possible at all — you can't check for drift on data you never captured.
- This project is intentionally minimal — real systems add authentication, request logging to proper databases, autoscaling, and alerting, but the core shape is exactly what you just built.
