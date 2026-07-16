# 001 - Capstone: End-to-End Tabular ML Pipeline

## Concept
This capstone walks through a complete, beginner-friendly tabular ML project from raw data to a saved, reusable model: load data → clean it → engineer features → train several models → pick the best one → save it. Nothing fancy — just every step done properly, in order.

## Why It Matters
Most real ML jobs are tabular data problems (spreadsheets, databases, CSVs), not deep learning. Being able to run this exact pipeline confidently, end to end, is the single most useful skill from this whole course.

## Hands-On

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# --- Step 1: Load data ---
from sklearn.datasets import load_breast_cancer
data = load_breast_cancer()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = pd.Series(data.target, name="diagnosis")

print("Shape:", X.shape)
print(X.head())

# --- Step 2: Clean data (check for missing values) ---
print("Missing values:", X.isnull().sum().sum())  # 0 here, but always check

# --- Step 3: Train/test split ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# --- Step 4: Build a pipeline (scaling + model bundled together) ---
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000)),
])

# --- Step 5: Cross-validate to get an honest performance estimate ---
cv_scores = cross_val_score(pipeline, X_train, y_train, cv=5)
print(f"Cross-val accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

# --- Step 6: Compare a couple of candidate models ---
candidates = {
    "LogisticRegression": Pipeline([("scaler", StandardScaler()), ("model", LogisticRegression(max_iter=1000))]),
    "RandomForest": Pipeline([("scaler", StandardScaler()), ("model", RandomForestClassifier(n_estimators=200, random_state=42))]),
}

for name, pipe in candidates.items():
    scores = cross_val_score(pipe, X_train, y_train, cv=5)
    print(f"{name}: {scores.mean():.4f}")

# --- Step 7: Fit the winning model on the full training set ---
best_pipeline = candidates["RandomForest"]
best_pipeline.fit(X_train, y_train)

# --- Step 8: Evaluate on the held-out test set (only once!) ---
y_pred = best_pipeline.predict(X_test)
print("Test accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# --- Step 9: Save the trained pipeline for reuse ---
joblib.dump(best_pipeline, "trained_model.pkl")
print("Model saved to trained_model.pkl")

# --- Step 10: Load it back and predict on new data ---
loaded_model = joblib.load("trained_model.pkl")
sample = X_test.iloc[[0]]
print("Prediction on one sample:", loaded_model.predict(sample))
```

## Exercise
1. Swap in a real CSV of your own (or one from Kaggle) instead of `load_breast_cancer` and repeat every step.
2. Add a third candidate model (e.g., `GradientBoostingClassifier`) to the comparison loop.
3. Write a small `predict_new(csv_path)` function that loads `trained_model.pkl` and returns predictions for a new CSV file.

## Key Takeaways
- The order matters: split first, then fit any scaler/encoder only on training data, to avoid data leakage (module 02-006).
- A `Pipeline` bundles preprocessing and the model together so you can't accidentally apply them out of order or forget a step at prediction time.
- Saving with `joblib` (or `pickle`) is what lets a trained model be reused later without retraining — the first step toward deployment (module 15).
