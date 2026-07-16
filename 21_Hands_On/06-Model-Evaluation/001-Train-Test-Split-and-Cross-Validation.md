# 001 - Train-Test Split and Cross-Validation

## Concept
A single train-test split gives one noisy performance estimate. **K-Fold Cross-Validation** trains and evaluates the model K times on different folds, giving a more robust, averaged estimate with a measure of variance. This lesson also covers Stratified K-Fold and time-series-safe cross-validation.

## Why It Matters
Every model comparison and hyperparameter choice in this course (modules 04, 05, 09) should be driven by cross-validation, not a single lucky/unlucky split.

## Hands-On

```python
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import (
    KFold, StratifiedKFold, TimeSeriesSplit, cross_val_score, cross_validate
)
from sklearn.linear_model import LogisticRegression

X, y = make_classification(n_samples=500, n_features=10, weights=[0.9, 0.1], random_state=42)

# 1. Single train-test split - one noisy estimate
from sklearn.model_selection import train_test_split
scores_single = []
for seed in range(5):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=seed)
    model = LogisticRegression(max_iter=1000).fit(X_train, y_train)
    scores_single.append(model.score(X_test, y_test))
print("Single-split accuracies across 5 different random seeds:", np.round(scores_single, 4))
print("-> notice the variability: a single split's score is unreliable.")

# 2. K-Fold cross-validation - more stable estimate
kfold = KFold(n_splits=5, shuffle=True, random_state=42)
model = LogisticRegression(max_iter=1000)
cv_scores = cross_val_score(model, X, y, cv=kfold, scoring="accuracy")
print(f"\n5-Fold CV accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
print("Individual fold scores:", np.round(cv_scores, 4))

# 3. Stratified K-Fold - preserves class balance in every fold (crucial here,
# since this dataset is imbalanced 90/10)
skfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores_strat = cross_val_score(model, X, y, cv=skfold, scoring="accuracy")
print(f"\nStratified 5-Fold CV accuracy: {cv_scores_strat.mean():.4f} (+/- {cv_scores_strat.std():.4f})")

for i, (train_idx, test_idx) in enumerate(skfold.split(X, y)):
    fold_balance = y[test_idx].mean()
    print(f"  Fold {i}: test set positive-class ratio = {fold_balance:.3f}")

# 4. cross_validate - get multiple metrics at once, plus timing
results = cross_validate(
    model, X, y, cv=skfold,
    scoring=["accuracy", "precision", "recall", "f1", "roc_auc"]
)
for metric in ["accuracy", "precision", "recall", "f1", "roc_auc"]:
    print(f"{metric:10s}: {results[f'test_{metric}'].mean():.4f}")

# 5. TimeSeriesSplit - for time-ordered data (module 02, file 005), where
# random shuffling would leak future information into training folds
tscv = TimeSeriesSplit(n_splits=5)
X_time = np.arange(100).reshape(-1, 1)
y_time = np.random.choice([0, 1], 100)
print("\nTimeSeriesSplit fold boundaries (train size grows, test is always future):")
for i, (train_idx, test_idx) in enumerate(tscv.split(X_time)):
    print(f"  Fold {i}: train=[0:{train_idx[-1]}], test=[{test_idx[0]}:{test_idx[-1]}]")
```

## Exercise
1. Compare 5-fold vs 10-fold CV mean and standard deviation on the same dataset — does more folds reduce variance of the estimate?
2. Deliberately use plain `KFold` (not stratified) on this imbalanced dataset and inspect the per-fold positive-class ratio — how much does it vary compared to `StratifiedKFold`?
3. Use `TimeSeriesSplit` with a real or simulated time-ordered dataset and confirm no fold's test set ever precedes its train set.

## Key Takeaways
- Cross-validation gives both a performance estimate AND a variance estimate — always report both (mean +/- std).
- Always use `StratifiedKFold` for classification with class imbalance.
- Use `TimeSeriesSplit` (never random shuffling) whenever your data has a temporal order.
