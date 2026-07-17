# Practice — Calculus

1. By hand, compute `d/dx` of `f(x) = 3x² + 5x - 2`. Verify using `sympy`:
```python
import sympy as sp
x = sp.Symbol('x')
f = 3*x**2 + 5*x - 2
print(sp.diff(f, x))
```
2. Compute the gradient of `f(x, y) = x²y + y³` by hand. Verify with PyTorch autograd.
3. Implement gradient descent from scratch (no libraries) to minimize `f(w) = (w - 5)²`, starting from `w=0`, and print `w` at each of 20 steps. Confirm it converges to `5`.
4. Implement a numerical gradient checker: compare your hand-derived gradient of some function against `(f(x+h) - f(x-h)) / (2h)` for small `h` (e.g., `1e-5`).
5. Build a tiny 2-layer neural network in PyTorch, call `.backward()`, and print the `.grad` of every parameter — explain in your own words what each one represents.
6. Explain in your own words (no code): why does a very small first-derivative value (like sigmoid's max of 0.25) repeated across 50 layers cause vanishing gradients? (Hint: think about what `0.25^50` equals.)

✅ Done? Move to `03-Probability`.
