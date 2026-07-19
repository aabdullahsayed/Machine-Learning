# 004 - Project: Time Series Forecasting

## Concept
This project builds a complete time series forecasting pipeline: prepare a windowed dataset from raw sequential data, train an LSTM to predict future values, evaluate with proper time-aware splitting (never shuffle time series!), and visualize predictions against actuals.

## Why It Matters
Time series forecasting (demand, sales, sensor readings, stock-adjacent metrics) is one of the most common applied uses of sequence models outside of NLP, and it requires different evaluation discipline than typical i.i.d. datasets.

## Hands-On

```python
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import matplotlib.pyplot as plt

# --- Step 1: Generate a synthetic but realistic time series (trend + seasonality + noise) ---
np.random.seed(42)
n_points = 500
t = np.arange(n_points)
trend = 0.05 * t
seasonality = 10 * np.sin(2 * np.pi * t / 50)
noise = np.random.normal(0, 2, n_points)
series = trend + seasonality + noise + 50

df = pd.DataFrame({"value": series})

plt.plot(df["value"])
plt.title("Synthetic time series")
plt.savefig("raw_series.png")
plt.close()

# --- Step 2: Time-aware train/test split (NEVER shuffle time series data!) ---
train_size = int(len(df) * 0.8)
train_series = df["value"].values[:train_size]
test_series = df["value"].values[train_size:]

# --- Step 3: Scale using ONLY training statistics (avoid leaking test info) ---
train_mean, train_std = train_series.mean(), train_series.std()
train_scaled = (train_series - train_mean) / train_std
test_scaled = (test_series - train_mean) / train_std

# --- Step 4: Create windowed sequences (use past N points to predict the next point) ---
def create_windows(series, window_size=20):
    X, y = [], []
    for i in range(len(series) - window_size):
        X.append(series[i:i+window_size])
        y.append(series[i+window_size])
    return np.array(X), np.array(y)

WINDOW_SIZE = 20
X_train, y_train = create_windows(train_scaled, WINDOW_SIZE)
X_test, y_test = create_windows(np.concatenate([train_scaled[-WINDOW_SIZE:], test_scaled]), WINDOW_SIZE)

X_train_t = torch.tensor(X_train, dtype=torch.float32).unsqueeze(-1)  # (N, window, 1)
y_train_t = torch.tensor(y_train, dtype=torch.float32).unsqueeze(-1)
X_test_t = torch.tensor(X_test, dtype=torch.float32).unsqueeze(-1)
y_test_t = torch.tensor(y_test, dtype=torch.float32).unsqueeze(-1)

# --- Step 5: LSTM forecasting model ---
class LSTMForecaster(nn.Module):
    def __init__(self, hidden_size=32):
        super().__init__()
        self.lstm = nn.LSTM(1, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        out, (h_n, c_n) = self.lstm(x)
        return self.fc(h_n[-1])

model = LSTMForecaster()
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# --- Step 6: Train ---
for epoch in range(200):
    optimizer.zero_grad()
    preds = model(X_train_t)
    loss = criterion(preds, y_train_t)
    loss.backward()
    optimizer.step()
    if epoch % 40 == 0:
        print(f"Epoch {epoch}: train MSE (scaled)={loss.item():.4f}")

# --- Step 7: Evaluate and un-scale predictions back to original units ---
model.eval()
with torch.no_grad():
    test_preds_scaled = model(X_test_t).squeeze().numpy()

test_preds = test_preds_scaled * train_std + train_mean
test_actual = y_test * train_std + train_mean

rmse = np.sqrt(np.mean((test_preds - test_actual) ** 2))
print(f"Test RMSE (original scale): {rmse:.4f}")

# --- Step 8: Visualize predictions vs. actuals ---
plt.plot(test_actual, label="Actual")
plt.plot(test_preds, label="Predicted")
plt.legend()
plt.title("Time Series Forecast: LSTM predictions vs actuals")
plt.savefig("forecast_comparison.png")
```

## Exercise
1. Compare the LSTM's test RMSE against a naive baseline that just predicts "tomorrow = today" (`test_actual[:-1]` vs `test_actual[1:]`) — beating this baseline is the real bar to clear.
2. Extend the model to multi-step forecasting: predict the next 5 points at once instead of just 1 (change the output layer to `Linear(hidden_size, 5)` and adjust window creation).
3. Add exogenous features (e.g., day-of-week as an extra input channel) and see if forecast accuracy improves.

## Key Takeaways
- Time series data must be split by time, never shuffled — shuffling would let the model "see the future" during training, giving falsely optimistic results.
- Always scale using statistics computed only from the training portion, then apply that same scaling to test data.
- A naive "predict the last known value" baseline is a surprisingly strong benchmark — always compare your model against it before declaring success.
