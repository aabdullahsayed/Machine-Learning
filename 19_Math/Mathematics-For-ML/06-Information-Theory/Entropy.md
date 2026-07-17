# Entropy

## Math Explanation

**Entropy** measures the average amount of "surprise" or uncertainty in a random variable's outcomes.
```
H(X) = -Σ P(x) log(P(x))
```
(sum over all possible values `x`; using `log base 2` gives units of "bits," `log base e` gives "nats" — ML typically uses natural log)

### Intuition
- A fair coin flip (`P(heads)=0.5`) has **high** entropy — maximally unpredictable.
- A heavily biased coin (`P(heads)=0.99`) has **low** entropy — you can predict the outcome with high confidence most of the time.
- A completely certain event (`P(x)=1` for one outcome) has **zero** entropy — no surprise at all.

### Worked example
Fair coin: `H = -(0.5·log(0.5) + 0.5·log(0.5)) = -log(0.5) = log(2) ≈ 0.693 nats` (or exactly 1 bit, using log base 2).
Biased coin (`P(heads)=0.99`): `H = -(0.99·log(0.99) + 0.01·log(0.01)) ≈ 0.056 nats` — much lower, as expected.

### Maximum entropy
Entropy is **maximized** when all outcomes are equally likely (a uniform distribution) — this makes intuitive sense: maximum uncertainty happens when you have no reason to favor any particular outcome.

## In ML/DL

- **Entropy underlies cross-entropy loss** (see `Cross-Entropy.md`) — the single most common loss function for classification problems is directly built from this concept.
- **Decision tree algorithms (ID3, C4.5)** use entropy directly to decide which feature to split on at each node — choosing the split that most reduces entropy (uncertainty about the class label) is called **"information gain"**:
```
Information Gain = H(parent node) - Σ (weighted) H(child nodes)
```
The feature/split that maximizes information gain (most reduces uncertainty) is chosen at each step of building the tree.
- **Model confidence/calibration**: a well-calibrated classifier's predicted probability distribution should have entropy that reflects genuine uncertainty — overconfident models (very low entropy predictions, even when wrong) are a real, diagnosable problem in deployed ML systems.
- **Exploration strategies in Reinforcement Learning**: "entropy regularization" (encouraging a policy's action distribution to maintain higher entropy) is a common technique to prevent an RL agent from prematurely converging to a suboptimal, overly-deterministic strategy, encouraging continued exploration.
```python
import numpy as np
def entropy(probs):
    probs = np.array(probs)
    return -np.sum(probs * np.log(probs + 1e-12))   # small epsilon avoids log(0)

print(entropy([0.5, 0.5]))         # high entropy (max uncertainty for 2 outcomes)
print(entropy([0.99, 0.01]))        # low entropy (confident prediction)
```
