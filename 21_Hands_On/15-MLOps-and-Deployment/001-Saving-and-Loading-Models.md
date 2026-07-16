# 001 - Saving and Loading Models

## Concept
A trained model only has value if you can save it to disk and load it back later without retraining. Different libraries have different recommended serialization formats — pickle/joblib for scikit-learn, `state_dict` for PyTorch, `SavedModel`/`.h5` for TensorFlow/Keras.

## Why It Matters
This is the first and most basic step of "deployment" — before an API, before Docker, before anything else, you need a reliable way to persist a model and reload it identically.

## Hands-On

```python
import joblib
import pickle
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

data = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
print("Original accuracy:", model.score(X_test, y_test))

# 1. joblib - preferred for scikit-learn models (efficient with large NumPy arrays)
joblib.dump(model, "model.joblib")
loaded_joblib = joblib.load("model.joblib")
print("Joblib-loaded accuracy:", loaded_joblib.score(X_test, y_test))

# 2. pickle - the general-purpose Python serialization format
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)
with open("model.pkl", "rb") as f:
    loaded_pickle = pickle.load(f)
print("Pickle-loaded accuracy:", loaded_pickle.score(X_test, y_test))

# 3. Saving a preprocessing pipeline alongside the model (avoids mismatches)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

full_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", RandomForestClassifier(n_estimators=100, random_state=42)),
])
full_pipeline.fit(X_train, y_train)
joblib.dump(full_pipeline, "full_pipeline.joblib")
# Loading this ONE file guarantees identical preprocessing at inference time.

# 4. PyTorch: save/load state_dict (the recommended way, not the whole model object)
import torch
import torch.nn as nn

class TinyNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(30, 2)
    def forward(self, x):
        return self.fc(x)

torch_model = TinyNet()
torch.save(torch_model.state_dict(), "torch_model.pth")

# To reload: must recreate the architecture first, then load weights into it
reloaded_torch_model = TinyNet()
reloaded_torch_model.load_state_dict(torch.load("torch_model.pth"))
reloaded_torch_model.eval()
print("PyTorch model reloaded and set to eval mode.")

# 5. Versioning: always save metadata alongside the model
import json
metadata = {
    "model_type": "RandomForestClassifier",
    "sklearn_version": "1.4.0",
    "trained_on": "breast_cancer dataset",
    "test_accuracy": model.score(X_test, y_test),
    "n_features": X_train.shape[1],
}
with open("model_metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)
```

## Exercise
1. Save a model with one scikit-learn version installed and try loading it after upgrading scikit-learn (if possible in your environment) — note any warnings about version mismatches.
2. Write a `load_model_safely(path, expected_features)` function that loads a model and raises a clear error if `expected_features` doesn't match `model.n_features_in_`.
3. Compare file sizes of `joblib.dump` with `compress=3` vs. no compression on a large Random Forest.

## Key Takeaways
- **Never** unpickle a model file from an untrusted source — pickle can execute arbitrary code on load.
- Save the *pipeline* (preprocessing + model), not just the raw model, to guarantee consistent behavior at inference time.
- Always save metadata (library versions, training date, metrics) next to the model file — "which model is this and how good was it" is a question you'll ask constantly in production.
