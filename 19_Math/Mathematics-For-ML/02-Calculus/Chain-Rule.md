# The Chain Rule

## Math Explanation

The **chain rule** tells you how to differentiate a **composition of functions** — a function inside another function.

### Single variable
If `y = f(g(x))`, then:
```
dy/dx = f'(g(x)) · g'(x)
```
Or in "Leibniz notation" (very intuitive for chaining many steps):
```
dy/dx = dy/du · du/dx     (where u = g(x))
```

### Worked example
```
y = (3x + 1)²

Let u = 3x + 1, so y = u²
dy/du = 2u
du/dx = 3

dy/dx = dy/du · du/dx = 2u · 3 = 6u = 6(3x+1) = 18x + 6
```

### Multivariable chain rule (the version that matters most for ML)
If `z = f(x, y)` where `x = x(t)` and `y = y(t)` (both depend on some other variable `t`):
```
dz/dt = ∂f/∂x · dx/dt  +  ∂f/∂y · dy/dt
```
This generalizes to arbitrarily long chains of composed functions with many variables at each stage — exactly the situation in a deep neural network, where the loss depends on the output layer, which depends on the previous layer, which depends on the one before that, all the way back to the input.

## In ML/DL

### The chain rule IS backpropagation
A neural network is a long composition of functions:
```
Loss = L( f_output( f_hiddenN( ... f_hidden1( f_input(x) ) ... ) ) )
```
To find `∂Loss/∂w` for a weight `w` buried deep inside this composition, you apply the chain rule repeatedly, layer by layer, working **backward** from the loss to that weight — multiplying together all the partial derivatives ("local gradients") along the path. This backward, layer-by-layer application of the chain rule is literally what "backpropagation" means.

### Concrete 2-layer example
```
z1 = W1 @ x + b1
a1 = relu(z1)
z2 = W2 @ a1 + b2
loss = mse(z2, y)
```
To get `∂loss/∂W1`, the chain rule says:
```
∂loss/∂W1 = ∂loss/∂z2 · ∂z2/∂a1 · ∂a1/∂z1 · ∂z1/∂W1
```
Each term is a "local" derivative of one step, and backprop computes them right-to-left, reusing intermediate results (this reuse is exactly why backprop is efficient — computing this naively from scratch for every weight would repeat enormous amounts of work).

```python
import torch
import torch.nn as nn

model = nn.Sequential(nn.Linear(10, 5), nn.ReLU(), nn.Linear(5, 1))
x = torch.randn(1, 10)
y = torch.tensor([[1.0]])

pred = model(x)
loss = nn.functional.mse_loss(pred, y)
loss.backward()    # chain rule applied automatically, backward through every layer

for name, param in model.named_parameters():
    print(name, param.grad.shape)   # gradient for every weight, computed via chained partials
```

### Vanishing/exploding gradients — a direct consequence of the chain rule
Because backprop **multiplies** many local derivatives together across layers, if each local derivative is consistently `< 1` (e.g., sigmoid's max derivative is 0.25), the product shrinks toward zero over many layers → **vanishing gradients** (early layers barely learn). If local derivatives are consistently `> 1`, the product grows explosively → **exploding gradients**. This single insight — "the chain rule is a product of many terms" — explains one of the most important practical challenges in training deep networks, and motivates architectural fixes like ReLU activations, residual/skip connections (ResNets), and careful weight initialization.
