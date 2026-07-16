# 005 - Support Vector Machines (SVM)

## Concept
SVMs find the hyperplane that maximizes the margin between classes. Points closest to the boundary ("support vectors") define it. The **kernel trick** lets SVMs learn nonlinear boundaries by implicitly mapping data into higher-dimensional space without ever computing that mapping explicitly.

## Why It Matters
SVMs were the state-of-the-art classifier before deep learning and remain excellent for small-to-medium, high-dimensional datasets (like text or bioinformatics data).

## Hands-On

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification, make_circles
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# 1. Linear SVM on linearly separable data - visualize the margin
X, y = make_classification(n_samples=100, n_features=2, n_redundant=0,
                            n_clusters_per_class=1, class_sep=2.0, random_state=42)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

linear_svm = SVC(kernel="linear", C=1.0)
linear_svm.fit(X_scaled, y)
print("Support vectors count:", len(linear_svm.support_vectors_), "out of", len(X))

# Plot decision boundary + margin
def plot_svm_boundary(model, X, y, title, filename):
    xx, yy = np.meshgrid(
        np.linspace(X[:, 0].min() - 1, X[:, 0].max() + 1, 300),
        np.linspace(X[:, 1].min() - 1, X[:, 1].max() + 1, 300)
    )
    Z = model.decision_function(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
    plt.figure(figsize=(7, 6))
    plt.contourf(xx, yy, Z > 0, alpha=0.3, cmap="RdBu")
    plt.contour(xx, yy, Z, levels=[-1, 0, 1], colors="k",
                linestyles=["--", "-", "--"], linewidths=1)
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap="RdBu", edgecolor="k")
    if hasattr(model, "support_vectors_"):
        plt.scatter(model.support_vectors_[:, 0], model.support_vectors_[:, 1],
                    s=150, facecolors="none", edgecolors="green", linewidths=2,
                    label="Support Vectors")
    plt.legend()
    plt.title(title)
    plt.savefig(filename)
    plt.close()

plot_svm_boundary(linear_svm, X_scaled, y, "Linear SVM with Margin", "svm_linear_margin.png")

# 2. The C hyperparameter - controls margin softness (regularization)
for C in [0.01, 1, 100]:
    svm_c = SVC(kernel="linear", C=C).fit(X_scaled, y)
    print(f"C={C}: {len(svm_c.support_vectors_)} support vectors "
          f"(smaller C -> wider margin -> more support vectors, more tolerance for violations)")

# 3. Kernel trick on non-linearly-separable data
X_circles, y_circles = make_circles(n_samples=200, noise=0.1, factor=0.4, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X_circles, y_circles, test_size=0.3, random_state=42)

# Linear kernel FAILS on this data
linear_fail = SVC(kernel="linear").fit(X_train, y_train)
print(f"\nLinear kernel on circles: {accuracy_score(y_test, linear_fail.predict(X_test)):.4f} accuracy")

# RBF (Gaussian) kernel handles it easily via the kernel trick
rbf_svm = SVC(kernel="rbf", gamma="scale").fit(X_train, y_train)
print(f"RBF kernel on circles:    {accuracy_score(y_test, rbf_svm.predict(X_test)):.4f} accuracy")

plot_svm_boundary(rbf_svm, X_circles, y_circles, "RBF Kernel SVM", "svm_rbf_circles.png")

# 4. Effect of gamma (RBF kernel width)
for gamma in [0.1, 1, 10]:
    g_svm = SVC(kernel="rbf", gamma=gamma).fit(X_train, y_train)
    acc = accuracy_score(y_test, g_svm.predict(X_test))
    print(f"gamma={gamma}: accuracy={acc:.4f} "
          f"(higher gamma -> tighter fit around individual points -> risk of overfitting)")
```

## Exercise
1. Try `kernel="poly"` with `degree=3` on the circles dataset — how does it compare to RBF?
2. Grid-search over `C` in `[0.01, 0.1, 1, 10, 100]` and `gamma` in `["scale", 0.01, 0.1, 1]` for the RBF SVM using `GridSearchCV`.
3. Explain in your own words why increasing `C` risks overfitting (hint: it forces the margin to allow fewer violations, fitting training points more tightly).

## Key Takeaways
- SVMs maximize the margin between classes; only the "support vectors" (points nearest the boundary) matter for the final decision.
- The kernel trick lets a linear algorithm learn nonlinear boundaries — RBF is the most common nonlinear kernel choice.
- `C` and `gamma` are the two critical hyperparameters, both controlling the same underlying tradeoff: model flexibility vs. generalization.
