# Vector & Matrix Norms

## Math Explanation

A **norm** measures the "size" or "length" of a vector. Written `||v||`.

### Common vector norms
| Norm | Formula | Meaning |
|---|---|---|
| **L1** (Manhattan) | `Σ \|vᵢ\|` | sum of absolute values |
| **L2** (Euclidean) | `√(Σ vᵢ²)` | straight-line distance (the "usual" length) |
| **L∞** (Max) | `max(\|vᵢ\|)` | largest single element |
| **Lp** (general) | `(Σ \|vᵢ\|ᵖ)^(1/p)` | generalizes all of the above |

### Geometric intuition
The "unit ball" (`||v|| = 1`) looks different for each norm:
- L2: a perfect circle/sphere.
- L1: a diamond (square rotated 45°) in 2D.
- L∞: a square.

This shape difference is *exactly* why L1 regularization produces sparse solutions (see below) while L2 doesn't — the diamond shape of the L1 ball has "corners" on the axes, making it likely that the optimal solution touches an axis (i.e., some coefficients become exactly zero).

## In ML/DL

- **L2 regularization (Ridge/weight decay)**: adds `λ||w||²` to the loss function — penalizes large weights, encourages small (but not necessarily zero) weights, improving generalization.
```python
loss = mse_loss + lam * np.sum(w**2)   # L2 penalty
```
- **L1 regularization (Lasso)**: adds `λ||w||₁` — encourages **sparse** weights (many exactly zero), useful for automatic feature selection.
```python
loss = mse_loss + lam * np.sum(np.abs(w))   # L1 penalty
```
- **Gradient clipping**: clip the L2 norm of the gradient vector during training to prevent exploding gradients in RNNs/deep networks:
```python
grad_norm = np.linalg.norm(gradient)
if grad_norm > max_norm:
    gradient = gradient * (max_norm / grad_norm)
```
- **Distance metrics**: L2 norm of `(a - b)` is Euclidean distance — used in k-NN, k-means clustering, and many similarity-based methods.
- **Batch/Layer normalization** in deep learning involves normalizing activations, conceptually related to controlling the "norm"/scale of values flowing through the network.
