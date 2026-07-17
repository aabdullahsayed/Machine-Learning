# Jacobian & Hessian

## Math Explanation

### Jacobian — gradients for vector-valued functions
The **gradient** applies to functions with a *single scalar* output (`f: ℝⁿ → ℝ`). When a function outputs a **vector** instead (`f: ℝⁿ → ℝᵐ`), you need the **Jacobian matrix** — every output's partial derivative with respect to every input:
```
        [ ∂f1/∂x1   ∂f1/∂x2  ...  ∂f1/∂xn ]
J(f) =  [ ∂f2/∂x1   ∂f2/∂x2  ...  ∂f2/∂xn ]
        [   ...        ...    ...    ...   ]
        [ ∂fm/∂x1   ∂fm/∂x2  ...  ∂fm/∂xn ]
```
Each **row** is the gradient of one output component with respect to all inputs. The gradient (`∇f`) is just a special case of the Jacobian where `m = 1` (a single-row Jacobian, transposed into a column vector).

### Hessian — second derivatives (curvature)
The **Hessian** is the matrix of ALL second partial derivatives of a scalar function `f: ℝⁿ → ℝ`:
```
        [ ∂²f/∂x1²    ∂²f/∂x1∂x2  ... ]
H(f) =  [ ∂²f/∂x2∂x1  ∂²f/∂x2²    ... ]
        [    ...          ...      ... ]
```
While the gradient tells you the **slope** (first-order behavior), the Hessian tells you the **curvature** (second-order behavior) — is the function curving upward (bowl-shaped, convex) or downward, or a saddle?

### Using the Hessian to classify critical points
At a point where `∇f = 0`:
- Hessian is **positive definite** (all eigenvalues > 0) → local **minimum** (bowl shape)
- Hessian is **negative definite** (all eigenvalues < 0) → local **maximum**
- Hessian has **mixed-sign eigenvalues** → **saddle point** (min in one direction, max in another)

## In ML/DL

- **The Jacobian appears constantly inside backpropagation.** Every layer of a neural network is technically a vector-valued function (input vector → output vector), so the chain rule during backprop is really chaining together Jacobians, not just single-number derivatives. Frameworks like PyTorch compute "vector-Jacobian products" efficiently without ever forming the full Jacobian matrix explicitly (too large/expensive).
- **Second-order optimization methods** (Newton's method, L-BFGS) use the Hessian to take smarter steps than plain gradient descent — accounting for curvature lets you converge faster near a minimum. Rarely used directly for huge deep networks (the Hessian would be enormous — billions × billions), but approximations (like Adam's use of squared gradients) borrow this intuition cheaply.
- **Saddle points** are now understood to be a bigger practical obstacle in deep learning than local minima — high-dimensional loss surfaces have MANY more saddle points than true local minima, and momentum-based optimizers (`05-Optimization/SGD-Variants.md`) help escape them.
- **Hessian eigenvalues and training stability**: a poorly-conditioned Hessian (eigenvalues spanning many orders of magnitude) causes the classic "zig-zagging" slow convergence of plain gradient descent — this motivates adaptive learning rate methods (Adam, RMSProp).

```python
import torch

x = torch.tensor([1.0, 2.0], requires_grad=True)
def f(x): return x[0]**2 + x[1]**3

hessian = torch.autograd.functional.hessian(f, x)
print(hessian)
```
