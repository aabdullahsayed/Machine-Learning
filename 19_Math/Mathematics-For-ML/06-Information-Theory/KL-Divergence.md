# KL Divergence

## Math Explanation

**Kullback-Leibler (KL) Divergence** measures how different one probability distribution `q` is from a reference distribution `p` — it's a measure of "information lost" when you use `q` to approximate `p`.
```
D_KL(p || q) = Σ p(x) log( p(x) / q(x) )
```

### Relationship to entropy and cross-entropy
```
D_KL(p || q) = H(p, q) - H(p)
             = (cross-entropy)  -  (entropy of the true distribution)
```
This reveals something important: **since `H(p)` (the true distribution's own entropy) doesn't depend on your model at all**, minimizing cross-entropy `H(p,q)` and minimizing KL divergence `D_KL(p||q)` are **equivalent optimization problems** — they differ only by a constant that doesn't affect where the minimum is. This is exactly why you'll see both cross-entropy loss AND KL divergence loss used somewhat interchangeably in different ML contexts.

### Key properties
- `D_KL(p || q) ≥ 0` always, and `= 0` only when `p` and `q` are identical distributions.
- **NOT symmetric**: `D_KL(p || q) ≠ D_KL(q || p)` in general — this asymmetry has real practical consequences for which direction you choose in certain ML applications (discussed below).

## In ML/DL

- **Variational Autoencoders (VAEs)**: the training objective (the "ELBO," evidence lower bound) explicitly includes a KL divergence term `D_KL(q(z|x) || p(z))`, pushing the learned latent distribution `q` (produced by the encoder) to stay close to a chosen prior distribution `p` (typically a standard Gaussian) — this is what gives VAEs their smooth, well-structured latent space.
- **Knowledge distillation**: training a smaller "student" model to mimic a larger "teacher" model's output probability distribution uses KL divergence between the student's and teacher's predicted distributions as (part of) the loss function.
- **Reinforcement Learning (PPO, TRPO algorithms)**: these popular policy-gradient RL algorithms explicitly constrain how much the policy is allowed to change in a single update step, measured via KL divergence between the old and new policy distributions — this constraint is what makes PPO trust-region-based training much more stable than naive policy gradient methods.
- **The asymmetry matters in practice**: `D_KL(p_data || q_model)` ("forward KL," minimized by standard maximum-likelihood/cross-entropy training) tends to produce models that spread probability mass broadly, covering all modes of the true data distribution ("mode-covering"). `D_KL(q_model || p_data)` ("reverse KL," used in some variational inference and GAN-adjacent methods) tends to produce models that concentrate on just one or a few modes, ignoring others ("mode-seeking"). Understanding this distinction explains real, observable behavioral differences between models trained with different objectives.

```python
import numpy as np
def kl_divergence(p, q):
    p, q = np.array(p), np.array(q)
    return np.sum(p * np.log((p + 1e-12) / (q + 1e-12)))

p = [0.5, 0.5]
q = [0.9, 0.1]
print(kl_divergence(p, q))   # measures how much q diverges from p
```
