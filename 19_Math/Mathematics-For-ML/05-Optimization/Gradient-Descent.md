# Gradient Descent

## Math Explanation

**Gradient descent** is an iterative algorithm to find a (local) minimum of a function, using the gradient (see `02-Calculus/Gradient.md`) as a compass.

### The update rule
```
θ_{t+1} = θ_t - η · ∇f(θ_t)
```
- Start at some initial point `θ_0`.
- Repeatedly step in the direction **opposite** the gradient (since `∇f` points toward increase, `-∇f` points toward decrease).
- `η` (learning rate) controls step size.
- Stop when the gradient is near zero (you've reached a minimum) or after a fixed number of iterations.

### Why it works (informally)
By the first-order Taylor approximation (`02-Calculus/Taylor-Series.md`), near the current point, `f(θ - η∇f) ≈ f(θ) - η||∇f||²`, which is **strictly less than `f(θ)`** for any small positive `η` (as long as `∇f ≠ 0`) — so each step is guaranteed to (locally) decrease the function value, provided the step is small enough for the linear approximation to remain valid.

### Choosing the learning rate — the central practical challenge
```
Too small η:  Convergence is correct but painfully slow.
Too large η:  Can overshoot the minimum, oscillate, or even diverge (loss increases!).
Just right:   Fast, stable convergence.
```

### Convex vs non-convex functions
- On a **convex** function (bowl-shaped, one global minimum — see `Convexity.md`), gradient descent is guaranteed to converge to the global minimum.
- On a **non-convex** function (like a real neural network's loss surface, full of local minima and saddle points), gradient descent only guarantees convergence to *some* critical point, not necessarily the global minimum — in practice, this turns out to be surprisingly fine for deep learning (see `07-ML-Applications` for more).

## In ML/DL

### This is literally the algorithm that trains almost every ML model
Linear regression, logistic regression, neural networks, and virtually every modern deep learning model are trained by gradient descent (or one of its variants — see `SGD-Variants.md`).

```python
import numpy as np

# minimize f(w) = (w - 5)^2 + 3, gradient is 2(w-5)
w = 0.0
lr = 0.1
for step in range(50):
    grad = 2 * (w - 5)
    w = w - lr * grad
print(f"Converged to w = {w:.4f}")   # should approach 5
```

### Batch, Stochastic, and Mini-batch Gradient Descent
- **Batch GD**: compute the gradient using the ENTIRE training dataset each step — accurate gradient, but extremely slow/expensive for large datasets, and requires all data to fit in memory.
- **Stochastic GD (SGD)**: compute the gradient using just ONE random sample each step — very fast per step, but noisy (the gradient estimate is highly variable).
- **Mini-batch GD** (what's actually used in practice): compute the gradient using a small batch (e.g., 32, 64, 256 samples) — balances accuracy and speed, and maps efficiently onto GPU parallelism.

### Learning rate scheduling
Because of the tradeoffs above, real training often starts with a larger learning rate (fast initial progress) and decreases it over time (fine-tune precisely near the minimum) — "learning rate decay" or "learning rate schedules" (step decay, cosine annealing, warmup) are standard practice in virtually all modern deep learning training recipes.

### Practical example
```python
import torch

model = torch.nn.Linear(10, 1)
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)   # plain gradient descent

for epoch in range(100):
    optimizer.zero_grad()
    loss = compute_loss(model, data)   # your loss function
    loss.backward()                      # compute ∇loss via backprop
    optimizer.step()                       # θ = θ - lr * ∇loss  <- gradient descent update
```
