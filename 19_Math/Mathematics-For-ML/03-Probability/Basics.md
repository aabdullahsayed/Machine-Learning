# Probability Basics

## Math Explanation

**Probability** measures how likely an event is, on a scale from 0 (impossible) to 1 (certain).

### Core rules
- `P(A)` = probability of event A, always `0 ≤ P(A) ≤ 1`
- `P(not A) = 1 - P(A)` (complement rule)
- `P(A or B) = P(A) + P(B) - P(A and B)` (avoid double-counting overlap)
- `P(A and B) = P(A) · P(B)` **only if A and B are independent**
- `P(A | B)` = probability of A **given that** B has occurred ("conditional probability")

### Conditional probability
```
P(A | B) = P(A and B) / P(B)
```
This says: among all the times B happens, what fraction of those times does A also happen?

### Independence
Events A and B are **independent** if knowing one occurred tells you nothing about the other:
```
P(A | B) = P(A)   ⟺   P(A and B) = P(A)·P(B)
```

## In ML/DL

- **Every prediction from a classifier is (or should be interpreted as) a probability.** A softmax output `[0.7, 0.2, 0.1]` for classes `[cat, dog, bird]` means "70% confident it's a cat" — literally `P(class = cat | input image)`.
- **Naive Bayes classifiers** apply the independence assumption directly: `P(features | class)` is computed by (naively) assuming each feature is independent given the class, making the joint probability a simple product.
- **Dropout** (a regularization technique) can be understood probabilistically — each neuron is independently "kept" with probability `p` during training, approximating an ensemble of many different sub-networks.
- **Data augmentation and sampling strategies** in training pipelines rely on understanding probability distributions over your dataset (e.g., ensuring class balance, or sampling proportional to some importance weight).
- **A/B testing and model evaluation** (comparing whether Model A is really better than Model B, not just by chance) fundamentally relies on probability and statistics (see `04-Statistics/Hypothesis-Testing.md`).
