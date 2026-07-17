# Constrained Optimization

## Math Explanation

**Constrained optimization** means minimizing/maximizing a function subject to restrictions on the allowed values of the variables — either **equality constraints** (`g(x) = 0`, solved via Lagrange multipliers, see previous file) or **inequality constraints** (`h(x) ≤ 0`).

### The general form
```
minimize    f(x)
subject to  g_i(x) = 0    (equality constraints)
            h_j(x) ≤ 0     (inequality constraints)
```

### KKT Conditions (the general solution framework)
At an optimal point `x*`, the **Karush-Kuhn-Tucker conditions** must hold:
1. **Stationarity**: `∇f(x*) + Σλᵢ∇gᵢ(x*) + Σμⱼ∇hⱼ(x*) = 0`
2. **Primal feasibility**: constraints are actually satisfied.
3. **Dual feasibility**: `μⱼ ≥ 0` for inequality constraints.
4. **Complementary slackness**: `μⱼ·hⱼ(x*) = 0` — either the constraint is "active" (exactly at its boundary, `hⱼ(x*)=0`) or its multiplier `μⱼ` is zero (the constraint isn't binding at the optimum).

This is the formal generalization of Lagrange multipliers to handle inequality constraints, and it's the theoretical backbone of a huge swath of applied optimization, including SVMs.

### Projected Gradient Descent (a practical algorithm)
A simple, widely-used approach for constrained problems: take a normal gradient descent step, then **project** back onto the feasible region if the step violated a constraint.
```python
def projected_gradient_descent(w, grad, lr, project_fn):
    w_new = w - lr * grad
    return project_fn(w_new)   # e.g., clip values to a valid range
```

## In ML/DL

- **Weight clipping** (used in the original Wasserstein GAN formulation, to enforce a Lipschitz constraint on the discriminator) is literally projected gradient descent — after each update, weights are clipped to a fixed range `[-c, c]`.
- **Gradient clipping** (extremely common in RNN/Transformer training to prevent exploding gradients) can be viewed as a soft, practical form of constrained optimization — constraining the *norm* of the update step, not the parameters themselves.
- **Projection onto probability simplex constraints** appears in some structured prediction and reinforcement learning settings, where outputs must remain valid probability distributions (non-negative, summing to 1) throughout optimization.
- **Fairness-constrained ML**: modern responsible-AI techniques sometimes explicitly frame model training as constrained optimization — "minimize prediction error, subject to a fairness metric (e.g., equal false-positive rates across groups) staying within an acceptable bound" — directly applying this KKT/Lagrangian framework to real-world model constraints.
- **Physics-Informed Neural Networks (PINNs)** incorporate physical laws as constraints (e.g., conservation of energy) into the training objective, often via penalty terms derived from this same constrained-optimization theory.
