# Lagrange Multipliers

## Math Explanation

**Lagrange multipliers** solve **constrained optimization** problems: minimize (or maximize) a function `f(x)` subject to an equality constraint `g(x) = 0`.

### The method
Instead of directly minimizing `f(x)` subject to `g(x)=0`, form the **Lagrangian**:
```
L(x, λ) = f(x) - λ·g(x)
```
Then find points where the gradient of `L` (with respect to BOTH `x` and `λ`) is zero:
```
∇_x L = 0   →   ∇f(x) = λ∇g(x)
∇_λ L = 0   →   g(x) = 0     (just recovers the original constraint)
```

### Geometric intuition
At the constrained optimum, the gradient of the objective `f` must be **parallel** to the gradient of the constraint `g` — if they weren't parallel, you could slide slightly along the constraint surface `g(x)=0` and still improve `f`, meaning you hadn't actually found the optimum yet. Parallel gradients mean `∇f = λ∇g` for some scalar `λ` — this is exactly the condition the method solves for.

### Worked example
Minimize `f(x,y) = x² + y²` subject to `x + y = 1`.
```
∇f = [2x, 2y],  ∇g = [1, 1]
2x = λ,  2y = λ   →   x = y
Combined with x + y = 1:   x = y = 0.5
```
Minimum distance from origin to the line `x+y=1` occurs at `(0.5, 0.5)` — matches geometric intuition (closest point on a line to the origin is where the connecting segment is perpendicular to the line).

## In ML/DL

- **Support Vector Machines (SVMs)** are derived almost entirely using Lagrange multipliers (and their inequality-constraint generalization, KKT conditions) — maximizing the margin between classes subject to correct-classification constraints is a textbook constrained optimization problem, and the resulting "dual problem" (in terms of Lagrange multipliers) is what makes the famous "kernel trick" possible.
- **Regularized regression (Ridge, Lasso) has an equivalent constrained-optimization formulation**: instead of adding a penalty term `λ||w||²` to the loss (the common "penalized" form), you can equivalently frame it as "minimize the loss subject to `||w||² ≤ some budget`" — Lagrange multiplier theory is what formally connects these two equivalent formulations, and explains why `λ` in the penalized form directly corresponds to a constraint budget.
- **Constrained policy optimization in Reinforcement Learning** (e.g., ensuring a robot's actions satisfy safety constraints while maximizing reward) directly uses Lagrangian methods to balance the primary objective against hard constraints.
- **KKT (Karush-Kuhn-Tucker) conditions**, the generalization of Lagrange multipliers to inequality constraints (`g(x) ≤ 0`, not just `g(x) = 0`), are the theoretical foundation behind why SVM training converges to a well-defined, unique solution, and are referenced throughout convex optimization theory in ML.
