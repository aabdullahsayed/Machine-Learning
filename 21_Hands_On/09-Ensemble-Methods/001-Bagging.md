# 001 - Bagging

## Concept
Bagging (Bootstrap AGGregatING) trains many copies of the same model on different random bootstrap samples of the training data, then averages (regression) or votes (classification) their predictions. It reduces variance without increasing bias much.

## Why It Matters
Bagging is the mathematical foundation of Random Forest (next lesson) and is a general recipe you can apply to any high-variance model, not just trees.

## Hands-On

```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.metrics import accuracy_score

X, y = make_classification(n_samples=1000, n_features=20, n_informative=10,
                            random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 1. Baseline: a single, deep (overfit-prone) decision tree
single_tree = DecisionTreeClassifier(random_state=42)
single_tree.fit(X_train, y_train)
print("Single tree accuracy:", accuracy_score(y_test, single_tree.predict(X_test)))

# 2. Bagging: 100 trees, each trained on a bootstrap sample
bagged = BaggingClassifier(
    estimator=DecisionTreeClassifier(),
    n_estimators=100,
    max_samples=1.0,      # sample size == training set size (with replacement)
    bootstrap=True,
    random_state=42,
    n_jobs=-1,
)
bagged.fit(X_train, y_train)
print("Bagged accuracy:", accuracy_score(y_test, bagged.predict(X_test)))

# 3. Implement bagging from scratch to see the mechanism
def bagging_from_scratch(X_train, y_train, X_test, n_estimators=50):
    n = len(X_train)
    all_preds = []
    for i in range(n_estimators):
        idx = np.random.choice(n, size=n, replace=True)   # bootstrap sample
        X_sample, y_sample = X_train[idx], y_train[idx]
        tree = DecisionTreeClassifier(random_state=i)
        tree.fit(X_sample, y_sample)
        all_preds.append(tree.predict(X_test))
    all_preds = np.array(all_preds)                        # shape (n_estimators, n_test)
    majority_vote = np.round(all_preds.mean(axis=0)).astype(int)
    return majority_vote

scratch_preds = bagging_from_scratch(X_train, y_train, X_test)
print("Scratch bagging accuracy:", accuracy_score(y_test, scratch_preds))
```

## Exercise
1. Vary `n_estimators` from 1 to 200 and plot test accuracy — where does it plateau?
2. Try `max_samples=0.5` (each tree sees only half the data) — how does variance vs. accuracy trade off?
3. Compute out-of-bag (OOB) accuracy using `oob_score=True` and compare it to the held-out test accuracy.

## Key Takeaways
- Bagging works best with high-variance, low-bias base learners (deep trees are ideal; a linear model would barely benefit).
- Each bootstrap sample leaves out ~37% of the data on average — these "out-of-bag" points give a free validation estimate.
- Bagging reduces variance, not bias — if your single model underfits, bagging won't fix that.
