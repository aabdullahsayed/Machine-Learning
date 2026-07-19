# 005 - Building a Neural Net From Scratch

## Concept
This lesson assembles everything from 001-004 (perceptrons, layers, backprop, activations) into a reusable, general-purpose neural network class built only with NumPy — no frameworks.

## Why It Matters
Building one end-to-end, however small, is the single best way to cement how forward pass, loss, backward pass, and weight updates fit together before you rely on PyTorch/TensorFlow's abstractions to do it for you.

## Hands-On

```python
import numpy as np

class NeuralNetwork:
    def __init__(self, layer_sizes, lr=0.1):
        """layer_sizes e.g. [2, 8, 8, 1] = input(2) -> hidden(8) -> hidden(8) -> output(1)"""
        self.lr = lr
        self.weights = []
        self.biases = []
        for i in range(len(layer_sizes) - 1):
            # He initialization - scales with layer size, helps ReLU networks train stably
            w = np.random.randn(layer_sizes[i], layer_sizes[i+1]) * np.sqrt(2 / layer_sizes[i])
            b = np.zeros((1, layer_sizes[i+1]))
            self.weights.append(w)
            self.biases.append(b)

    def relu(self, z): return np.maximum(0, z)
    def relu_deriv(self, z): return (z > 0).astype(float)
    def sigmoid(self, z): return 1 / (1 + np.exp(-z))

    def forward(self, X):
        self.z_values = []
        self.a_values = [X]
        a = X
        for i in range(len(self.weights) - 1):
            z = a @ self.weights[i] + self.biases[i]
            a = self.relu(z)
            self.z_values.append(z)
            self.a_values.append(a)
        # Output layer uses sigmoid (binary classification)
        z_out = a @ self.weights[-1] + self.biases[-1]
        a_out = self.sigmoid(z_out)
        self.z_values.append(z_out)
        self.a_values.append(a_out)
        return a_out

    def backward(self, X, y):
        m = X.shape[0]
        n_layers = len(self.weights)
        grads_w = [None] * n_layers
        grads_b = [None] * n_layers

        # Output layer error
        delta = self.a_values[-1] - y   # for sigmoid+BCE this simplifies nicely

        for i in reversed(range(n_layers)):
            grads_w[i] = self.a_values[i].T @ delta / m
            grads_b[i] = np.sum(delta, axis=0, keepdims=True) / m
            if i > 0:
                delta = (delta @ self.weights[i].T) * self.relu_deriv(self.z_values[i-1])

        for i in range(n_layers):
            self.weights[i] -= self.lr * grads_w[i]
            self.biases[i] -= self.lr * grads_b[i]

    def compute_loss(self, y_pred, y_true):
        eps = 1e-8
        return -np.mean(y_true * np.log(y_pred + eps) + (1 - y_true) * np.log(1 - y_pred + eps))

    def fit(self, X, y, epochs=1000, verbose=True):
        losses = []
        for epoch in range(epochs):
            y_pred = self.forward(X)
            loss = self.compute_loss(y_pred, y)
            losses.append(loss)
            self.backward(X, y)
            if verbose and epoch % 200 == 0:
                print(f"Epoch {epoch}: loss={loss:.4f}")
        return losses

    def predict(self, X):
        return (self.forward(X) > 0.5).astype(int)

# 1. Test on make_moons (non-linear dataset)
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split

X, y = make_moons(n_samples=500, noise=0.2, random_state=42)
y = y.reshape(-1, 1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

nn = NeuralNetwork(layer_sizes=[2, 16, 8, 1], lr=0.5)
losses = nn.fit(X_train, y_train, epochs=2000)

preds = nn.predict(X_test)
accuracy = np.mean(preds == y_test)
print(f"\nTest accuracy: {accuracy:.4f}")

import matplotlib.pyplot as plt
plt.plot(losses)
plt.xlabel("Epoch")
plt.ylabel("Binary cross-entropy loss")
plt.savefig("scratch_nn_loss.png")
```

## Exercise
1. Add support for mini-batch training (shuffle + split X into batches of size 32 each epoch) instead of full-batch gradient descent.
2. Add L2 regularization to the loss and gradient updates (`loss += lambda * sum(w**2 for w in weights)`).
3. Extend the class to support multi-class classification: softmax output layer + categorical cross-entropy loss.

## Key Takeaways
- A neural network is fully specified by: layer sizes, activation functions, a loss function, and an optimization rule — everything else is bookkeeping.
- He initialization (scaling by `sqrt(2/fan_in)`) matters a lot for ReLU networks — poor initialization can stall training entirely.
- This from-scratch implementation is ~60 lines, but every production framework (PyTorch, TensorFlow) is doing conceptually the same thing, just with automatic differentiation and GPU support.
