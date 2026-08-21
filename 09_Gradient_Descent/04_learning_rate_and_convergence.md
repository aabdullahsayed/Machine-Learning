# 04 — Learning Rate, Convergence & Traps

## Analogy: step size of the hiker

The learning rate `α` is literally **how big a step** the hiker takes each
time. This single number can make or break training.

```
TOO SMALL (α tiny)              JUST RIGHT (α good)             TOO LARGE (α huge)
                                                                   
start                            start                            start
 \                                 \                              /\
  \                                 \                            /  \
   \.                                \___                       /    \
    \.                                    \___minimum          /      \
     \.                                                        /        \
      \. (takes forever,                                      /  bounces around,
       \  tiny shuffling steps)                               /   might diverge to infinity!
        \.....minimum (eventually)
```

| Learning rate | Symptom | Fix |
|---|---|---|
| Too small | Loss decreases painfully slowly, training takes forever | Increase α, or use an adaptive optimizer |
| Too large | Loss oscillates wildly, or explodes to `NaN`/infinity (diverges) | Decrease α |
| Just right | Loss decreases smoothly and reasonably fast | 🎉 |

## Visualizing on the loss curve (loss vs. training step)

```
Loss
 │  too-large α: bounces / diverges
 │    /\    /\
 │   /  \  /  \      /\
 │  /    \/    \    /  \
 │ /            \  /    \___________ (never settles, or explodes)
 │
 │  too-small α: crawls down forever
 │  \
 │   \___
 │       \____
 │            \_____
 │                  \______________________ (barely moving after many steps)
 │
 │  good α: fast, smooth decay
 │  \
 │   \_
 │     \__
 │        \____
 │             \__________  <- converged
 └───────────────────────────────────────── training steps
```

## How do we know we've "converged"?

Common stopping criteria:

1. **Gradient near zero**: `‖∇J(θ)‖ < ε` (the ground feels flat)
2. **Loss change is tiny**: `|J(θ_t) − J(θ_{t-1})| < ε`
3. **Fixed iteration budget**: just run N steps (simplest, common in practice)
4. **Validation loss stops improving**: "early stopping" — halt before overfitting

## Convex vs. non-convex loss surfaces

| | Convex (e.g. linear/logistic regression) | Non-convex (e.g. deep neural nets) |
|---|---|---|
| Shape | single bowl | mountain range with many dips |
| Local minima | none other than the global one | many |
| Saddle points | none | common, especially in high dimensions |
| Guarantee | GD *will* reach the global minimum (with suitable α) | GD may get stuck; often fine in practice anyway |

```
CONVEX (one bowl)                    NON-CONVEX (bumpy landscape)

  \                /                  \  /\      /\        /
   \              /                    \/  \    /  \  /\  /
    \            /                          \  /    \/  \/
     \          /                            \/
      \        /                     local   global   local
       \______/                      min      min     min
      global minimum                  ↑ gradient descent can get
      (only minimum)                    trapped here if it starts nearby!
```

**In practice**, deep learning still works remarkably well despite
non-convexity, because (a) most local minima in high dimensions turn out to
have similar, good loss values, and (b) techniques like momentum and
stochastic noise help escape shallow traps and saddle points.

## Saddle points — the sneaky trap

A saddle point has zero gradient (flat in some directions) but is
**not** a minimum — it curves up in one direction and down in another,
like a horse saddle or a mountain pass.

```
        ___
       /   \___
      /        \___          <- flat "pass" in the middle:
_____/             \___          gradient ≈ 0, but NOT a minimum!
                       \___
                           \
```

Plain gradient descent can slow to a crawl near saddle points because the
gradient shrinks toward zero even though we haven't actually minimized
anything yet. This is one of the big motivations for **momentum**
(see file `05`) — it carries speed through these flat regions.

## Practical tips

- Start with `α` around `0.01`–`0.1` for simple models; for deep nets,
  common starting points are `0.001` (Adam) or `0.01`–`0.1` (SGD+momentum).
- Use a **learning rate schedule**: start larger, decay over time
  (e.g. halve `α` every N epochs) — big steps early to cover ground fast,
  small steps later to fine-tune near the minimum.
- **Normalize/scale your features first!** Unscaled features (e.g. one
  ranging 0–1, another 0–1,000,000) create an elongated, stretched bowl
  that makes a single learning rate awkward for all dimensions:

```
Unscaled features (elongated bowl)     Scaled features (round bowl)
    _______________                          ___
   /               \                        /   \
  /                 \        vs.           |     |
  \                 /                       \___ /
   \_______________/
   GD zig-zags across the narrow axis      GD moves efficiently in all directions
```
