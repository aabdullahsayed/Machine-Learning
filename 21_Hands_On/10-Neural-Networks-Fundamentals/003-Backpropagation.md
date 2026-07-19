# 003 - Backpropagation

## Concept
Backpropagation computes the gradient of the loss with respect to every weight in the network by applying the chain rule backward from the output layer to the input layer. It's the algorithm that makes training deep networks computationally feasible.

## Why It Matters
Frameworks like PyTorch hide backprop behind `.backward()`, but understanding it demystifies why deep networks can be hard to train (vanishing/exploding gradients) and why architectural choices (activations, normalization, skip connections) matter.

## Hands-On

```python
import numpy as np

# A tiny 2-layer network trained with manually implemented backprop, on XOR
np.random.seed(1)

X = np.array([[0,0],[0,1],[1,0],[1,1]], dtype=float)
y = np.array([[0],[1],[1],[0]], dtype=float)   # XOR

# Initialize weights
W1 = np.random.randn(2, 4) * 0.5
b1 = np.zeros((1, 4))
W2 = np.random.randn(4, 1) * 0.5
b2 = np.zeros((1, 1))

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def sigmoid_deriv(a):
    return a * (1 - a)   # derivative in terms of the sigmoid OUTPUT, a common trick

lr = 0.5
losses = []

for epoch in range(10000):
    # --- Forward pass ---
    z1 = X @ W1 + b1
    a1 = sigmoid(z1)          # hidden layer activations
    z2 = a1 @ W2 + b2
    a2 = sigmoid(z2)          # output prediction

    loss = np.mean((y - a2) ** 2)
    losses.append(loss)

    # --- Backward pass (the chain rule, applied layer by layer) ---
    # dL/da2
    d_a2 = -(y - a2)
    # dL/dz2 = dL/da2 * da2/dz2
    d_z2 = d_a2 * sigmoid_deriv(a2)
    # dL/dW2 = a1^T @ dL/dz2
    d_W2 = a1.T @ d_z2
    d_b2 = np.sum(d_z2, axis=0, keepdims=True)

    # Propagate the error back into the hidden layer
    d_a1 = d_z2 @ W2.T
    d_z1 = d_a1 * sigmoid_deriv(a1)
    d_W1 = X.T @ d_z1
    d_b1 = np.sum(d_z1, axis=0, keepdims=True)

    # --- Gradient descent update ---
    W2 -= lr * d_W2 / len(X)
    b2 -= lr * d_b2 / len(X)
    W1 -= lr * d_W1 / len(X)
    b1 -= lr * d_b1 / len(X)

    if epoch % 2000 == 0:
        print(f"Epoch {epoch}, loss={loss:.4f}")

print("\nFinal predictions on XOR:")
print(np.round(a2, 3))
print("Actual XOR labels:")
print(y.ravel())

import matplotlib.pyplot as plt
plt.plot(losses)
plt.xlabel("Epoch")
plt.ylabel("MSE Loss")
plt.title("Backprop training loss (solving XOR with a hidden layer)")
plt.savefig("backprop_loss.png")
```

## Exercise
1. Verify one gradient numerically: perturb a single weight in `W1` by `+1e-5`, recompute the loss, and check the finite-difference gradient matches `d_W1` at that position (this is "gradient checking," a standard debugging technique).
2. Add a third hidden neuron and re-derive/re-run — does convergence speed change?
3. Replace `sigmoid` with `relu` in the hidden layer (keep sigmoid at output) and adjust the derivative accordingly — does it train faster?

## Key Takeaways
- Backprop is just the chain rule applied systematically, layer by layer, from output back to input.
- Every gradient (`d_W1`, `d_W2`, etc.) tells you "how much would the loss change if I nudged this weight" — gradient descent then nudges it in the opposite direction.
- Deep networks can suffer vanishing gradients when many small derivatives (like sigmoid's, which maxes at 0.25) get multiplied together across many layers — this motivates ReLU and normalization techniques used in real architectures.
