# 05 — Beyond Vanilla GD: Momentum, AdaGrad, RMSProp, Adam

Plain gradient descent treats every step independently — it has no memory
of where it's been. Modern optimizers fix specific weaknesses by adding
"memory" of past gradients.

## 1. Momentum — "the rolling ball remembers its speed"

**Analogy**: A ball rolling downhill doesn't stop and re-decide direction
at every instant — it builds up speed (inertia) in a consistent direction
and can even roll *through* small bumps and flat saddle regions.

```
v := β·v + (1 − β)·∇J(θ)        (velocity = blend of old velocity + new gradient)
θ := θ − α·v
```

| Symbol | Meaning |
|---|---|
| `v` | velocity (accumulated, decaying average of past gradients) |
| `β` | momentum coefficient, typically 0.9 (how much past velocity is kept) |

```
Without momentum (zig-zag on a narrow valley):     With momentum (smoothed path):

   \  /\  /\  /\                                      \
    \/  \/  \/  \                                       \___
                  \______minimum                             \____minimum
```

## 2. AdaGrad — "give tired dimensions a bigger stride"

**Analogy**: If one direction on the trail has always been gently sloped
(small historical gradients), give it a relatively bigger step; if another
direction has been steep and jumpy (large historical gradients), tone
its steps down. AdaGrad **adapts the learning rate per-parameter**.

```
G := G + (∇J(θ))²                         (accumulate squared gradients, per param)
θ := θ − (α / (√G + ε)) · ∇J(θ)
```

- ✅ Great for sparse features (e.g. text/NLP with rare words)
- ❌ `G` only grows, so the effective learning rate shrinks to near-zero
  over long training runs (learning can stall)

## 3. RMSProp — "AdaGrad with a short memory"

Fixes AdaGrad's ever-shrinking learning rate by using a **decaying**
(exponentially weighted moving) average of squared gradients instead of an
ever-growing sum.

```
E[g²] := β·E[g²] + (1 − β)·(∇J(θ))²
θ     := θ − (α / (√E[g²] + ε)) · ∇J(θ)
```

## 4. Adam (Adaptive Moment Estimation) — momentum + RMSProp combined

The most widely used optimizer in deep learning today. It keeps **both**:
- a decaying average of past gradients (like momentum) → called `m`
- a decaying average of past *squared* gradients (like RMSProp) → called `v`

```
m := β1·m + (1 − β1)·g              (1st moment: mean of gradients)
v := β2·v + (1 − β2)·g²             (2nd moment: uncentered variance)

m̂ := m / (1 − β1^t)                 (bias correction, since m,v start at 0)
v̂ := v / (1 − β2^t)

θ := θ − α · m̂ / (√v̂ + ε)
```

Typical defaults: `β1 = 0.9`, `β2 = 0.999`, `ε = 1e-8`, `α = 0.001`.

## Comparison table

| Optimizer | Adapts per-parameter LR? | Uses momentum? | Common use | Main weakness |
|---|---|---|---|---|
| Plain (vanilla) GD | ❌ | ❌ | teaching, simple convex problems | slow, zig-zags on uneven surfaces |
| Momentum | ❌ | ✅ | speeding up plain GD | still one global LR |
| AdaGrad | ✅ | ❌ | sparse data (NLP, text) | learning rate can vanish over time |
| RMSProp | ✅ | ❌ | RNNs, non-stationary problems | no momentum term |
| **Adam** | ✅ | ✅ | default choice for most deep learning | can generalize slightly worse than tuned SGD+momentum in some cases |

## Visual summary: paths on a valley with a narrow, curved floor

```
Plain GD           Momentum            RMSProp/AdaGrad        Adam
  \  /\  /\           \                    \                     \
   \/  \/  \            \___                 \___                  \__
             \_______        \____min             \____min             \___min
   (slow zig-zag)      (smoother, faster)      (per-dim scaled)     (best of both)
```

## Which one should I actually use?

```
                     ┌─────────────────────────────┐
                     │ Is this a learning exercise  │
                     │ or a simple convex problem?  │
                     └───────────────┬───────────────┘
                          yes │             │ no
                              ▼             ▼
                    Plain/Batch GD    ┌───────────────────┐
                    (as in file 02)   │ Deep learning /    │
                                      │ neural network?    │
                                      └─────────┬──────────┘
                                          yes │        │ no
                                              ▼        ▼
                                            Adam     Momentum-SGD
                                       (great default)  or RMSProp
```
