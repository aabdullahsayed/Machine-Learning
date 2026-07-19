# 002 - LSTM and GRU

## Concept
LSTM (Long Short-Term Memory) and GRU (Gated Recurrent Unit) are RNN variants that use learnable "gates" to control what information is kept, forgotten, or output at each time step, which solves vanilla RNNs' vanishing gradient problem on long sequences.

## Why It Matters
Before Transformers took over, LSTMs and GRUs were the standard for any serious sequence task (translation, speech recognition, time series). They're still widely used today, especially for smaller-scale or resource-constrained sequence problems.

## Hands-On

```python
import torch
import torch.nn as nn
import numpy as np

# 1. LSTM gates, illustrated conceptually with the equations (not full manual implementation)
"""
At each time step t, given input x_t and previous (h_{t-1}, c_{t-1}):

  forget_gate  f_t = sigmoid(W_f @ [h_{t-1}, x_t] + b_f)   # what to forget from cell state
  input_gate   i_t = sigmoid(W_i @ [h_{t-1}, x_t] + b_i)   # what new info to add
  candidate    g_t = tanh(W_g @ [h_{t-1}, x_t] + b_g)      # candidate new values
  output_gate  o_t = sigmoid(W_o @ [h_{t-1}, x_t] + b_o)   # what to output

  cell state   c_t = f_t * c_{t-1} + i_t * g_t             # the "long-term memory" pathway
  hidden state h_t = o_t * tanh(c_t)

The cell state c_t is the key innovation: it's a near-linear pathway across time steps,
which lets gradients flow back through many steps without vanishing as badly as vanilla RNNs.
"""

# 2. Build a sequence dataset (same pattern-recognition task as lesson 001, but longer)
def make_sequence_dataset(n_samples=500, seq_len=40):
    X, y = [], []
    for _ in range(n_samples):
        trend = np.random.choice([1, -1])
        seq = np.cumsum(np.random.randn(seq_len) * 0.5 + trend * 0.2)
        X.append(seq)
        y.append(1 if trend == 1 else 0)
    X = np.array(X).reshape(n_samples, seq_len, 1)
    y = np.array(y)
    return torch.tensor(X, dtype=torch.float32), torch.tensor(y, dtype=torch.long)

X, y = make_sequence_dataset()
X_train, y_train = X[:400], y[:400]
X_test, y_test = X[400:], y[400:]

# 3. LSTM-based classifier
class LSTMClassifier(nn.Module):
    def __init__(self, input_size=1, hidden_size=32, num_classes=2):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        out, (h_n, c_n) = self.lstm(x)   # LSTM returns hidden AND cell state
        return self.fc(h_n[-1])

# 4. GRU-based classifier - simpler gating (no separate cell state), often similar performance
class GRUClassifier(nn.Module):
    def __init__(self, input_size=1, hidden_size=32, num_classes=2):
        super().__init__()
        self.gru = nn.GRU(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        out, h_n = self.gru(x)           # GRU only returns hidden state, no cell state
        return self.fc(h_n[-1])

def train_and_evaluate(model, X_train, y_train, X_test, y_test, epochs=100):
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    for epoch in range(epochs):
        optimizer.zero_grad()
        loss = criterion(model(X_train), y_train)
        loss.backward()
        optimizer.step()
    with torch.no_grad():
        acc = (model(X_test).argmax(1) == y_test).float().mean().item()
    return acc

lstm_model = LSTMClassifier()
gru_model = GRUClassifier()

lstm_acc = train_and_evaluate(lstm_model, X_train, y_train, X_test, y_test)
gru_acc = train_and_evaluate(gru_model, X_train, y_train, X_test, y_test)

print(f"LSTM test accuracy: {lstm_acc:.4f}")
print(f"GRU test accuracy: {gru_acc:.4f}")

# 5. Parameter count comparison - GRU has fewer gates, so fewer parameters
lstm_params = sum(p.numel() for p in lstm_model.parameters())
gru_params = sum(p.numel() for p in gru_model.parameters())
print(f"LSTM parameters: {lstm_params:,}")
print(f"GRU parameters: {gru_params:,}")

# 6. Bidirectional LSTM - reads the sequence both forward and backward
bilstm = nn.LSTM(input_size=1, hidden_size=32, batch_first=True, bidirectional=True)
sample_out, (h_n, c_n) = bilstm(X_train[:2])
print("Bidirectional LSTM output shape:", sample_out.shape)  # hidden_size * 2 in last dim
```

## Exercise
1. Re-run lesson 001's vanilla RNN on this same 40-step dataset and compare its accuracy to LSTM/GRU — does the gap widen compared to the shorter 5-10 step sequences?
2. Stack two LSTM layers (`num_layers=2` in `nn.LSTM`) and see if it improves accuracy on this task.
3. Explain in your own words why GRU has fewer parameters than LSTM (hint: count the gates in each).

## Key Takeaways
- LSTM's separate cell state `c_t` provides a more direct gradient pathway across time, which is why it handles longer sequences much better than vanilla RNNs.
- GRU merges the forget and input gates into one "update gate" and has no separate cell state — fewer parameters, often comparable performance, and generally faster to train.
- Both are largely superseded by Transformer-based architectures for large-scale NLP (module 13), but remain strong choices for smaller sequence problems, especially time series.
