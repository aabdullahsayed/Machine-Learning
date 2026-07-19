# 006 - Intro to PyTorch or TensorFlow

## Concept
PyTorch and TensorFlow/Keras are the two dominant deep learning frameworks. Both give you automatic differentiation (no manual backprop like lesson 003) and GPU acceleration. This lesson builds the exact same network in both so you can see how the same ideas map to each framework's API.

## Why It Matters
Every deep learning module after this one (CNNs, RNNs, Transformers) is built on top of one of these frameworks. PyTorch is more common in research and increasingly in industry; Keras/TensorFlow is prized for its simplicity and production tooling. Knowing both makes you framework-agnostic.

## Hands-On

```python
# pip install torch tensorflow --break-system-packages
import numpy as np
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

X, y = make_moons(n_samples=1000, noise=0.2, random_state=42)
X = StandardScaler().fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ============================================
# 1. PyTorch version
# ============================================
import torch
import torch.nn as nn
import torch.optim as optim

X_train_t = torch.tensor(X_train, dtype=torch.float32)
y_train_t = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1)
X_test_t = torch.tensor(X_test, dtype=torch.float32)
y_test_t = torch.tensor(y_test, dtype=torch.float32).unsqueeze(1)

class TorchMLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(2, 16), nn.ReLU(),
            nn.Linear(16, 8), nn.ReLU(),
            nn.Linear(8, 1), nn.Sigmoid(),
        )
    def forward(self, x):
        return self.net(x)

torch_model = TorchMLP()
criterion = nn.BCELoss()
optimizer = optim.Adam(torch_model.parameters(), lr=0.01)

for epoch in range(200):
    optimizer.zero_grad()
    outputs = torch_model(X_train_t)
    loss = criterion(outputs, y_train_t)
    loss.backward()          # automatic differentiation - no manual backprop needed
    optimizer.step()
    if epoch % 50 == 0:
        print(f"[PyTorch] Epoch {epoch}: loss={loss.item():.4f}")

with torch.no_grad():
    preds = (torch_model(X_test_t) > 0.5).float()
    torch_accuracy = (preds == y_test_t).float().mean().item()
print("PyTorch test accuracy:", torch_accuracy)

# ============================================
# 2. TensorFlow / Keras version
# ============================================
import tensorflow as tf
from tensorflow import keras

keras_model = keras.Sequential([
    keras.layers.Input(shape=(2,)),
    keras.layers.Dense(16, activation="relu"),
    keras.layers.Dense(8, activation="relu"),
    keras.layers.Dense(1, activation="sigmoid"),
])

keras_model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
history = keras_model.fit(X_train, y_train, epochs=200, verbose=0)

keras_loss, keras_accuracy = keras_model.evaluate(X_test, y_test, verbose=0)
print("Keras test accuracy:", keras_accuracy)

# ============================================
# 3. Side-by-side comparison of the mental model
# ============================================
comparison = """
                    PyTorch                         Keras/TensorFlow
Model definition    class + forward()                Sequential([...]) or Functional API
Training loop        manual (you write the loop)      model.fit() handles it
Loss + backward       loss.backward()                  handled internally by .fit()
Weight update          optimizer.step()                 handled internally by .fit()
Inference mode       model.eval() + torch.no_grad()   automatic in model.predict()
"""
print(comparison)
```

## Exercise
1. Train both models for 500 epochs instead of 200 and compare final accuracy — do they converge to similar results?
2. Rewrite the Keras model using the Functional API (`keras.Input` + calling layers as functions) instead of `Sequential`.
3. Add a `keras.callbacks.EarlyStopping` callback and a PyTorch manual early-stopping check (track best validation loss, stop if it doesn't improve for N epochs) — compare the two approaches.

## Key Takeaways
- PyTorch gives you an explicit training loop (more control, more code); Keras's `.fit()` handles the loop for you (less code, less visibility into what's happening).
- Both use automatic differentiation under the hood — you never again need to manually derive gradients like in lesson 003, though understanding that lesson makes debugging much easier.
- Choice of framework is largely about ecosystem and team preference — the underlying deep learning concepts (layers, activations, loss, optimizer) are identical.
