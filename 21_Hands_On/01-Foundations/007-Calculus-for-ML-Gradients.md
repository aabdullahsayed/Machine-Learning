# 007 - Calculus for ML: Gradients

## Concept
Derivatives measure how a function's output changes as its input changes. Gradients generalize this to multiple variables. Every model that "learns" (linear regression, neural networks) does so by computing gradients of a loss function and moving parameters in the direction that reduces loss.

## Why It Matters
Gradient descent (module 03) and backpropagation (module 10) are both direct applications of the chain rule. Understanding derivatives here demystifies what `.backward()` does in PyTorch.

## Hands-On

```python
import numpy as np

# 1. Numerical derivative - the definition of a derivative, approximated
def f(x):
    return x ** 2

def numerical_derivative(f, x, h=1e-5):
    return (f(x + h) - f(x - h)) / (2 * h)

print("f(x) = x^2, f'(3) numerically:", numerical_derivative(f, 3))
print("f'(3) analytically (2x):", 2 * 3)

# 2. Partial derivatives - derivative w.r.t. one variable, others held constant
def g(x, y):
    return x**2 + 3 * x * y + y**2

def partial_derivative_x(g, x, y, h=1e-5):
    return (g(x + h, y) - g(x - h, y)) / (2 * h)

def partial_derivative_y(g, x, y, h=1e-5):
    return (g(x, y + h) - g(x, y - h)) / (2 * h)

print("dg/dx at (1,2):", partial_derivative_x(g, 1, 2))  # analytical: 2x+3y = 8
print("dg/dy at (1,2):", partial_derivative_y(g, 1, 2))  # analytical: 3x+2y = 7

# 3. Gradient of a loss function - Mean Squared Error for linear regression
# Loss(w) = (1/n) * sum((y_pred - y_true)^2), y_pred = w * x
def mse_loss(w, x, y):
    y_pred = w * x
    return np.mean((y_pred - y) ** 2)

def mse_gradient(w, x, y):
    y_pred = w * x
    return np.mean(2 * (y_pred - y) * x)  # analytical gradient dLoss/dw

x_data = np.array([1, 2, 3, 4])
y_data = np.array([2, 4, 6, 8])  # true relationship: y = 2x

w = 0.0  # start with a bad guess
for step in range(10):
    grad = mse_gradient(w, x_data, y_data)
    w = w - 0.1 * grad  # gradient descent update
    loss = mse_loss(w, x_data, y_data)
    print(f"Step {step}: w={w:.4f}, loss={loss:.4f}")

print(f"\nFinal weight: {w:.4f} (target: 2.0)")

# 4. Chain rule demo - the backbone of backpropagation
# If y = (3x + 1)^2, dy/dx = 2*(3x+1) * 3
def composed(x):
    inner = 3 * x + 1
    outer = inner ** 2
    return outer

x_val = 2.0
numerical = numerical_derivative(composed, x_val)
analytical = 2 * (3 * x_val + 1) * 3
print(f"\nChain rule check -> numerical: {numerical:.4f}, analytical: {analytical:.4f}")
```

## Exercise
1. Extend the gradient descent loop to also learn a bias term `b` (`y_pred = w*x + b`), computing its gradient too.
2. Try different learning rates (0.01, 0.1, 0.5, 1.5) in the gradient descent loop — what happens at 1.5? Explain why.
3. Implement `numerical_derivative` for a 2-variable function and compare it to the analytical partial derivatives for `g(x,y) = x^2*y + y^3`.

## Key Takeaways
- Gradient descent is just "compute the slope, step downhill, repeat."
- Too large a learning rate causes divergence (loss increases); too small makes training painfully slow — this exact tradeoff resurfaces in module 03 and module 10.
- The chain rule lets you compute gradients through composed functions — this is literally how backpropagation works through many stacked neural network layers.
