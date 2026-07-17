# Interview Questions — Math for ML

Quick-fire theory questions with concise model answers.

## Linear Algebra
**Q: What is the geometric interpretation of the dot product?**
A: `a·b = ||a|| ||b|| cos(θ)` — it measures how aligned two vectors are, scaled by their magnitudes. Zero means orthogonal (unrelated); positive means similar direction; negative means opposite direction.

**Q: What does it mean for a matrix to be singular?**
A: Its determinant is 0, meaning it's not invertible — it collapses space into a lower dimension (loses information), so there's no unique way to "undo" its transformation.

**Q: What is PCA doing mathematically?**
A: Finding the eigenvectors of the data's covariance matrix — the eigenvector with the largest eigenvalue is the direction of maximum variance; projecting onto the top-k eigenvectors gives the best possible k-dimensional linear approximation of the data.

## Calculus / Gradient
**Q: What is a gradient, and what does it point toward?**
A: The vector of all partial derivatives of a scalar function; it points in the direction of steepest ascent (increase) of the function. Negative gradient points toward steepest descent, which is why gradient descent subtracts it.

**Q: Why do we subtract the gradient in gradient descent, not add it?**
A: The gradient points toward increasing the function; since we want to minimize the loss, we move in the opposite direction — hence `θ = θ - η∇L`.

**Q: What is backpropagation, in one sentence?**
A: The chain rule applied systematically backward through a neural network's computational graph, efficiently computing the gradient of the loss with respect to every parameter.

**Q: Why do vanishing gradients happen?**
A: Backpropagation multiplies many local derivatives together across layers (chain rule); if each is consistently less than 1 (e.g., sigmoid's max derivative is 0.25), the product shrinks toward zero over many layers, so early layers receive almost no learning signal.

## Probability & Statistics
**Q: What's the difference between a PMF and a PDF?**
A: PMF (Probability Mass Function) applies to discrete random variables — `P(X=x)` directly gives a probability. PDF (Probability Density Function) applies to continuous variables — you must integrate over a range to get a probability; the density value itself isn't a probability.

**Q: What is Maximum Likelihood Estimation?**
A: Choosing the parameters that make the observed data most probable under the assumed model — equivalently, maximizing `Π P(data | parameters)`, usually via the log-likelihood for numerical/computational convenience.

**Q: Explain the bias-variance tradeoff.**
A: Total error decomposes into bias² (systematic error from an overly simple model, underfitting) + variance (sensitivity to the specific training set, overfitting) + irreducible noise. Simpler models have higher bias/lower variance; complex models have lower bias/higher variance — good generalization requires balancing both.

## Optimization
**Q: Why is convexity important for optimization?**
A: A convex function has no separate local minima — any local minimum found by gradient descent is guaranteed to be the global minimum, given a suitable learning rate.

**Q: How does Adam differ from plain SGD?**
A: Adam maintains per-parameter adaptive learning rates using running estimates of both the mean (momentum) and variance (like RMSProp) of past gradients, generally converging faster and requiring less learning-rate tuning than plain SGD.

**Q: What problem do Lagrange multipliers solve?**
A: Finding the optimum of a function subject to equality constraints, by finding points where the objective's gradient is parallel to the constraint's gradient.

## Information Theory
**Q: What's the relationship between cross-entropy and KL divergence?**
A: `D_KL(p||q) = H(p,q) - H(p)`. Since `H(p)` doesn't depend on the model, minimizing cross-entropy and minimizing KL divergence are equivalent optimization problems.

**Q: Why is cross-entropy used for classification instead of MSE?**
A: Cross-entropy is the negative log-likelihood under a Categorical/Bernoulli output assumption (matching how classification is actually modeled), and produces better-behaved gradients for confidently-wrong predictions than MSE combined with softmax outputs would.

See `Cheatsheet.md` for a compressed final-review version.
