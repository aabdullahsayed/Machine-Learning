# Loss Functions — A Practical Reference

## Math Explanation & Where Each Comes From

A **loss function** quantifies how wrong a model's prediction is — training minimizes it via gradient descent. Every standard loss function below traces back to concepts already covered in this repo.

### Mean Squared Error (MSE) — Regression
```
MSE = (1/n) Σ (yᵢ - ŷᵢ)²
```
Derived from **MLE under a Gaussian noise assumption** (`04-Statistics/MLE.md`) — minimizing MSE is mathematically equivalent to maximizing the likelihood of your data assuming the true value is the model's prediction plus Gaussian noise.
```python
mse = np.mean((y_true - y_pred)**2)
```

### Mean Absolute Error (MAE) — Regression, robust to outliers
```
MAE = (1/n) Σ |yᵢ - ŷᵢ|
```
Corresponds to an L1 norm (`01-Linear-Algebra/Norms.md`) of the error, and to MLE under a Laplace-distributed noise assumption — less sensitive to large outlier errors than MSE (since MSE squares errors, a single huge outlier dominates the loss; MAE doesn't amplify it as much).

### Cross-Entropy Loss — Classification
```
CE = -Σ y_true · log(y_pred)
```
Covered fully in `06-Information-Theory/Cross-Entropy.md` — derived from MLE under a Categorical/Bernoulli output distribution assumption.

### Hinge Loss — SVMs
```
Hinge = max(0, 1 - y·ŷ)      (for y ∈ {-1, +1})
```
Penalizes predictions that are wrong OR not confidently correct enough (within a "margin") — the objective directly optimized by Support Vector Machines, connected to the constrained-optimization/Lagrange-multiplier formulation in `05-Optimization/Lagrange-Multipliers.md`.

### Huber Loss — Regression, combines MSE + MAE
```
Huber(e) = 0.5e²           if |e| ≤ δ    (behaves like MSE for small errors)
           δ(|e| - 0.5δ)    if |e| > δ     (behaves like MAE for large errors)
```
A practical engineering compromise: smooth/differentiable like MSE for small errors (good gradient behavior near the optimum), but robust to outliers like MAE for large errors.

## In ML/DL — Choosing the Right Loss

| Problem type | Standard loss | Why |
|---|---|---|
| Regression (no outliers) | MSE | Matches Gaussian noise assumption, smooth gradients |
| Regression (outliers present) | MAE or Huber | Less sensitive to extreme errors |
| Binary classification | Binary Cross-Entropy | MLE under Bernoulli assumption |
| Multi-class classification | Cross-Entropy | MLE under Categorical assumption |
| Multi-label classification | Binary Cross-Entropy (per label) | Each label treated as independent Bernoulli |
| Ranking/margin-based | Hinge Loss | Directly optimizes decision boundary margin |
| Object detection (bounding boxes) | Smooth L1 / IoU-based losses | Combines robustness with task-specific geometry |

**Practical takeaway**: choosing a loss function isn't arbitrary — it's a direct statement about what probabilistic assumption you're making about your data/errors (see `04-Statistics/MLE.md`), and understanding this connection helps you pick (or design) the right loss for a new, unusual problem rather than defaulting blindly to MSE or cross-entropy.
