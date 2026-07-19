# 002 - Random Forest

## Concept
Random Forest is bagging plus one extra trick: at each split, only a random subset of features is considered. This decorrelates the trees so their errors don't all point the same direction, which improves the averaged result beyond plain bagging.

## Why It Matters
Random Forest is one of the most reliable "just works" algorithms for tabular data — strong baseline, resistant to overfitting, gives free feature importances, and needs almost no preprocessing (no scaling required).

## Hands-On

```python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import numpy as np
import matplotlib.pyplot as plt

data = load_breast_cancer()
X, y = data.data, data.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 1. Train a Random Forest
rf = RandomForestClassifier(
    n_estimators=300,
    max_depth=None,          # let trees grow fully; forest controls overfitting via averaging
    max_features="sqrt",     # the "random subset of features" trick
    oob_score=True,
    random_state=42,
    n_jobs=-1,
)
rf.fit(X_train, y_train)

print("OOB score:", rf.oob_score_)
print(classification_report(y_test, rf.predict(X_test)))

# 2. Feature importances - a major reason RF is popular for exploratory work
importances = pd.Series(rf.feature_importances_, index=data.feature_names)
importances.sort_values(ascending=False).head(10).plot(kind="barh")
plt.title("Top 10 Feature Importances")
plt.gca().invert_yaxis()
plt.savefig("rf_importances.png")
plt.close()

# 3. Compare max_features settings
for mf in ["sqrt", "log2", None]:
    rf_test = RandomForestClassifier(n_estimators=200, max_features=mf, random_state=42)
    rf_test.fit(X_train, y_train)
    print(f"max_features={mf}: test accuracy={rf_test.score(X_test, y_test):.4f}")

# 4. Visualize how accuracy changes with number of trees
import pandas as pd
n_trees_range = [1, 5, 10, 25, 50, 100, 200, 400]
scores = []
for n in n_trees_range:
    rf_n = RandomForestClassifier(n_estimators=n, random_state=42, n_jobs=-1)
    rf_n.fit(X_train, y_train)
    scores.append(rf_n.score(X_test, y_test))

plt.plot(n_trees_range, scores, marker="o")
plt.xlabel("n_estimators")
plt.ylabel("Test accuracy")
plt.title("Random Forest: accuracy vs number of trees")
plt.savefig("rf_ntrees.png")
```

## Exercise
1. Train a `RandomForestRegressor` on a regression dataset (e.g., `fetch_california_housing`) and compare R² to a single decision tree.
2. Use `permutation_importance` from `sklearn.inspection` and compare its ranking to `feature_importances_` — they can disagree, especially with correlated features.
3. Tune `max_depth`, `min_samples_leaf`, and `n_estimators` with `RandomizedSearchCV` and report the best combination.

## Key Takeaways
- `max_features="sqrt"` for classification and full features for regression are reasonable sklearn defaults, but tune them.
- OOB score gives a free, honest validation estimate without needing a separate validation set.
- Built-in `feature_importances_` can be biased toward high-cardinality features — permutation importance is often more trustworthy.
