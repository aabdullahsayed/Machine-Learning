# 003 - Feature Selection

## Concept
Feature selection reduces the number of input features by keeping only the most informative ones. Methods fall into three families: **Filter** (statistical tests, independent of any model), **Wrapper** (uses model performance to greedily add/remove features, e.g., Recursive Feature Elimination), and **Embedded** (feature importance built into the model itself, like Lasso or tree-based importances).

## Why It Matters
Fewer, better features reduce overfitting risk, training time, and improve interpretability — directly connects to Lasso's automatic selection (module 04, file 004) and tree feature importances (module 05, file 003).

## Hands-On

```python
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.feature_selection import (
    SelectKBest, f_classif, mutual_info_classif, RFE, SelectFromModel
)
from sklearn.linear_model import LogisticRegression, Lasso
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score

# Dataset with 5 informative features and 15 pure-noise features
X, y = make_classification(n_samples=500, n_features=20, n_informative=5,
                            n_redundant=0, n_repeated=0, random_state=42)
feature_names = [f"feature_{i}" for i in range(20)]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 1. FILTER method - univariate statistical test (ANOVA F-value), fast,
# model-agnostic, but ignores feature interactions
selector_f = SelectKBest(score_func=f_classif, k=5)
X_train_f = selector_f.fit_transform(X_train, y_train)
selected_f = np.array(feature_names)[selector_f.get_support()]
print("SelectKBest (F-test) chose:", list(selected_f))

# 2. FILTER method - mutual information, captures nonlinear relationships too
selector_mi = SelectKBest(score_func=mutual_info_classif, k=5)
X_train_mi = selector_mi.fit_transform(X_train, y_train)
selected_mi = np.array(feature_names)[selector_mi.get_support()]
print("SelectKBest (mutual info) chose:", list(selected_mi))

# 3. WRAPPER method - Recursive Feature Elimination (RFE): repeatedly fit a
# model, remove the least important feature, repeat
rfe_model = LogisticRegression(max_iter=1000)
rfe = RFE(estimator=rfe_model, n_features_to_select=5)
rfe.fit(X_train, y_train)
selected_rfe = np.array(feature_names)[rfe.support_]
print("\nRFE chose:", list(selected_rfe))
print("RFE feature ranking (1 = selected):", rfe.ranking_)

# 4. EMBEDDED method - Lasso's built-in zeroing of coefficients (module 04, file 004)
lasso_selector = SelectFromModel(Lasso(alpha=0.05), threshold="mean")
lasso_selector.fit(X_train, y_train)
selected_lasso = np.array(feature_names)[lasso_selector.get_support()]
print("\nLasso-based selection chose:", list(selected_lasso))

# 5. EMBEDDED method - tree-based feature importance (module 05, file 003)
rf_selector = SelectFromModel(RandomForestClassifier(n_estimators=100, random_state=42),
                               threshold="median")
rf_selector.fit(X_train, y_train)
selected_rf = np.array(feature_names)[rf_selector.get_support()]
print("\nRandom Forest importance-based selection chose:", list(selected_rf))

# 6. Does feature selection actually help? Compare CV performance
baseline_scores = cross_val_score(LogisticRegression(max_iter=1000), X_train, y_train, cv=5)
selected_scores = cross_val_score(LogisticRegression(max_iter=1000), X_train_f, y_train, cv=5)
print(f"\nAll 20 features CV accuracy: {baseline_scores.mean():.4f}")
print(f"Top 5 features CV accuracy:  {selected_scores.mean():.4f}")
print("Selecting only informative features often matches or beats using everything, "
      "while training faster and being more interpretable.")
```

## Exercise
1. Vary `k` in `SelectKBest` from 1 to 20 and plot CV accuracy vs `k` — find the point of diminishing/negative returns.
2. Compare the feature sets chosen by the F-test filter vs. RFE — how much overlap is there? Explain any differences using the fact that F-test ignores interactions.
3. Combine feature selection with `Pipeline` + `GridSearchCV` (module 06, file 005) so that `k` itself is tuned via cross-validation rather than fixed manually.

## Key Takeaways
- Filter methods are fast and model-agnostic but ignore feature interactions; wrapper methods (RFE) are slower but model-aware; embedded methods (Lasso, tree importances) get selection "for free" during training.
- Feature selection should always be validated via cross-validation performance, not assumed to help.
- Always perform feature selection using only the training fold — treat it as part of the model pipeline (module 02, file 006), not a separate pre-processing step done on the full dataset.
