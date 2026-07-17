# Practice — ML Applications

1. Build a 2-layer neural network in raw NumPy (no PyTorch/TensorFlow) — implement the forward pass AND manually derive/implement the backward pass (backpropagation) using the chain rule, for a simple regression task.
2. Compare training the same network with MSE loss vs a manually-implemented cross-entropy loss on a classification toy dataset — confirm cross-entropy is more appropriate and produces better-behaved training.
3. Train a model with and without L2 regularization (`weight_decay` in PyTorch) on a small, overfitting-prone dataset — plot training vs validation loss for both, and confirm regularization reduces the train/validation gap.
4. Implement PCA completely from scratch (as shown in `PCA.md`), apply it to a real small dataset (e.g., `sklearn.datasets.load_digits`), reduce to 2 dimensions, and visualize the result with a scatter plot colored by class label.
5. Train a linear autoencoder with a small bottleneck layer on the same dataset, and compare its learned reduced representation to your PCA result.
6. Explain in your own words, using vocabulary from earlier folders (gradient, chain rule, entropy, bias-variance): what mathematically happens, step by step, when you call `loss.backward()` followed by `optimizer.step()` in PyTorch.

✅ Done? Move to `08-Interview`.
