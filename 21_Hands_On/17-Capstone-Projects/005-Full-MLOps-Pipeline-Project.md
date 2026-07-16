# 005 - Capstone: Full MLOps Pipeline Project

## Concept
A simplified but complete MLOps loop: train a model → save it → serve it behind a small API → simulate incoming data → check for drift → know when to retrain. This connects module 15's individual pieces into one small working system.

## Why It Matters
A model sitting in a notebook delivers no value. This capstone shows the minimum viable version of what it takes to actually run a model in production and keep it healthy over time.

## Hands-On

```python
# --- Step 1: Train and save a model (same idea as capstone 001) ---
import pandas as pd
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

data = load_breast_cancer()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = data.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)
joblib.dump(model, "production_model.pkl")
print("Baseline test accuracy:", model.score(X_test, y_test))

# Save the training feature distribution - our reference for drift detection
train_summary = X_train.describe().loc[["mean", "std"]]
train_summary.to_csv("training_feature_summary.csv")
```

```python
# --- Step 2: A minimal serving API (FastAPI) - save as app.py and run separately ---
"""
from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()
model = joblib.load("production_model.pkl")

@app.post("/predict")
def predict(features: dict):
    X = pd.DataFrame([features])
    pred = model.predict(X)[0]
    proba = model.predict_proba(X)[0].max()
    return {"prediction": int(pred), "confidence": float(proba)}

# Run with: uvicorn app:app --reload
"""
print("See the docstring above for app.py - run separately with uvicorn.")
```

```python
# --- Step 3: Simulate incoming production data (some of it drifted) ---
np.random.seed(1)
normal_batch = X_test.sample(50, random_state=1)
drifted_batch = X_test.sample(50, random_state=2).copy()
drifted_batch["mean radius"] *= 1.4   # simulate a sensor/process change upstream

# --- Step 4: A simple drift check comparing incoming data to training stats ---
def check_drift(new_data, train_summary, threshold=2.0):
    alerts = []
    for col in new_data.columns:
        train_mean = train_summary.loc["mean", col]
        train_std = train_summary.loc["std", col]
        new_mean = new_data[col].mean()
        z = abs(new_mean - train_mean) / (train_std + 1e-8)
        if z > threshold:
            alerts.append((col, round(z, 2)))
    return alerts

print("Drift check on normal batch:", check_drift(normal_batch, train_summary))
print("Drift check on drifted batch:", check_drift(drifted_batch, train_summary))

# --- Step 5: Monitor prediction confidence over time (a proxy signal too) ---
def monitor_predictions(model, batch, label=""):
    preds = model.predict(batch)
    probas = model.predict_proba(batch).max(axis=1)
    print(f"[{label}] avg confidence: {probas.mean():.3f}, min confidence: {probas.min():.3f}")

monitor_predictions(model, normal_batch, "normal batch")
monitor_predictions(model, drifted_batch, "drifted batch")

# --- Step 6: Decide whether to retrain (simple rule-based trigger) ---
def should_retrain(alerts, min_confidence, confidence_threshold=0.6):
    return len(alerts) > 0 or min_confidence < confidence_threshold

drift_alerts = check_drift(drifted_batch, train_summary)
min_conf = model.predict_proba(drifted_batch).max(axis=1).min()
print("Should retrain?", should_retrain(drift_alerts, min_conf))
```

## Exercise
1. Wire up the FastAPI app for real (`pip install fastapi uvicorn`), run it locally, and send it a test request with `curl` or `requests.post`.
2. Containerize the API with a `Dockerfile` (module 15-004) and confirm it runs the same way inside the container.
3. Extend `should_retrain` into a small scheduled job (pseudocode is fine) that would run daily, check drift, and print an alert if retraining is needed.

## Key Takeaways
- "Deploying a model" really means: save it in a reusable format, serve it behind an API, and keep watching it — training is the easy 20%.
- Feature drift (a distribution shift on the input side) is one of the most common causes of quiet production model decay.
- A simple z-score-based drift check, run regularly against a stored training summary, catches a large fraction of real-world problems without needing fancy tooling.
