# Practice — Information Theory

1. Implement `entropy()` from scratch and compute the entropy of: a fair coin, a heavily biased coin (`p=0.95`), and a fair 6-sided die. Order them by entropy — does the ordering match your intuition?
2. Implement `cross_entropy_loss()` from scratch (as in `Cross-Entropy.md`) and confirm it matches PyTorch's `nn.CrossEntropyLoss` output on a small example.
3. Implement `kl_divergence()` from scratch. Compute `D_KL(p||q)` and `D_KL(q||p)` for two different distributions `p` and `q`, and confirm they're NOT equal (demonstrating the asymmetry).
4. Verify numerically that `D_KL(p||q) = H(p,q) - H(p)` for a chosen `p` and `q`, using your `entropy()`, `cross_entropy_loss()`, and `kl_divergence()` functions together.
5. Build a tiny decision tree stump (one split) on a toy dataset, computing information gain by hand for 2-3 candidate splits, and confirm the split with the highest information gain is the one a real decision tree implementation (e.g., `sklearn.tree.DecisionTreeClassifier(max_depth=1)`) would choose.
6. Explain in your own words: why does cross-entropy loss penalize a confident WRONG prediction so much more harshly than an unconfident wrong prediction?

✅ Done? Move to `07-ML-Applications`.
