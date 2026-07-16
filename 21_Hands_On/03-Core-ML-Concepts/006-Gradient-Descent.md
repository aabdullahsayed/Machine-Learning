# 006 - Gradient Descent

## Concept
Gradient descent is an iterative optimization algorithm: compute the gradient (slope) of the loss function with respect to the parameters, then step in the opposite direction to reduce loss. Variants include Batch, Stochastic (SGD), and Mini-batch gradient descent.

## Why It Matters
This is THE algorithm that trains nearly every ML model beyond simple closed-form solutions — linear/logistic regression, neural networks (module 10), and beyond. Understanding it deeply demystifies "training" as a concept.

## Hands-On

```python
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)

# Simple linear regression setup: y = true_w * x + true_b + noise
true_w, true_b = 3.0, 5.0
X = np.random.uniform(-5, 5, 200)
y = true_w * X + true_b + np.random.normal(0, 1, 200)

def compute_loss(w, b, X, y):
    y_pred = w * X + b
    return np.mean((y_pred - y) ** 2)

def compute_gradients(w, b, X, y):
    y_pred = w * X + b
    dw = np.mean(2 * (y_pred - y) * X)
    db = np.mean(2 * (y_pred - y))
    return dw, db

# 1. BATCH gradient descent - uses the ENTIRE dataset for every update
def batch_gradient_descent(X, y, lr=0.01, epochs=100):
    w, b = 0.0, 0.0
    history = []
    for epoch in range(epochs):
        dw, db = compute_gradients(w, b, X, y)
        w -= lr * dw
        b -= lr * db
        history.append(compute_loss(w, b, X, y))
    return w, b, history

w_batch, b_batch, history_batch = batch_gradient_descent(X, y, lr=0.01, epochs=100)
print(f"Batch GD    -> w={w_batch:.3f}, b={b_batch:.3f} (true: w={true_w}, b={true_b})")

# 2. STOCHASTIC gradient descent - one random sample per update, noisier
# but much faster per-step and scales to huge datasets
def stochastic_gradient_descent(X, y, lr=0.01, epochs=20):
    w, b = 0.0, 0.0
    history = []
    n = len(X)
    for epoch in range(epochs):
        indices = np.random.permutation(n)
        for i in indices:
            xi, yi = X[i], y[i]
            y_pred = w * xi + b
            dw = 2 * (y_pred - yi) * xi
            db = 2 * (y_pred - yi)
            w -= lr * dw
            b -= lr * db
        history.append(compute_loss(w, b, X, y))
    return w, b, history

w_sgd, b_sgd, history_sgd = stochastic_gradient_descent(X, y, lr=0.001, epochs=20)
print(f"SGD         -> w={w_sgd:.3f}, b={b_sgd:.3f}")

# 3. MINI-BATCH gradient descent - the standard in deep learning (module 10):
# balances the stability of batch GD with the speed of SGD
def minibatch_gradient_descent(X, y, lr=0.01, epochs=50, batch_size=32):
    w, b = 0.0, 0.0
    history = []
    n = len(X)
    for epoch in range(epochs):
        indices = np.random.permutation(n)
        X_shuffled, y_shuffled = X[indices], y[indices]
        for start in range(0, n, batch_size):
            X_batch = X_shuffled[start:start + batch_size]
            y_batch = y_shuffled[start:start + batch_size]
            dw, db = compute_gradients(w, b, X_batch, y_batch)
            w -= lr * dw
            b -= lr * db
        history.append(compute_loss(w, b, X, y))
    return w, b, history

w_mb, b_mb, history_mb = minibatch_gradient_descent(X, y, lr=0.01, epochs=50)
print(f"Mini-batch  -> w={w_mb:.3f}, b={b_mb:.3f}")

# 4. Effect of learning rate - too high diverges, too low is slow
for lr in [0.001, 0.01, 0.1, 0.5]:
    _, _, hist = batch_gradient_descent(X, y, lr=lr, epochs=20)
    print(f"lr={lr}: final loss={hist[-1]:.4f}" if not np.isnan(hist[-1]) and hist[-1] < 1e6
          else f"lr={lr}: DIVERGED")

# 5. Plot loss curves
plt.figure(figsize=(7, 5))
plt.plot(history_batch, label="Batch GD")
plt.plot(np.linspace(0, len(history_batch), len(history_sgd)), history_sgd, label="SGD")
plt.plot(np.linspace(0, len(history_batch), len(history_mb)), history_mb, label="Mini-batch GD")
plt.xlabel("Epoch (approx.)")
plt.ylabel("Loss (MSE)")
plt.legend()
plt.title("Gradient Descent Variants - Loss Convergence")
plt.savefig("gradient_descent_comparison.png")
plt.close()
```

## Exercise
1. Implement gradient descent with **momentum** (`velocity = momentum * velocity - lr * grad; w += velocity`) and compare its convergence speed against plain batch GD.
2. Experiment with batch sizes of 1, 16, 64, and the full dataset — how does the loss curve's smoothness change?
3. Find, experimentally, the largest learning rate for which batch gradient descent still converges on this dataset (right before it diverges).

## Key Takeaways
- Batch GD is stable but slow per-epoch on large datasets; SGD is fast per-step but noisy; mini-batch GD is the practical default used throughout deep learning.
- Learning rate is the single most important hyperparameter to tune — too high diverges, too low wastes compute.
- This exact update rule (`param -= lr * gradient`) reappears, scaled up with automatic differentiation, as the training loop of every neural network in module 10.
