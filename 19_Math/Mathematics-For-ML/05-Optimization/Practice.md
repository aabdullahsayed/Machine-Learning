# Practice — Optimization

1. Implement plain gradient descent from scratch (as in `Gradient-Descent.md`) to minimize `f(w) = w⁴ - 3w³ + 2` starting from several different initial points (e.g., `w=-2, 0, 3`) — observe that it can converge to different results depending on initialization, since this function is non-convex.
2. Implement Momentum-based gradient descent from scratch and compare its convergence speed against plain gradient descent on a function with a narrow, elongated minimum (e.g., `f(x,y) = x² + 100y²`).
3. Use PyTorch's built-in `SGD`, `SGD(momentum=0.9)`, and `Adam` optimizers on the same small neural network and training data — plot and compare their loss curves.
4. By hand, solve the constrained optimization problem: minimize `f(x,y) = x² + y²` subject to `x + 2y = 3`, using Lagrange multipliers.
5. Verify a function is convex by checking its second derivative (e.g., confirm `f(x) = x²` is convex, and `f(x) = x³` is NOT convex over all real numbers).
6. Explain in your own words: why is Adam generally considered a "safer default" than plain SGD for a new deep learning project, and in what situation might you still choose plain SGD?

✅ Done? Move to `06-Information-Theory`.
