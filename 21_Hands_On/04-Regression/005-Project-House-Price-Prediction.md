# 005 - Project: House Price Prediction

## Concept
This is a capstone-style project for the Regression module: an end-to-end pipeline combining EDA (module 02), feature engineering, model selection among Linear/Ridge/Lasso/Polynomial regression, and proper evaluation (module 06).

## Why It Matters
Real projects require chaining together everything learned so far into one coherent, leakage-free pipeline — this is the workflow you'll repeat, with different models, throughout the rest of the course.

## Hands-On

```python
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score

# 1. Load & quick EDA
housing = fetch_california_housing(as_frame=True)
df = housing.frame
print(df.describe())
print("\nMissing values:\n", df.isna().sum())
print("\nCorrelation with target:\n",
      df.corr(numeric_only=True)["MedHouseVal"].sort_values(ascending=False))

# 2. Feature engineering: create a couple of domain-informed ratio features
df["rooms_per_household"] = df["AveRooms"] / df["AveOccup"].replace(0, np.nan)
df["bedrooms_ratio"] = df["AveBedrms"] / df["AveRooms"].replace(0, np.nan)
df = df.fillna(df.median(numeric_only=True))

X = df.drop(columns=["MedHouseVal"])
y = df["MedHouseVal"]

# 3. Split FIRST, before any fitting (module 02, file 006)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Build leakage-safe pipelines for each candidate model
pipelines = {
    "Linear": Pipeline([
        ("scaler", StandardScaler()),
        ("model", LinearRegression())
    ]),
    "Ridge": Pipeline([
        ("scaler", StandardScaler()),
        ("model", Ridge(alpha=1.0))
    ]),
    "Lasso": Pipeline([
        ("scaler", StandardScaler()),
        ("model", Lasso(alpha=0.01))
    ]),
    "Polynomial+Ridge": Pipeline([
        ("scaler", StandardScaler()),
        ("poly", PolynomialFeatures(degree=2, include_bias=False)),
        ("model", Ridge(alpha=10.0))
    ]),
}

# 5. Compare candidates with cross-validation (module 06 preview)
print("\n--- Model comparison (5-fold CV, negative MSE) ---")
cv_results = {}
for name, pipe in pipelines.items():
    scores = cross_val_score(pipe, X_train, y_train, cv=5, scoring="neg_mean_squared_error")
    cv_results[name] = -scores.mean()
    print(f"{name:20s} -> CV MSE: {-scores.mean():.4f} (+/- {scores.std():.4f})")

best_name = min(cv_results, key=cv_results.get)
print(f"\nBest model by CV: {best_name}")

# 6. Hyperparameter tuning for the winning model
param_grid = {"model__alpha": [0.001, 0.01, 0.1, 1, 10, 100]}
grid = GridSearchCV(pipelines["Ridge"], param_grid, cv=5, scoring="neg_mean_squared_error")
grid.fit(X_train, y_train)
print(f"\nBest Ridge alpha: {grid.best_params_}, CV MSE: {-grid.best_score_:.4f}")

# 7. Final evaluation on the held-out test set (touched only ONCE, here)
final_model = grid.best_estimator_
y_pred = final_model.predict(X_test)
print(f"\nFinal Test MSE: {mean_squared_error(y_test, y_pred):.4f}")
print(f"Final Test R²: {r2_score(y_test, y_pred):.4f}")

# 8. Baseline sanity check
baseline_pred = np.full_like(y_test, y_train.mean())
print(f"Baseline (predict mean) MSE: {mean_squared_error(y_test, baseline_pred):.4f}")
print("Model beats baseline:", mean_squared_error(y_test, y_pred) < mean_squared_error(y_test, baseline_pred))
```

## Exercise
1. Add 2-3 more engineered features of your own (e.g., `population_per_household`) and re-run the comparison — did CV MSE improve?
2. Extend the `param_grid` to also search over `poly__degree` for the polynomial pipeline using `GridSearchCV`.
3. Write a short (5-bullet) final report: which model won, what its test R² means practically, and one concrete idea for further improvement (e.g., try Random Forest — module 09).

## Key Takeaways
- A real project is a *pipeline*: EDA → feature engineering → leakage-safe preprocessing → model comparison via CV → hyperparameter tuning → single final test evaluation.
- The test set should be touched exactly once, at the very end — everything else (model selection, tuning) happens via cross-validation on the training set.
- Comparing against a naive baseline (predict-the-mean) is a mandatory sanity check before declaring any model "good."
