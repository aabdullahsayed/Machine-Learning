# 002 - Feedforward Neural Networks

## Concept
A feedforward (multi-layer) neural network stacks layers of neurons where each layer's output feeds into the next. Non-linear activation functions between layers let the network approximate complex, non-linearly-separable functions — solving exactly the XOR-style problem a single perceptron can't.

## Why It Matters
This is the architecture underlying every deep learning model, before you add convolutions, recurrence, or attention. Get the forward pass mechanics solid here before backpropagation (next lesson).

## Hands-On

```python
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# 1. A non-linearly-separable dataset - the kind a single perceptron can't solve
X, y = make_moons(n_samples=500, noise=0.2, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. sklearn's MLP (a full feedforward network with backprop under the hood)
mlp = MLPClassifier(hidden_layer_sizes=(16, 8), activation="relu",
                     max_iter=2000, random_state=42)
mlp.fit(X_train, y_train)
print("MLP test accuracy:", mlp.score(X_test, y_test))

# 3. Manual forward pass - understand exactly what "hidden_layer_sizes=(16, 8)" does
def relu(z):
    return np.maximum(0, z)

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def forward_pass(X, W1, b1, W2, b2, W3, b3):
    z1 = X @ W1 + b1
    a1 = relu(z1)             # hidden layer 1
    z2 = a1 @ W2 + b2
    a2 = relu(z2)             # hidden layer 2
    z3 = a2 @ W3 + b3
    a3 = sigmoid(z3)          # output layer (binary classification)
    return a3

# Random initialization just to demonstrate shapes/mechanics (untrained)
np.random.seed(0)
W1 = np.random.randn(2, 16) * 0.1;  b1 = np.zeros(16)
W2 = np.random.randn(16, 8) * 0.1;  b2 = np.zeros(8)
W3 = np.random.randn(8, 1) * 0.1;   b3 = np.zeros(1)

output = forward_pass(X_train[:5], W1, b1, W2, b2, W3, b3)
print("Forward pass output shape:", output.shape)  # (5, 1) - one probability per sample

# 4. Visualize the decision boundary the trained MLP learned
xx, yy = np.meshgrid(np.linspace(X[:, 0].min()-0.5, X[:, 0].max()+0.5, 200),
                      np.linspace(X[:, 1].min()-0.5, X[:, 1].max()+0.5, 200))
Z = mlp.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
plt.contourf(xx, yy, Z, alpha=0.3)
plt.scatter(X[:, 0], X[:, 1], c=y, edgecolors="k")
plt.title("MLP decision boundary on make_moons")
plt.savefig("mlp_boundary.png")
```

## Exercise
1. Change `hidden_layer_sizes` to `(2,)` (a single tiny hidden layer) — can it still separate the moons? Try `(64, 64, 64)`.
2. Swap `activation="relu"` for `"tanh"` and `"logistic"` — compare test accuracy and training time.
3. Extend `forward_pass` to compute total parameter count for the network and verify it matches `sum(w.size for w in mlp.coefs_) + sum(b.size for b in mlp.intercepts_)`.

## Key Takeaways
- Depth (more layers) and width (more neurons per layer) both increase representational capacity, but also overfitting risk and training difficulty.
- Non-linear activations between layers are essential — stacking purely linear layers collapses mathematically into a single linear layer.
- `MLPClassifier`/`MLPRegressor` are fine for learning and small problems, but production deep learning uses PyTorch/TensorFlow (lesson 006) for GPU acceleration and flexibility.
