# 003 - Decision Trees

## Concept
A decision tree recursively splits data based on feature thresholds that maximize "purity" of the resulting groups, measured by Gini impurity or entropy. It builds an interpretable, flowchart-like structure of if/else rules.

## Why It Matters
Decision trees are the building block for Random Forests and Gradient Boosting (module 09) — arguably the most powerful and widely used tabular-data models in practice.

## Hands-On

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score

# 1. Impurity measures - the criteria used to choose splits
def gini_impurity(y):
    _, counts = np.unique(y, return_counts=True)
    probabilities = counts / len(y)
    return 1 - np.sum(probabilities ** 2)

def entropy(y):
    _, counts = np.unique(y, return_counts=True)
    probabilities = counts / len(y)
    return -np.sum(probabilities * np.log2(probabilities + 1e-12))

pure_node = np.array([1, 1, 1, 1])
impure_node = np.array([1, 1, 0, 0])
mixed_node = np.array([1, 1, 1, 0])
for name, node in [("Pure", pure_node), ("50/50 mixed", impure_node), ("75/25 mixed", mixed_node)]:
    print(f"{name:12s} -> Gini: {gini_impurity(node):.3f}, Entropy: {entropy(node):.3f}")

# 2. How a split is chosen - information gain example
def information_gain(parent, left_child, right_child):
    n = len(parent)
    weight_left, weight_right = len(left_child) / n, len(right_child) / n
    return entropy(parent) - (weight_left * entropy(left_child) + weight_right * entropy(right_child))

parent = np.array([1, 1, 1, 0, 0, 0, 1, 0])
# Candidate split A produces a clean separation
left_a, right_a = np.array([1, 1, 1, 1]), np.array([0, 0, 0, 0])
# Candidate split B produces a poor separation
left_b, right_b = np.array([1, 1, 0, 0]), np.array([1, 0, 0, 1])
print(f"\nInformation gain (good split): {information_gain(parent, left_a, right_a):.4f}")
print(f"Information gain (bad split):  {information_gain(parent, left_b, right_b):.4f}")
print("-> The tree greedily picks the split with the highest information gain at each node.")

# 3. Fit sklearn's DecisionTreeClassifier
X, y = make_classification(n_samples=300, n_features=4, n_informative=3,
                            n_redundant=0, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

tree = DecisionTreeClassifier(max_depth=3, criterion="gini", random_state=42)
tree.fit(X_train, y_train)
print(f"\nDecision tree accuracy: {accuracy_score(y_test, tree.predict(X_test)):.4f}")

# 4. Visualize the tree structure - directly readable "rules"
plt.figure(figsize=(16, 8))
plot_tree(tree, filled=True, feature_names=[f"feat_{i}" for i in range(4)],
          class_names=["0", "1"], rounded=True, fontsize=9)
plt.savefig("decision_tree_structure.png", bbox_inches="tight")
plt.close()

# 5. Feature importance - how much each feature contributed to reducing impurity
importance_df = list(zip([f"feat_{i}" for i in range(4)], tree.feature_importances_))
print("\nFeature importances:", sorted(importance_df, key=lambda x: -x[1]))

# 6. Overfitting demo: unconstrained tree depth
for depth in [1, 3, 5, None]:
    t = DecisionTreeClassifier(max_depth=depth, random_state=42).fit(X_train, y_train)
    train_acc = accuracy_score(y_train, t.predict(X_train))
    test_acc = accuracy_score(y_test, t.predict(X_test))
    print(f"max_depth={str(depth):5s} -> Train acc: {train_acc:.3f}, Test acc: {test_acc:.3f}")
```

## Exercise
1. Compute Gini impurity vs Entropy for a node with class distribution [90%, 10%] and compare the two values — they should both be low but not identical.
2. Train trees with `min_samples_leaf` set to 1, 5, and 20 — how does this hyperparameter affect overfitting compared to `max_depth`?
3. Use `tree.feature_importances_` on a dataset with one clearly irrelevant (random noise) feature — confirm it receives near-zero importance.

## Key Takeaways
- Trees greedily choose the split (feature + threshold) that maximizes information gain (or minimizes Gini impurity) at each node.
- Unconstrained trees will grow until every leaf is pure — this almost always overfits; use `max_depth`, `min_samples_leaf`, or pruning to control it.
- A single tree's decision boundary is a set of axis-aligned rectangles — this is why ensembles of trees (module 09) are usually far more accurate than one tree alone.
