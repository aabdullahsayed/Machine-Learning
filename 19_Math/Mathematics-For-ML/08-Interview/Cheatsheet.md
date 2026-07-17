# Math for ML — Cheat Sheet (Last-Minute Revision)

## Linear Algebra
- Dot product: `a·b = Σaᵢbᵢ = ||a||·||b||·cos(θ)`
- Matrix mult: `(m×n) @ (n×p) = (m×p)`, each entry is a dot product.
- Eigenvector: `Av = λv` — direction unchanged, only scaled by `λ`.
- SVD: `A = UΣVᵀ` — works for ANY matrix, not just square.
- PCA = eigendecomposition of the covariance matrix.

## Calculus / Gradient
- Gradient: `∇f = [∂f/∂x1, ..., ∂f/∂xn]` — vector of all partial derivatives.
- Gradient points toward **steepest ascent**; `-∇f` points toward steepest descent.
- Gradient descent: `θ = θ - η∇L(θ)`.
- Chain rule: `dy/dx = dy/du · du/dx` — backpropagation IS the chain rule, applied backward through a network.
- Jacobian = matrix of partial derivatives for vector-output functions (generalizes gradient).
- Hessian = matrix of second derivatives; positive definite at a critical point ⟹ local minimum.

## Probability
- `P(A|B) = P(A∩B)/P(B)` — conditional probability.
- Bayes: `P(H|E) = P(E|H)P(H)/P(E)` — posterior ∝ likelihood × prior.
- `E[X] = Σx·P(X=x)` — expectation is linear: `E[X+Y]=E[X]+E[Y]` always.
- `Var(X) = E[X²] - (E[X])²`.

## Statistics
- MLE: choose parameters maximizing `P(data | parameters)`.
- MSE loss ⟺ MLE under Gaussian noise. Cross-entropy loss ⟺ MLE under Categorical/Bernoulli.
- Bias-Variance: `Error = Bias² + Variance + Irreducible Error`.
- p-value: probability of data this extreme IF the null hypothesis were true — small p-value → reject H0.

## Optimization
- Convex function: no separate local minima → gradient descent finds the global minimum.
- Momentum: `v = β·v + (1-β)·∇f`; smooths/accelerates descent.
- Adam: combines momentum (1st moment) + RMSProp (2nd moment) — most common default optimizer.
- Lagrange multipliers: at the constrained optimum, `∇f = λ∇g` (gradients are parallel).

## Information Theory
- Entropy: `H(X) = -Σ P(x)log P(x)` — measures uncertainty; max when uniform.
- Cross-entropy: `H(p,q) = -Σ p(x)log q(x)` — the standard classification loss.
- KL divergence: `D_KL(p||q) = H(p,q) - H(p)` — measures how different q is from p; NOT symmetric.

## Golden one-liners for interviews
- "The gradient is the vector of steepest ascent; we subtract it to descend."
- "Backpropagation is the chain rule, applied efficiently backward through a computational graph."
- "Most standard loss functions are literally negative log-likelihoods under some distributional assumption."
- "Regularization = adding a prior belief (Bayesian) that trades a little bias for a lot less variance."
- "PCA finds the eigenvectors of the covariance matrix — directions of maximum variance."
- "Convexity guarantees gradient descent finds the global minimum; deep learning mostly doesn't have this guarantee, but works well in practice anyway."
