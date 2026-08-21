"""
09 - Supervised Learning Algorithms, from scratch AND with scikit-learn
=========================================================================
Covers, on the two accompanying demo datasets:

  Regression dataset (10_regression_dataset.csv):
    - Linear Regression (from-scratch + sklearn)
    - Generalized Linear Model / Poisson-style example (sklearn)

  Classification dataset (11_classification_dataset.csv):
    - Logistic Regression (from-scratch + sklearn)
    - Decision Tree
    - Support Vector Machine (SVM)
    - k-Nearest Neighbors (k-NN)

Run:
    python 09_python_implementations.py

Requires: numpy, scikit-learn (falls back gracefully / synthesizes data
if the CSVs aren't found, so this script also runs standalone).
"""

import os
import csv
import numpy as np


# ----------------------------------------------------------------------
# 0. Helpers to load the two demo datasets
# ----------------------------------------------------------------------
def load_csv(filename, feature_cols, label_col):
    path = os.path.join(os.path.dirname(__file__), filename)
    X, y = [], []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                X.append([float(row[c]) for c in feature_cols])
                y.append(float(row[label_col]))
            except (ValueError, KeyError, TypeError):
                continue
    return np.array(X), np.array(y)


def train_test_split(X, y, test_frac=0.2, seed=0):
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(X))
    n_test = int(len(X) * test_frac)
    test_idx, train_idx = idx[:n_test], idx[n_test:]
    return X[train_idx], X[test_idx], y[train_idx], y[test_idx]


def standardize(X_train, X_test):
    mu, sigma = X_train.mean(axis=0), X_train.std(axis=0)
    sigma[sigma == 0] = 1.0
    return (X_train - mu) / sigma, (X_test - mu) / sigma


# ========================================================================
# PART A — REGRESSION  (dataset: sqft, bedrooms, age_years -> price)
# ========================================================================
print("=" * 70)
print("PART A: REGRESSION  (predicting house price)")
print("=" * 70)

Xr, yr = load_csv(
    "10_regression_dataset.csv",
    feature_cols=["sqft", "bedrooms", "age_years"],
    label_col="price",
)
Xr_train, Xr_test, yr_train, yr_test = train_test_split(Xr, yr, seed=1)
Xr_train_s, Xr_test_s = standardize(Xr_train, Xr_test)


# --- A1. Linear Regression from scratch (batch gradient descent) -------
def fit_linear_regression_gd(X, y, alpha=0.1, n_iter=2000):
    m, n = X.shape
    Xb = np.hstack([np.ones((m, 1)), X])          # add bias column
    theta = np.zeros(n + 1)
    for _ in range(n_iter):
        preds = Xb @ theta
        grad = (Xb.T @ (preds - y)) / m
        theta -= alpha * grad
    return theta


def predict_linear(theta, X):
    Xb = np.hstack([np.ones((len(X), 1)), X])
    return Xb @ theta


theta = fit_linear_regression_gd(Xr_train_s, yr_train)
preds_scratch = predict_linear(theta, Xr_test_s)
rmse_scratch = np.sqrt(np.mean((preds_scratch - yr_test) ** 2))
print(f"\n[From scratch] Linear Regression (gradient descent)")
print(f"  theta (bias, sqft, bedrooms, age) = {np.round(theta, 2)}")
print(f"  Test RMSE = {rmse_scratch:,.2f}")

# --- A2. Linear Regression with scikit-learn ----------------------------
try:
    from sklearn.linear_model import LinearRegression, PoissonRegressor
    from sklearn.metrics import mean_squared_error, r2_score

    lr = LinearRegression().fit(Xr_train, yr_train)
    preds_sklearn = lr.predict(Xr_test)
    rmse_sklearn = np.sqrt(mean_squared_error(yr_test, preds_sklearn))
    print(f"\n[scikit-learn] LinearRegression")
    print(f"  coefficients (sqft, bedrooms, age) = {np.round(lr.coef_, 2)}")
    print(f"  intercept = {lr.intercept_:.2f}")
    print(f"  Test RMSE = {rmse_sklearn:,.2f}   R^2 = {r2_score(yr_test, preds_sklearn):.3f}")

    # --- A3. GLM example: Poisson regression (treat price/1000 as a "count"-like demo) ---
    # (Illustrative only -- Poisson is meant for true count data; shown here
    #  purely to demonstrate the GLM API / log-link mechanics from file 08.)
    y_counts_like = np.round(yr_train / 5000).astype(float)  # pretend "counts"
    y_counts_test = np.round(yr_test / 5000).astype(float)
    pr = PoissonRegressor(max_iter=500).fit(Xr_train_s, y_counts_like)
    preds_pr = pr.predict(Xr_test_s)
    print(f"\n[scikit-learn] PoissonRegressor (GLM w/ log link, illustrative demo)")
    print(f"  Test RMSE (on pseudo-count target) = "
          f"{np.sqrt(mean_squared_error(y_counts_test, preds_pr)):.3f}")
except ImportError:
    print("\n(scikit-learn not installed - skipping sklearn regression demos)")


# ========================================================================
# PART B — CLASSIFICATION (dataset: tumor_size_cm, cell_irregularity -> malignant)
# ========================================================================
print("\n" + "=" * 70)
print("PART B: CLASSIFICATION  (predicting malignant tumor: 0/1)")
print("=" * 70)

Xc, yc = load_csv(
    "11_classification_dataset.csv",
    feature_cols=["tumor_size_cm", "cell_irregularity"],
    label_col="malignant",
)
Xc_train, Xc_test, yc_train, yc_test = train_test_split(Xc, yc, seed=2)
Xc_train_s, Xc_test_s = standardize(Xc_train, Xc_test)


# --- B1. Logistic Regression from scratch (batch gradient descent) -----
def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


def fit_logistic_regression_gd(X, y, alpha=0.5, n_iter=3000):
    m, n = X.shape
    Xb = np.hstack([np.ones((m, 1)), X])
    theta = np.zeros(n + 1)
    for _ in range(n_iter):
        preds = sigmoid(Xb @ theta)
        grad = (Xb.T @ (preds - y)) / m
        theta -= alpha * grad
    return theta


def predict_logistic(theta, X, threshold=0.5):
    Xb = np.hstack([np.ones((len(X), 1)), X])
    probs = sigmoid(Xb @ theta)
    return (probs >= threshold).astype(int), probs


theta_log = fit_logistic_regression_gd(Xc_train_s, yc_train)
preds_log, probs_log = predict_logistic(theta_log, Xc_test_s)
acc_scratch = np.mean(preds_log == yc_test)
print(f"\n[From scratch] Logistic Regression (gradient descent)")
print(f"  theta (bias, size, irregularity) = {np.round(theta_log, 3)}")
print(f"  Test Accuracy = {acc_scratch:.3f}")

# --- B2. Everything else via scikit-learn -------------------------------
try:
    from sklearn.linear_model import LogisticRegression
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.svm import SVC
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

    models = {
        "Logistic Regression": LogisticRegression().fit(Xc_train_s, yc_train),
        "Decision Tree": DecisionTreeClassifier(max_depth=4, random_state=0).fit(Xc_train, yc_train),
        "SVM (RBF kernel)": SVC(kernel="rbf", C=1.0, gamma="scale").fit(Xc_train_s, yc_train),
        "k-NN (k=5)": KNeighborsClassifier(n_neighbors=5).fit(Xc_train_s, yc_train),
    }

    print(f"\n{'Model':<22}{'Accuracy':>10}{'Precision':>11}{'Recall':>9}{'F1':>8}")
    print("-" * 62)
    for name, model in models.items():
        # tree uses unscaled features (scale-invariant); others use scaled
        X_eval = Xc_test if name == "Decision Tree" else Xc_test_s
        preds = model.predict(X_eval)
        acc = accuracy_score(yc_test, preds)
        prec = precision_score(yc_test, preds, zero_division=0)
        rec = recall_score(yc_test, preds, zero_division=0)
        f1 = f1_score(yc_test, preds, zero_division=0)
        print(f"{name:<22}{acc:>10.3f}{prec:>11.3f}{rec:>9.3f}{f1:>8.3f}")

    print(f"\n{'From-scratch Logistic Regression':<22}{acc_scratch:>10.3f}")
    print("  (matches sklearn closely - both solve the same convex optimization problem)")

except ImportError:
    print("\n(scikit-learn not installed - skipping sklearn classification demos)")


print("\nDone. Try changing k in k-NN, max_depth in the tree, or the SVM kernel")
print("(kernel='linear' vs 'rbf') and re-run to see how metrics shift!")
