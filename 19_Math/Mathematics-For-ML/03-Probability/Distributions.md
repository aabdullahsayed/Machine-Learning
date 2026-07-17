# Common Probability Distributions

## Math Explanation

### Bernoulli distribution
Models a single binary outcome (success/failure) with probability `p` of success.
```
P(X=1) = p,  P(X=0) = 1-p
```

### Binomial distribution
Models the number of successes in `n` independent Bernoulli trials.
```
P(X=k) = C(n,k) pᵏ (1-p)ⁿ⁻ᵏ
```

### Gaussian (Normal) distribution
The famous "bell curve" — defined by mean `μ` and variance `σ²`:
```
f(x) = (1 / √(2πσ²)) · exp(-(x-μ)² / 2σ²)
```
Central to statistics because of the **Central Limit Theorem**: the sum/average of many independent random variables tends toward a Gaussian distribution, regardless of the original distribution's shape.

### Uniform distribution
Every value in a range `[a,b]` is equally likely.

### Categorical distribution
Generalizes Bernoulli to more than 2 categories — exactly what a softmax output represents.

## In ML/DL

- **Weight initialization** (e.g., "Xavier/Glorot initialization," "He initialization") samples initial neural network weights from a carefully-scaled Gaussian or Uniform distribution — the specific scaling is mathematically derived to keep activations/gradients from vanishing or exploding early in training.
```python
import torch.nn as nn
layer = nn.Linear(100, 50)
nn.init.xavier_normal_(layer.weight)   # samples from a scaled Gaussian
```
- **Gaussian noise** is added intentionally in many contexts: data augmentation, differential privacy (adding calibrated noise to protect individual data points), and diffusion models (which literally learn to reverse a process of gradually adding Gaussian noise to images).
- **The Categorical distribution IS the softmax output** — when your model predicts `[0.7, 0.2, 0.1]` for 3 classes, it's defining a Categorical distribution over those classes.
- **Cross-entropy loss** (the most common classification loss) is derived directly from comparing two probability distributions — the true label's distribution (a "one-hot" Categorical) vs the model's predicted distribution. See `06-Information-Theory/Cross-Entropy.md`.
- **Dropout** can be modeled as each neuron following an independent Bernoulli distribution (kept/dropped) during training.
- **Variational Autoencoders (VAEs)** explicitly model latent variables as following a Gaussian distribution, and the model learns the mean/variance parameters of that distribution.
