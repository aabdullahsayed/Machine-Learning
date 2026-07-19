# 006 - Project: Kaggle Tabular Competition Workflow

## Concept
This project simulates the end-to-end workflow used in a typical Kaggle tabular competition: EDA, feature engineering, cross-validated model comparison, ensembling, and generating a submission file.

## Why It Matters
Real competitions (and real jobs) rarely reward knowing one algorithm well — they reward a repeatable, disciplined workflow: solid cross-validation, careful feature engineering, and combining several models to squeeze out the last bit of performance.

## Hands-On

```python
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import KFold, cross_val_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge
import lightgbm as lgb
import xgboost as xgb

# 1. Load and prep data (standing in for a Kaggle train.csv)
data = fetch_california_housing()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = data.target

# 2. Feature engineering - domain-driven combinations
X["rooms_per_household"] = X["AveRooms"] / X["AveOccup"]
X["bedrooms_per_room"] = X["AveBedrms"] / X["AveRooms"]
X["population_per_household"] = X["Population"] / X["AveOccup"]

# 3. Set up a consistent cross-validation scheme - use the SAME folds for every model
kf = KFold(n_splits=5, shuffle=True, random_state=42)

def cv_rmse(model, X, y):
    scores = cross_val_score(model, X, y, cv=kf, scoring="neg_root_mean_squared_error")
    return -scores.mean(), scores.std()

models = {
    "Ridge": Ridge(alpha=1.0),
    "RandomForest": RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1),
    "GradientBoosting": GradientBoostingRegressor(n_estimators=200, random_state=42),
    "XGBoost": xgb.XGBRegressor(n_estimators=300, learning_rate=0.05, random_state=42),
    "LightGBM": lgb.LGBMRegressor(n_estimators=300, learning_rate=0.05, random_state=42, verbosity=-1),
}

results = {}
for name, model in models.items():
    mean_rmse, std_rmse = cv_rmse(model, X, y)
    results[name] = mean_rmse
    print(f"{name}: RMSE={mean_rmse:.4f} (+/- {std_rmse:.4f})")

# 4. Ensembling: average predictions from the top 3 models (a simple, robust technique)
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

top_models = [
    RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1),
    xgb.XGBRegressor(n_estimators=300, learning_rate=0.05, random_state=42),
    lgb.LGBMRegressor(n_estimators=300, learning_rate=0.05, random_state=42, verbosity=-1),
]

for m in top_models:
    m.fit(X_train, y_train)

ensemble_preds = np.mean([m.predict(X_test) for m in top_models], axis=0)
from sklearn.metrics import mean_squared_error
print("Ensemble RMSE:", mean_squared_error(y_test, ensemble_preds) ** 0.5)

# 5. Generate a "submission" file, as you would for Kaggle
submission = pd.DataFrame({"id": range(len(y_test)), "prediction": ensemble_preds})
submission.to_csv("submission.csv", index=False)
print(submission.head())
```

## Exercise
1. Add weighted averaging (e.g., weight by inverse CV RMSE) instead of a simple mean — does it beat the plain ensemble?
2. Implement a basic stacking model: train a `Ridge` meta-model on the out-of-fold predictions of the base models.
3. Add at least 3 more engineered features and re-run cross-validation — quantify the improvement.

## Key Takeaways
- Always evaluate every model on the **same** CV folds — otherwise comparisons are unfair.
- Simple averaging of diverse models (tree-based + linear) often beats any single model.
- Feature engineering typically gives a bigger boost than hyperparameter tuning in tabular competitions.
