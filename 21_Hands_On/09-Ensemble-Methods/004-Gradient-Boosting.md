# 004 - Gradient Boosting

## Concept
Gradient Boosting builds trees sequentially like AdaBoost, but instead of reweighting samples, each new tree is trained to predict the **residual errors** (negative gradient of the loss) of the ensemble so far. This generalizes boosting to any differentiable loss function.

## Why It Matters
Gradient Boosting is the algorithm family behind XGBoost, LightGBM, and CatBoost — the dominant approach for tabular data in Kaggle competitions and industry. Understanding the base algorithm makes those libraries much less mysterious.

## Hands-On

```python
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error

data = fetch_california_housing()
X, y = data.data, data.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 1. sklearn's Gradient Boosting
gbr = GradientBoostingRegressor(
    n_estimators=200,
    learning_rate=0.1,
    max_depth=3,
    random_state=42,
)
gbr.fit(X_train, y_train)
print("GBR RMSE:", mean_squared_error(y_test, gbr.predict(X_test)) ** 0.5)

# 2. Gradient boosting from scratch for squared-error loss (regression)
def gradient_boosting_from_scratch(X_train, y_train, X_test, n_estimators=100, lr=0.1, max_depth=3):
    # Start with a constant prediction: the mean
    pred_train = np.full(len(y_train), y_train.mean())
    pred_test = np.full(len(X_test), y_train.mean())
    trees = []

    for i in range(n_estimators):
        residuals = y_train - pred_train           # negative gradient for squared error
        tree = DecisionTreeRegressor(max_depth=max_depth)
        tree.fit(X_train, residuals)
        trees.append(tree)

        pred_train += lr * tree.predict(X_train)    # shrink each tree's contribution
        pred_test += lr * tree.predict(X_test)

    return pred_test

scratch_preds = gradient_boosting_from_scratch(X_train, y_train, X_test)
print("Scratch GB RMSE:", mean_squared_error(y_test, scratch_preds) ** 0.5)

# 3. Effect of learning_rate vs n_estimators trade-off
for lr, n in [(0.3, 50), (0.1, 150), (0.03, 500)]:
    model = GradientBoostingRegressor(learning_rate=lr, n_estimators=n, max_depth=3, random_state=42)
    model.fit(X_train, y_train)
    rmse = mean_squared_error(y_test, model.predict(X_test)) ** 0.5
    print(f"lr={lr}, n_estimators={n}: RMSE={rmse:.4f}")

# 4. Early stopping using a validation set (staged predictions)
X_tr, X_val, y_tr, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)
gbr_es = GradientBoostingRegressor(n_estimators=500, learning_rate=0.05, max_depth=3, random_state=42)
gbr_es.fit(X_tr, y_tr)

val_scores = [mean_squared_error(y_val, pred) for pred in gbr_es.staged_predict(X_val)]
best_n = np.argmin(val_scores) + 1
print(f"Best number of trees by validation: {best_n}")
```

## Exercise
1. Modify the from-scratch function to support a `subsample` parameter (train each tree on a random fraction of rows — this is "stochastic gradient boosting").
2. Plot training RMSE vs. test RMSE across `n_estimators` — at what point does the model start overfitting?
3. Swap `max_depth` between 1, 3, and 8 — how does tree depth interact with the number of estimators needed?

## Key Takeaways
- Gradient boosting fits each new tree to the *residual errors*, not to reweighted samples like AdaBoost.
- `learning_rate` and `n_estimators` are tightly coupled: lower learning rate needs more trees but usually generalizes better.
- Because it fits errors sequentially, gradient boosting is prone to overfitting without regularization (shallow trees, subsampling, early stopping).
