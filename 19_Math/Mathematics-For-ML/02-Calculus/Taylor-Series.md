# Taylor Series

## Math Explanation

A **Taylor series** approximates a function near a point using a polynomial built from its derivatives at that point:
```
f(x) ≈ f(a) + f'(a)(x-a) + f''(a)/2! · (x-a)² + f'''(a)/3! · (x-a)³ + ...
```
The more terms you include, the better the approximation (near `a`). Truncating after a few terms gives a useful, computable approximation of a potentially complicated function.

### First-order (linear) approximation — the one that matters most for ML
Truncating after the first derivative term:
```
f(x) ≈ f(a) + f'(a)(x - a)
```
This is literally "the tangent line" — the best straight-line approximation of `f` near point `a`.

### Multivariable version (first-order)
```
f(x) ≈ f(a) + ∇f(a) · (x - a)
```
This says: near a point `a`, the function's value changes approximately linearly, in the direction and magnitude given by the gradient — a direct generalization of the single-variable tangent line, using the gradient instead of a scalar derivative.

### Second-order approximation (adds curvature via the Hessian)
```
f(x) ≈ f(a) + ∇f(a)·(x-a) + ½(x-a)ᵀH(a)(x-a)
```

## In ML/DL

- **The first-order Taylor approximation is the mathematical justification for gradient descent.** Near the current parameters `θ`, the loss function is *approximately* `L(θ) + ∇L(θ)·(θ_new - θ)` — and since we don't know the true shape of `L` far away, we trust this local linear approximation only for a **small step**, which is exactly why the learning rate `η` must be small: too large a step and the linear (Taylor) approximation is no longer accurate, causing the loss to potentially increase instead of decrease.
- **Second-order optimization methods** (Newton's method) use the second-order Taylor approximation (including the Hessian) to take a smarter, curvature-aware step directly to the approximate minimum of that local quadratic approximation — faster convergence near a minimum, but expensive for large models (needs the Hessian).
- **Understanding "why small learning rates are safer"**: this is a direct, practical consequence of Taylor's theorem — the linear approximation used by gradient descent is only locally accurate, and larger steps venture into regions where that approximation breaks down.
- **Loss landscape visualization/analysis** in deep learning research often uses local quadratic (second-order Taylor) approximations around trained model weights to study "flatness" of minima and its relationship to generalization.
