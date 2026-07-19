# 001 - Perceptron

## Concept
The perceptron is the simplest possible neural network: one neuron that computes a weighted sum of inputs, adds a bias, and passes the result through a step function to produce a binary output. It's the atomic building block everything in deep learning descends from.

## Why It Matters
Understanding the perceptron's learning rule — nudge weights toward reducing error — is literally the same idea (simplified) as backpropagation in a 100-layer network. Also worth knowing its famous limitation: it can only learn linearly separable patterns.

## Hands-On

```python
import numpy as np
import matplotlib.pyplot as plt

class Perceptron:
    def __init__(self, n_features, lr=0.1):
        self.weights = np.zeros(n_features)
        self.bias = 0.0
        self.lr = lr

    def activation(self, z):
        return np.where(z >= 0, 1, 0)   # step function

    def predict(self, X):
        z = X @ self.weights + self.bias
        return self.activation(z)

    def fit(self, X, y, epochs=20):
        errors_per_epoch = []
        for epoch in range(epochs):
            total_error = 0
            for xi, target in zip(X, y):
                pred = self.predict(xi.reshape(1, -1))[0]
                error = target - pred
                # The perceptron learning rule: nudge weights toward the correct answer
                self.weights += self.lr * error * xi
                self.bias += self.lr * error
                total_error += abs(error)
            errors_per_epoch.append(total_error)
        return errors_per_epoch

# 1. AND gate - linearly separable, perceptron solves it perfectly
X_and = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_and = np.array([0, 0, 0, 1])

p = Perceptron(n_features=2, lr=0.1)
errors = p.fit(X_and, y_and, epochs=10)
print("AND gate predictions:", p.predict(X_and))
print("Learned weights:", p.weights, "bias:", p.bias)

plt.plot(errors, marker="o")
plt.xlabel("Epoch")
plt.ylabel("Total errors")
plt.title("Perceptron learning AND gate")
plt.savefig("perceptron_and.png")
plt.close()

# 2. XOR gate - famously NOT linearly separable, perceptron fails
X_xor = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_xor = np.array([0, 1, 1, 0])

p_xor = Perceptron(n_features=2, lr=0.1)
errors_xor = p_xor.fit(X_xor, y_xor, epochs=50)
print("XOR gate predictions (should fail to match [0,1,1,0]):", p_xor.predict(X_xor))
print("Final epoch errors:", errors_xor[-1], "(never reaches 0)")
```

## Exercise
1. Plot the decision boundary the AND perceptron learns (a line in 2D) using `weights` and `bias`.
2. Show that XOR error never converges to zero, no matter how many epochs you run.
3. Add a second layer manually (combine two perceptrons' outputs into a third) to solve XOR — this is the intuition behind multi-layer networks (next lesson).

## Key Takeaways
- The perceptron update rule `w += lr * error * x` is the ancestor of gradient descent.
- A single perceptron can only separate data with a straight line/hyperplane — it cannot solve XOR.
- Stacking perceptrons into layers (multi-layer perceptron) is exactly what's needed to solve non-linearly-separable problems, motivating the next lesson.
