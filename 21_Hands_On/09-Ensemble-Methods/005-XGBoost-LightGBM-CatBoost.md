# 005 - XGBoost, LightGBM, and CatBoost

## Concept
These are three production-grade, highly optimized gradient boosting libraries. They share the core gradient boosting idea but differ in tree-growth strategy, speed, and how they handle categorical features.

| Library  | Tree growth        | Categorical handling      | Notable strength           |
|----------|--------------------|----------------------------|-----------------------------|
| XGBoost  | Level-wise          | Needs manual encoding      | Regularization, wide adoption |
| LightGBM | Leaf-wise (best-first) | Native categorical support | Speed on large datasets     |
| CatBoost | Symmetric (oblivious) trees | Best native categorical handling | Handles categoricals with minimal tuning |

## Why It Matters
These libraries win the overwhelming majority of tabular-data Kaggle competitions and are the default choice in industry for structured/tabular problems — often outperforming deep learning on this data type.

## Hands-On

```python
# pip install xgboost lightgbm catboost --break-system-packages
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

data = fetch_california_housing()
X, y = pd.DataFrame(data.data, columns=data.feature_names), data.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 1. XGBoost
import xgboost as xgb

xgb_model = xgb.XGBRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    reg_alpha=0.1,        # L1 regularization
    reg_lambda=1.0,       # L2 regularization
    early_stopping_rounds=20,
    eval_metric="rmse",
    random_state=42,
)
xgb_model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)
print("XGBoost RMSE:", mean_squared_error(y_test, xgb_model.predict(X_test)) ** 0.5)

# 2. LightGBM
import lightgbm as lgb

lgb_model = lgb.LGBMRegressor(
    n_estimators=500,
    learning_rate=0.05,
    num_leaves=31,        # controls model complexity in leaf-wise growth
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    verbosity=-1,
)
lgb_model.fit(X_train, y_train)
print("LightGBM RMSE:", mean_squared_error(y_test, lgb_model.predict(X_test)) ** 0.5)

# 3. CatBoost
from catboost import CatBoostRegressor

cat_model = CatBoostRegressor(
    iterations=500,
    learning_rate=0.05,
    depth=6,
    random_state=42,
    verbose=0,
)
cat_model.fit(X_train, y_train)
print("CatBoost RMSE:", mean_squared_error(y_test, cat_model.predict(X_test)) ** 0.5)

# 4. Feature importance comparison
importances = pd.DataFrame({
    "feature": X.columns,
    "xgboost": xgb_model.feature_importances_,
    "lightgbm": lgb_model.feature_importances_ / lgb_model.feature_importances_.sum(),
    "catboost": cat_model.feature_importances_ / 100,
}).sort_values("xgboost", ascending=False)
print(importances)
```

## Exercise
1. Create a dataset with a categorical column (e.g., `pd.cut` on a numeric feature into bins) and pass it directly to CatBoost using `cat_features=[...]` — compare against one-hot-encoding it for XGBoost.
2. Use `early_stopping_rounds` with a validation set on all three libraries and compare how many rounds each needed.
3. Benchmark training time (`%timeit` or `time.time()`) for all three on a dataset with 100k+ rows — which is fastest?

## Key Takeaways
- All three beat plain `GradientBoostingRegressor` in speed due to histogram-based splitting and other optimizations.
- CatBoost is the best default when you have many categorical columns and don't want to hand-engineer encodings.
- LightGBM's leaf-wise growth can overfit on small datasets faster than XGBoost's level-wise growth — watch `num_leaves` and `max_depth` together.
