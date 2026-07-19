# 003 - Boosting: AdaBoost

## Concept
Boosting builds models sequentially, where each new model focuses on the mistakes of the previous ones. AdaBoost (Adaptive Boosting) does this by increasing the sample weight of misclassified points after each round, forcing the next weak learner to pay more attention to them.

## Why It Matters
Boosting trades the "average many independent models" idea of bagging for "chain together models that correct each other's mistakes." It generally achieves lower bias than bagging, at the cost of being more sensitive to noisy data and outliers.

## Hands-On

```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score

X, y = make_classification(n_samples=1000, n_features=20, n_informative=10, random_state=42)
y = np.where(y == 0, -1, 1)  # AdaBoost math is cleanest with {-1, +1} labels
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 1. sklearn's AdaBoost with decision stumps (depth-1 trees) as weak learners
ada = AdaBoostClassifier(
    estimator=DecisionTreeClassifier(max_depth=1),
    n_estimators=100,
    learning_rate=1.0,
    random_state=42,
)
ada.fit(X_train, y_train)
print("AdaBoost accuracy:", accuracy_score(y_test, ada.predict(X_test)))

# 2. AdaBoost from scratch - illustrates the reweighting mechanism
def adaboost_from_scratch(X, y, n_estimators=20):
    n = len(y)
    weights = np.ones(n) / n
    stumps, alphas = [], []

    for t in range(n_estimators):
        stump = DecisionTreeClassifier(max_depth=1)
        stump.fit(X, y, sample_weight=weights)
        pred = stump.predict(X)

        err = np.sum(weights * (pred != y)) / np.sum(weights)
        err = np.clip(err, 1e-10, 1 - 1e-10)  # avoid log(0)
        alpha = 0.5 * np.log((1 - err) / err)   # stump's "vote strength"

        weights *= np.exp(-alpha * y * pred)    # up-weight mistakes, down-weight correct
        weights /= weights.sum()                # renormalize

        stumps.append(stump)
        alphas.append(alpha)

    return stumps, alphas

def adaboost_predict(stumps, alphas, X):
    agg = sum(a * s.predict(X) for s, a in zip(stumps, alphas))
    return np.sign(agg)

stumps, alphas = adaboost_from_scratch(X_train, y_train, n_estimators=50)
scratch_preds = adaboost_predict(stumps, alphas, X_test)
print("Scratch AdaBoost accuracy:", accuracy_score(y_test, scratch_preds))

# 3. Show how a single stump alone performs (should be much worse - AdaBoost's whole point)
weak_stump = DecisionTreeClassifier(max_depth=1)
weak_stump.fit(X_train, y_train)
print("Single stump accuracy:", accuracy_score(y_test, weak_stump.predict(X_test)))
```

## Exercise
1. Plot test accuracy vs. `n_estimators` (1 to 200) — does AdaBoost overfit as rounds increase?
2. Inject 5% label noise into `y_train` and compare AdaBoost's accuracy drop to Random Forest's — AdaBoost is known to be noise-sensitive.
3. Print the `alphas` from the from-scratch version — which rounds contributed the most "voting power"?

## Key Takeaways
- AdaBoost combines many "weak learners" (barely better than random) into one strong learner via weighted voting.
- Misclassified points get exponentially more weight each round — this is both AdaBoost's strength and its Achilles' heel (outlier sensitivity).
- `learning_rate` shrinks each stump's contribution — lower values need more estimators but often generalize better.
