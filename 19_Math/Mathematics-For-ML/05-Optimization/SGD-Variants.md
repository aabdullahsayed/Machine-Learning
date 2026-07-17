# SGD Variants (Momentum, RMSProp, Adam)

## Math Explanation

Plain gradient descent has known weaknesses: slow convergence on poorly-conditioned (elongated, "narrow valley") loss surfaces, and getting stuck oscillating. These variants add "memory" of past gradients to fix that.

### Momentum
Instead of using only the current gradient, accumulate a **velocity** — a running average of past gradients — like a ball rolling downhill picking up speed:
```
v_{t+1} = β·v_t + (1-β)·∇f(θ_t)     (β commonly ≈ 0.9)
θ_{t+1} = θ_t - η·v_{t+1}
```
This dampens oscillations (in directions where the gradient keeps flipping sign) while accelerating progress in directions where the gradient is consistent.

### RMSProp
Divides the learning rate by a running average of the **squared** gradient magnitude, per-parameter — parameters with historically large gradients get smaller effective steps, and vice versa (adaptive, per-parameter learning rates):
```
s_{t+1} = β·s_t + (1-β)·(∇f(θ_t))²
θ_{t+1} = θ_t - η · ∇f(θ_t) / (√s_{t+1} + ε)
```

### Adam (Adaptive Moment Estimation) — the most widely used optimizer today
Combines Momentum (first moment: mean of gradients) AND RMSProp (second moment: variance of gradients):
```
m_{t+1} = β1·m_t + (1-β1)·∇f(θ_t)         (momentum term)
v_{t+1} = β2·v_t + (1-β2)·(∇f(θ_t))²       (RMSProp term)
θ_{t+1} = θ_t - η · m_{t+1} / (√v_{t+1} + ε)
```
(Adam also includes a "bias correction" step for `m` and `v`, since they're initialized at zero and biased toward zero early in training — omitted here for simplicity.)

## In ML/DL

- **Adam is the default optimizer for the vast majority of deep learning training today** — it's robust, requires relatively little learning-rate tuning compared to plain SGD, and works well across a huge range of architectures and problems out of the box.
```python
import torch
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)   # the most common default choice
```
- **Momentum helps escape saddle points and shallow local minima** — a real, practical problem in the high-dimensional, non-convex loss landscapes of deep neural networks (see `02-Calculus/Jacobian-Hessian.md` for why saddle points are common in high dimensions).
- **Plain SGD (sometimes with momentum) is still preferred for some tasks** (notably, some computer vision architectures) because it can generalize slightly better than Adam in certain settings, despite being harder to tune — an active area of empirical ML research and practical debate.
- **Learning rate warmup**, common in training Transformers, is often combined with Adam specifically because Adam's adaptive estimates are noisy/unreliable during the very first training steps — starting with a small learning rate and ramping up avoids instability early on.
- **Weight decay vs L2 regularization subtlety**: in Adam, naively adding an L2 penalty to the loss interacts oddly with the adaptive learning rate; "AdamW" (a very commonly used variant) decouples weight decay from the gradient-based update to fix this, and is now the standard choice for training large models (e.g., most modern LLMs use AdamW).
