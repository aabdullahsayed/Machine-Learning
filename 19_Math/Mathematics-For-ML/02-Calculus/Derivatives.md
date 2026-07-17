# Derivatives (Single Variable)

## Math Explanation

The **derivative** of a function `f(x)` measures how fast `f` changes as `x` changes — the slope of the tangent line at a point.

### Formal definition
```
f'(x) = lim (h→0) [f(x+h) - f(x)] / h
```
It's the instantaneous rate of change — a limit of the "average rate of change" (rise/run) as the interval shrinks to zero.

### Common derivative rules
| Function | Derivative |
|---|---|
| `f(x) = c` (constant) | `f'(x) = 0` |
| `f(x) = xⁿ` | `f'(x) = n·xⁿ⁻¹` |
| `f(x) = eˣ` | `f'(x) = eˣ` |
| `f(x) = ln(x)` | `f'(x) = 1/x` |
| `f(x) = sin(x)` | `f'(x) = cos(x)` |
| `f(x) = c·g(x)` | `f'(x) = c·g'(x)` |
| `f(x) = g(x) + h(x)` | `f'(x) = g'(x) + h'(x)` (sum rule) |
| `f(x) = g(x)·h(x)` | `f'(x) = g'(x)h(x) + g(x)h'(x)` (product rule) |
| `f(x) = g(h(x))` | `f'(x) = g'(h(x))·h'(x)` (chain rule — see `Chain-Rule.md`) |

### What the derivative tells you
- `f'(x) > 0` → function is increasing at `x`
- `f'(x) < 0` → function is decreasing at `x`
- `f'(x) = 0` → flat point — a local min, max, or saddle/inflection point

## In ML/DL

- **This is the foundation of everything.** Training a model means finding parameters that minimize a loss function — and you find minima by looking at where the derivative is zero (or by following the derivative "downhill," see `05-Optimization/Gradient-Descent.md`).
- **Activation function derivatives** are computed millions of times during backpropagation:
```python
# Sigmoid and its derivative
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    s = sigmoid(x)
    return s * (1 - s)     # derived using the quotient/chain rule
```
- **ReLU's derivative** is trivially simple (`1` if `x > 0`, else `0`), which is a big reason ReLU trains faster than sigmoid/tanh in deep networks — no vanishing-gradient-prone small derivatives.
- **Numerical differentiation** (`(f(x+h) - f(x)) / h` directly from the definition) is used to sanity-check that your hand-derived/autograd gradients are correct — a classic ML engineering debugging technique called "gradient checking."
