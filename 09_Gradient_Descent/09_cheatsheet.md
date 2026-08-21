# 09 — Gradient Descent Cheat Sheet

## Core update rule

```
θ := θ − α · ∇J(θ)
```

## Key formulas

| Concept | Formula |
|---|---|
| Linear regression prediction | `ŷ = θ0 + θ1·x` |
| Mean Squared Error cost | `J(θ) = (1/2m) Σ (ŷ_i − y_i)²` |
| Gradient w.r.t. bias | `∂J/∂θ0 = (1/m) Σ (ŷ_i − y_i)` |
| Gradient w.r.t. weight | `∂J/∂θ1 = (1/m) Σ (ŷ_i − y_i)·x_i` |
| Momentum velocity | `v := β·v + (1−β)·g` |
| Adam 1st moment | `m := β1·m + (1−β1)·g` |
| Adam 2nd moment | `v := β2·v + (1−β2)·g²` |
| Adam update | `θ := θ − α·m̂ / (√v̂ + ε)` |

## Terminology quick reference

| Term | Meaning |
|---|---|
| `θ` (theta) | model parameters (weights/biases) |
| `α` (alpha) | learning rate |
| `∇J(θ)` | gradient of the cost function |
| epoch | one full pass over the training data |
| batch size | # examples used per gradient update |
| convergence | loss stops meaningfully decreasing |
| local minimum | a low point that isn't the global lowest point |
| saddle point | flat gradient, but not a minimum (curves up one way, down another) |
| convex function | single bowl shape, one global minimum |

## The 3 core variants at a glance

| Variant | Data per update |
|---|---|
| Batch GD | all `m` examples |
| Stochastic GD | 1 example |
| Mini-Batch GD | small batch `b` (e.g. 32–256) |

## Optimizer decision cheat sheet

```
Simple/convex problem, learning?      -> Plain (Batch) GD
Sparse features (NLP, one-hot heavy)? -> AdaGrad
Non-stationary / RNNs?                -> RMSProp
Deep learning, general default?       -> Adam
Want tuned SGD performance ceiling?   -> SGD + Momentum (+ LR schedule)
```

## Learning rate troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Loss barely moves | `α` too small | increase `α`, or use Adam |
| Loss oscillates / explodes / NaN | `α` too large | decrease `α` |
| Loss decreases then plateaus early | stuck in local min / saddle, or `α` decayed too much | add momentum, tweak schedule |
| Loss decreases smoothly | ✅ all good | keep training / consider early stopping |

## Minimal code skeleton (from-scratch)

```python
theta = np.zeros(n_params)
for step in range(n_iterations):
    y_hat = X @ theta                     # predict
    error = y_hat - y                     # how wrong?
    grad = (X.T @ error) / len(y)         # gradient (vectorized)
    theta -= alpha * grad                 # update
```

## Formula derivation reminder (chain rule, 1 line)

```
J = (1/2m)Σ(θ0+θ1x−y)²  →  dJ/dθ1 = (1/m)Σ(θ0+θ1x−y)·x
                                     └────────┬────────┘
                                        "error × feature"
```

Keep this page open while coding — it covers 90% of what you'll need
day-to-day.
