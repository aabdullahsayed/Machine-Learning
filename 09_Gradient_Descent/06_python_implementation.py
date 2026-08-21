"""
06 - Gradient Descent from scratch (NumPy only)
================================================
Implements, on simple linear regression (y = theta0 + theta1*x):

  1. Batch Gradient Descent
  2. Stochastic Gradient Descent (SGD)
  3. Mini-Batch Gradient Descent
  4. Momentum
  5. Adam

Run:
    python 06_python_implementation.py

Requires: numpy  (matplotlib optional, used only if installed, for a plot)
Uses the accompanying 07_demo_dataset.csv (falls back to a generated
dataset if the CSV isn't found, so this script also runs standalone).
"""

import os
import csv
import math
import numpy as np


# ----------------------------------------------------------------------
# 1. Load (or synthesize) the demo dataset
# ----------------------------------------------------------------------
def load_dataset():
    path = os.path.join(os.path.dirname(__file__), "07_demo_dataset.csv")
    xs, ys = [], []
    if os.path.exists(path):
        with open(path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    xs.append(float(row["x"]))
                    ys.append(float(row["y"]))
                except (ValueError, TypeError):
                    continue  # skip malformed rows
    if not xs:
        rng = np.random.default_rng(42)
        xs = rng.uniform(0, 10, 60)
        ys = 3.5 * xs + 7 + rng.normal(0, 1.5, 60)
    return np.array(xs), np.array(ys)


X, y = load_dataset()
m = len(X)
print(f"Loaded dataset with {m} examples. True relationship ~ y = 3.5x + 7\n")


# ----------------------------------------------------------------------
# 2. Cost function and gradient (theta = [theta0, theta1])
# ----------------------------------------------------------------------
def predict(theta, x):
    return theta[0] + theta[1] * x


def cost(theta, x, y_true):
    errors = predict(theta, x) - y_true
    return np.mean(errors ** 2) / 2


def gradient(theta, x, y_true):
    errors = predict(theta, x) - y_true
    d0 = np.mean(errors)
    d1 = np.mean(errors * x)
    return np.array([d0, d1])


# ----------------------------------------------------------------------
# 3. Batch Gradient Descent
# ----------------------------------------------------------------------
def batch_gd(x, y_true, alpha=0.02, n_iter=500):
    theta = np.zeros(2)
    history = []
    for _ in range(n_iter):
        g = gradient(theta, x, y_true)
        theta = theta - alpha * g
        history.append(cost(theta, x, y_true))
    return theta, history


# ----------------------------------------------------------------------
# 4. Stochastic Gradient Descent
# ----------------------------------------------------------------------
def stochastic_gd(x, y_true, alpha=0.02, n_epochs=30, seed=0):
    rng = np.random.default_rng(seed)
    theta = np.zeros(2)
    history = []
    n = len(x)
    for _ in range(n_epochs):
        idx = rng.permutation(n)
        for i in idx:
            xi, yi = x[i:i + 1], y_true[i:i + 1]
            g = gradient(theta, xi, yi)
            theta = theta - alpha * g
        history.append(cost(theta, x, y_true))
    return theta, history


# ----------------------------------------------------------------------
# 5. Mini-Batch Gradient Descent
# ----------------------------------------------------------------------
def minibatch_gd(x, y_true, alpha=0.02, n_epochs=30, batch_size=8, seed=0):
    rng = np.random.default_rng(seed)
    theta = np.zeros(2)
    history = []
    n = len(x)
    for _ in range(n_epochs):
        idx = rng.permutation(n)
        for start in range(0, n, batch_size):
            batch_idx = idx[start:start + batch_size]
            xb, yb = x[batch_idx], y_true[batch_idx]
            g = gradient(theta, xb, yb)
            theta = theta - alpha * g
        history.append(cost(theta, x, y_true))
    return theta, history


# ----------------------------------------------------------------------
# 6. Batch GD + Momentum
# ----------------------------------------------------------------------
def momentum_gd(x, y_true, alpha=0.02, beta=0.9, n_iter=500):
    theta = np.zeros(2)
    v = np.zeros(2)
    history = []
    for _ in range(n_iter):
        g = gradient(theta, x, y_true)
        v = beta * v + (1 - beta) * g
        theta = theta - alpha * v
        history.append(cost(theta, x, y_true))
    return theta, history


# ----------------------------------------------------------------------
# 7. Adam
# ----------------------------------------------------------------------
def adam_gd(x, y_true, alpha=0.1, beta1=0.9, beta2=0.999, eps=1e-8, n_iter=500):
    theta = np.zeros(2)
    m_t = np.zeros(2)
    v_t = np.zeros(2)
    history = []
    for t in range(1, n_iter + 1):
        g = gradient(theta, x, y_true)
        m_t = beta1 * m_t + (1 - beta1) * g
        v_t = beta2 * v_t + (1 - beta2) * (g ** 2)
        m_hat = m_t / (1 - beta1 ** t)
        v_hat = v_t / (1 - beta2 ** t)
        theta = theta - alpha * m_hat / (np.sqrt(v_hat) + eps)
        history.append(cost(theta, x, y_true))
    return theta, history


# ----------------------------------------------------------------------
# 8. Run everything and compare
# ----------------------------------------------------------------------
if __name__ == "__main__":
    results = {}
    results["Batch GD"] = batch_gd(X, y)
    results["Stochastic GD"] = stochastic_gd(X, y)
    results["Mini-Batch GD"] = minibatch_gd(X, y)
    results["Momentum"] = momentum_gd(X, y)
    results["Adam"] = adam_gd(X, y)

    print(f"{'Method':<16}{'theta0':>10}{'theta1':>10}{'final cost':>14}")
    print("-" * 50)
    for name, (theta, history) in results.items():
        print(f"{name:<16}{theta[0]:>10.3f}{theta[1]:>10.3f}{history[-1]:>14.5f}")

    # Optional: plot convergence curves if matplotlib is available
    try:
        import matplotlib.pyplot as plt

        plt.figure(figsize=(8, 5))
        for name, (theta, history) in results.items():
            plt.plot(history, label=name)
        plt.xlabel("iteration / epoch")
        plt.ylabel("cost J(theta)")
        plt.title("Gradient Descent Variants: Convergence Comparison")
        plt.legend()
        plt.yscale("log")
        out_path = os.path.join(os.path.dirname(__file__), "convergence_plot.png")
        plt.savefig(out_path, dpi=120, bbox_inches="tight")
        print(f"\nSaved convergence plot to: {out_path}")
    except ImportError:
        print("\n(matplotlib not installed — skipping plot; numeric results above still valid)")
