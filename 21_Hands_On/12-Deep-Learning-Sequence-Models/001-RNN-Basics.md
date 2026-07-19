# 001 - RNN Basics

## Concept
A Recurrent Neural Network processes a sequence one step at a time, maintaining a hidden state that carries information from previous steps forward. This lets it handle variable-length sequential data (text, time series, audio) where order matters.

## Why It Matters
RNNs introduced the idea of "memory" into neural networks, which is foundational to everything sequence-related — even though LSTMs/GRUs (next lesson) and Transformers have mostly replaced vanilla RNNs in practice, the core recurrence idea still shows up everywhere.

## Hands-On

```python
import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt

# 1. A manual RNN cell, step by step, to see exactly what "recurrence" means
def rnn_cell_forward(x_t, h_prev, Wxh, Whh, bh):
    """One time step: combine current input and previous hidden state."""
    h_t = np.tanh(x_t @ Wxh + h_prev @ Whh + bh)
    return h_t

np.random.seed(0)
input_size, hidden_size = 3, 4
Wxh = np.random.randn(input_size, hidden_size) * 0.1
Whh = np.random.randn(hidden_size, hidden_size) * 0.1
bh = np.zeros(hidden_size)

sequence = np.random.randn(5, input_size)  # 5 time steps
h = np.zeros(hidden_size)                  # initial hidden state

hidden_states = []
for t in range(len(sequence)):
    h = rnn_cell_forward(sequence[t], h, Wxh, Whh, bh)
    hidden_states.append(h.copy())
    print(f"t={t}: hidden state = {np.round(h, 3)}")

# Notice: h at each step depends on ALL previous inputs through the recurrence

# 2. PyTorch's built-in RNN, applied to a toy sequence classification task
# Task: classify whether a sequence of numbers is mostly increasing or decreasing
def make_sequence_dataset(n_samples=500, seq_len=10):
    X, y = [], []
    for _ in range(n_samples):
        trend = np.random.choice([1, -1])
        seq = np.cumsum(np.random.randn(seq_len) * 0.5 + trend * 0.3)
        X.append(seq)
        y.append(1 if trend == 1 else 0)
    X = np.array(X).reshape(n_samples, seq_len, 1)  # (batch, seq_len, features)
    y = np.array(y)
    return torch.tensor(X, dtype=torch.float32), torch.tensor(y, dtype=torch.long)

X, y = make_sequence_dataset()
X_train, y_train = X[:400], y[:400]
X_test, y_test = X[400:], y[400:]

class SimpleRNNClassifier(nn.Module):
    def __init__(self, input_size=1, hidden_size=16, num_classes=2):
        super().__init__()
        self.rnn = nn.RNN(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        out, h_n = self.rnn(x)          # out: all time steps, h_n: final hidden state
        last_hidden = h_n[-1]            # use the final hidden state for classification
        return self.fc(last_hidden)

model = SimpleRNNClassifier()
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

for epoch in range(100):
    optimizer.zero_grad()
    outputs = model(X_train)
    loss = criterion(outputs, y_train)
    loss.backward()
    optimizer.step()
    if epoch % 20 == 0:
        print(f"Epoch {epoch}: loss={loss.item():.4f}")

with torch.no_grad():
    test_preds = model(X_test).argmax(dim=1)
    accuracy = (test_preds == y_test).float().mean().item()
print("Test accuracy:", accuracy)
```

## Exercise
1. Change `seq_len` to 50 and re-train — does accuracy drop? This hints at the vanishing gradient problem RNNs suffer with long sequences (solved by LSTM/GRU, next lesson).
2. Modify `SimpleRNNClassifier` to use `out` (all time steps) with mean pooling instead of just the last hidden state — compare performance.
3. Print the norm of the hidden state (`np.linalg.norm(h)`) at each of the 5 manual time steps — does it grow, shrink, or stay stable?

## Key Takeaways
- The same weights (`Wxh`, `Whh`) are reused at every time step — this is what lets RNNs handle sequences of any length with a fixed number of parameters.
- The final hidden state is a compressed summary of the entire sequence seen so far — useful for classification tasks that only need one output per sequence.
- Vanilla RNNs struggle with long sequences due to vanishing/exploding gradients through many recurrent steps — this motivates LSTM and GRU architectures.
