# Regularization

## Math Explanation

**Regularization** adds a penalty term to the loss function to discourage overly complex models, directly targeting the "variance" side of the bias-variance tradeoff (`04-Statistics/Bias-Variance.md`).
```
Total Loss = Original Loss + λ · Penalty(θ)
```
`λ` controls the strength of regularization — a hyperparameter you tune (larger `λ` = simpler model, more bias, less variance).

### L2 Regularization (Ridge / Weight Decay)
```
Penalty = ||θ||² = Σ θᵢ²
```
Its gradient is `2θ`, meaning during gradient descent, every weight update includes a term proportionally shrinking the weight toward zero — hence "weight decay." Geometrically (per `01-Linear-Algebra/Norms.md`), the L2 penalty's circular constraint region tends to shrink all weights smoothly, rarely to exactly zero.

### L1 Regularization (Lasso)
```
Penalty = ||θ||₁ = Σ |θᵢ|
```
Its gradient has constant magnitude regardless of the weight's size, and the diamond-shaped constraint region (`01-Linear-Algebra/Norms.md`) means the optimal solution frequently lands exactly ON an axis — producing **sparse** solutions where many weights become exactly zero (automatic feature selection).

### Elastic Net
Combines both: `Penalty = α||θ||₁ + (1-α)||θ||²` — gets some sparsity from L1 while keeping the smoother, more stable optimization behavior of L2.

### Bayesian interpretation (connects back to `03-Probability/Bayes-Theorem.md`)
Regularization is mathematically equivalent to placing a **prior distribution** on the weights and performing MAP (Maximum A Posteriori) estimation instead of plain MLE:
- L2 regularization ⟺ Gaussian prior on weights (values near 0 are a priori more likely)
- L1 regularization ⟺ Laplace prior on weights (strongly favors exactly 0)

## In ML/DL

### Dropout — a very different, but conceptually related, regularization technique
Randomly "drops" (zeroes out) a fraction of neurons during each training step (see `03-Probability/Basics.md` — each neuron is independently kept with probability `p`, a Bernoulli process). This prevents neurons from "co-adapting" too heavily on specific other neurons, forcing the network to learn more robust, redundant representations — empirically very effective for reducing overfitting in deep networks.
```python
import torch.nn as nn
model = nn.Sequential(
    nn.Linear(784, 256), nn.ReLU(), nn.Dropout(p=0.5),
    nn.Linear(256, 10)
)
```

### Early stopping — regularization via optimization control
Simply stop training once validation loss stops improving (even if training loss keeps decreasing) — a very simple, widely-used, effective form of regularization that directly targets the bias-variance tradeoff without modifying the loss function at all.

### Data augmentation — regularization via more effective data
Artificially expanding your training set (image rotations/flips, text paraphrasing, etc.) reduces overfitting by preventing the model from memorizing exact training examples — conceptually a very different mechanism than L1/L2, but serving the exact same "reduce variance" goal from `04-Statistics/Bias-Variance.md`.

### Practical example
```python
# L2 regularization ("weight decay") is often built directly into the optimizer:
optimizer = torch.optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-4)
```
Tuning `weight_decay` (equivalent to `λ` above) is one of the most common hyperparameter tuning tasks in practical deep learning — too small and you overfit, too large and you underfit (directly visualized via the bias-variance tradeoff curve).
