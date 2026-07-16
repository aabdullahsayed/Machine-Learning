# 005 - Hyperparameter Tuning: GridSearch & RandomSearch

## Concept
Hyperparameters (like `alpha`, `max_depth`, `C`, `k`) aren't learned from data — they're set before training and control model complexity/behavior. **GridSearchCV** exhaustively tries every combination; **RandomizedSearchCV** samples a fixed number of random combinations, often finding near-optimal settings much faster for high-dimensional search spaces.

## Why It Matters
This lesson formalizes the tuning step used informally throughout modules 04-05, and connects cross-validation (file 001) with model selection into one robust workflow.

## Hands-On

```python
import numpy as np
from scipy.stats import randint, uniform
from sklearn.datasets import make_classification
from sklearn.model_selection import (
    train_test_split, GridSearchCV, RandomizedSearchCV, StratifiedKFold
)
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import time

X, y = make_classification(n_samples=800, n_features=15, n_informative=8, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# 1. GridSearchCV - exhaustive search over a small, discrete grid
param_grid = {
    "n_estimators": [50, 100, 200],
    "max_depth": [3, 5, 10, None],
    "min_samples_leaf": [1, 5, 10],
}
print(f"Grid size: {3 * 4 * 3} = 36 combinations x 5 folds = 180 fits")

start = time.time()
grid_search = GridSearchCV(
    RandomForestClassifier(random_state=42), param_grid,
    cv=cv, scoring="roc_auc", n_jobs=-1
)
grid_search.fit(X_train, y_train)
grid_time = time.time() - start

print(f"\nGridSearchCV best params: {grid_search.best_params_}")
print(f"GridSearchCV best CV score: {grid_search.best_score_:.4f}")
print(f"GridSearchCV time: {grid_time:.2f}s")

# 2. RandomizedSearchCV - samples a fixed budget of combinations from
# distributions, scales much better to large/continuous search spaces
param_distributions = {
    "n_estimators": randint(50, 300),
    "max_depth": randint(3, 20),
    "min_samples_leaf": randint(1, 15),
    "max_features": uniform(0.3, 0.7),
}

start = time.time()
random_search = RandomizedSearchCV(
    RandomForestClassifier(random_state=42), param_distributions,
    n_iter=30, cv=cv, scoring="roc_auc", random_state=42, n_jobs=-1
)
random_search.fit(X_train, y_train)
random_time = time.time() - start

print(f"\nRandomizedSearchCV best params: {random_search.best_params_}")
print(f"RandomizedSearchCV best CV score: {random_search.best_score_:.4f}")
print(f"RandomizedSearchCV time: {random_time:.2f}s (only 30 x 5 = 150 fits, "
      f"but covers a MUCH larger/continuous space)")

# 3. Inspect all results, not just the best - useful for understanding
# sensitivity to each hyperparameter
import pandas as pd
results_df = pd.DataFrame(grid_search.cv_results_)
top5 = results_df.sort_values("mean_test_score", ascending=False)[
    ["params", "mean_test_score", "std_test_score"]
].head(5)
print("\nTop 5 grid search configurations:\n", top5)

# 4. Final evaluation with the best found model, on the held-out test set
best_model = random_search.best_estimator_
test_score = best_model.score(X_test, y_test)
print(f"\nFinal test accuracy with best model: {test_score:.4f}")

# 5. Nested cross-validation - the gold standard when you need an UNBIASED
# estimate of generalization performance for the whole tuning process itself
from sklearn.model_selection import cross_val_score
nested_scores = cross_val_score(
    GridSearchCV(RandomForestClassifier(random_state=42),
                 {"n_estimators": [50, 100], "max_depth": [5, 10]},
                 cv=3, scoring="roc_auc"),
    X, y, cv=3, scoring="roc_auc"
)
print(f"\nNested CV score (unbiased estimate): {nested_scores.mean():.4f} "
      f"(+/- {nested_scores.std():.4f})")
```

## Exercise
1. Run `GridSearchCV` and `RandomizedSearchCV` with the same total fit budget (e.g., both around 150 fits) and compare their best CV scores — which found a better configuration?
2. Explain why `grid_search.best_score_` (a cross-validated score) is generally a fairer estimate than fitting once on all of `X_train` and checking training accuracy.
3. Explain in your own words why "nested" cross-validation is needed if you want to report an honest performance number for a process that *includes* hyperparameter tuning.

## Key Takeaways
- GridSearchCV guarantees finding the best combination within your specified grid, but scales exponentially with the number of hyperparameters.
- RandomizedSearchCV scales linearly with the search budget you set (`n_iter`) and often finds comparably good results much faster.
- Never tune hyperparameters using the test set — always tune via cross-validation on the training set, and touch the test set only once at the end (as established in module 02, file 005 and module 04, file 005).
