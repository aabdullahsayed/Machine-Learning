# Cross-Entropy

## Math Explanation

**Cross-entropy** measures the "distance" between two probability distributions: the TRUE distribution `p` and an ESTIMATED/predicted distribution `q`.
```
H(p, q) = -Σ p(x) log(q(x))
```
It's closely related to plain entropy (`Entropy.md`) — instead of using the true distribution's own probabilities inside the log, you use your *model's predicted* probabilities, while still weighting by the true distribution.

### Key property
`H(p, q) ≥ H(p)` always — cross-entropy is minimized (equal to the true entropy `H(p)`) exactly when your predicted distribution `q` perfectly matches the true distribution `p`. **This is why minimizing cross-entropy is a mathematically well-justified way to make your model's predictions match reality as closely as possible.**

### Worked example: classification
True label: class 0 (so `p = [1, 0, 0]`, a one-hot "distribution").
Model's prediction: `q = [0.7, 0.2, 0.1]`.
```
H(p, q) = -(1·log(0.7) + 0·log(0.2) + 0·log(0.1)) = -log(0.7) ≈ 0.357
```
Notice: because `p` is one-hot, ALL terms except the true class vanish — cross-entropy for classification simplifies to just `-log(predicted probability of the TRUE class)`. If the model had instead predicted 0.99 for the true class, the loss would be much lower (`-log(0.99) ≈ 0.01`); if it predicted 0.01 for the true class (very wrong and confident), the loss would be very high (`-log(0.01) ≈ 4.6`) — cross-entropy heavily penalizes confident, wrong predictions.

## In ML/DL

### Cross-entropy loss is THE standard loss function for classification
```python
import numpy as np

def cross_entropy_loss(y_true_one_hot, y_pred_probs):
    epsilon = 1e-12   # avoid log(0)
    return -np.sum(y_true_one_hot * np.log(y_pred_probs + epsilon))

y_true = np.array([1, 0, 0])         # true class: 0
y_pred = np.array([0.7, 0.2, 0.1])    # model's softmax output
print(cross_entropy_loss(y_true, y_pred))
```
```python
# In practice (PyTorch), this is built in and combined with softmax for numerical stability:
import torch.nn as nn
criterion = nn.CrossEntropyLoss()
loss = criterion(model_output_logits, true_class_indices)
```

### Why cross-entropy (and not, say, MSE) for classification
As shown in `04-Statistics/MLE.md`, cross-entropy loss is exactly the negative log-likelihood under a Categorical/Bernoulli output distribution — it's the mathematically principled choice given how classification outputs are modeled, and it produces much better-behaved gradients for classification than MSE would (MSE combined with softmax outputs tends to produce very small, unhelpful gradients when predictions are very wrong, slowing learning — cross-entropy avoids this issue).

### Binary Cross-Entropy (BCE) — for binary/multi-label classification
```
BCE = -[y·log(ŷ) + (1-y)·log(1-ŷ)]
```
Used for binary classification (spam/not spam) or multi-label problems (an image can belong to multiple categories simultaneously), where each output is treated as an independent Bernoulli variable.

### Practical example
Training an image classifier on ImageNet (1000 classes): the model outputs a 1000-dimensional softmax probability vector; cross-entropy loss compares this against the true one-hot label, and its gradient (via backpropagation, `02-Calculus/Gradient.md`) is what actually updates every weight in the network during training.
