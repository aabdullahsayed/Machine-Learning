# Partial Derivatives

## Math Explanation

When a function has **multiple inputs**, `f(x, y, z, ...)`, a **partial derivative** measures the rate of change with respect to ONE variable, treating all others as constant.

Notation: `∂f/∂x` (the curly "d", called "partial," to distinguish from single-variable `d/dx`).

### Worked example
```
f(x, y) = x²y + 3y²

∂f/∂x = 2xy          (treat y as a constant, differentiate the x² term normally)
∂f/∂y = x² + 6y        (treat x as a constant, differentiate the y terms normally)
```

### Why this matters
Real functions (and ML models) almost never have just one input — a neural network's loss function depends on potentially **millions or billions of parameters** simultaneously. Partial derivatives let us ask: "if I nudge just THIS ONE weight, how does the loss change?" — one variable at a time.

## In ML/DL

- **Every single weight in a neural network gets its own partial derivative** during backpropagation — `∂Loss/∂w1`, `∂Loss/∂w2`, ..., `∂Loss/∂wn` — telling you exactly how much each individual weight contributed to the current error.
- **This is literally what a gradient IS** (see `Gradient.md` next) — a gradient is just the collection of ALL partial derivatives, packaged into a vector.
- **PyTorch/TensorFlow's autograd systems** compute these partial derivatives automatically for every parameter in your model, via the chain rule applied backward through the computational graph.
```python
import torch
x = torch.tensor(2.0, requires_grad=True)
y = torch.tensor(3.0, requires_grad=True)
f = x**2 * y + 3 * y**2
f.backward()
print(x.grad)   # ∂f/∂x = 2xy = 2*2*3 = 12
print(y.grad)   # ∂f/∂y = x² + 6y = 4 + 18 = 22
```

Read `Gradient.md` next — it's the single most important file in this entire repo for understanding how models learn.
