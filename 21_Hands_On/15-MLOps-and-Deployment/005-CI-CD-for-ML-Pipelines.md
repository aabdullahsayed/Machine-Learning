# 005 - CI/CD for ML Pipelines

## Concept
Continuous Integration/Continuous Deployment (CI/CD) automates testing and deploying code changes. For ML, this extends to automatically testing data quality, model performance, and reproducibility every time code or data changes, before a new model reaches production.

## Why It Matters
Manual deployment ("I'll just copy the new model file to the server") is how silent regressions and outages happen. CI/CD catches problems before they reach users and makes deployments boring and repeatable — which is exactly what you want.

## Hands-On

```yaml
# ============================================
# .github/workflows/ml-ci.yml - GitHub Actions pipeline
# ============================================
name: ML CI Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test-and-validate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run unit tests
        run: pytest tests/ -v

      - name: Run data validation checks
        run: python scripts/validate_data.py

      - name: Train and evaluate model
        run: python scripts/train.py

      - name: Check model meets minimum performance bar
        run: python scripts/check_model_quality.py

      - name: Build Docker image
        run: docker build -t ml-api:${{ github.sha }} .

  deploy:
    needs: test-and-validate
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to production
        run: echo "Push image to registry and trigger deployment (details depend on your cloud provider)"
```

```python
# scripts/check_model_quality.py - a "gate" that fails CI if the model regresses
import joblib
import json
from sklearn.metrics import accuracy_score

MINIMUM_ACCEPTABLE_ACCURACY = 0.90

model = joblib.load("model.joblib")

# Load a fixed, version-controlled evaluation set (not the live training data!)
import pandas as pd
eval_data = pd.read_csv("data/eval_holdout.csv")
X_eval = eval_data.drop(columns=["target"])
y_eval = eval_data["target"]

accuracy = accuracy_score(y_eval, model.predict(X_eval))
print(f"Evaluation accuracy: {accuracy:.4f}")

if accuracy < MINIMUM_ACCEPTABLE_ACCURACY:
    raise SystemExit(f"FAILED: accuracy {accuracy:.4f} is below the minimum bar {MINIMUM_ACCEPTABLE_ACCURACY}")

print("PASSED: model meets the minimum quality bar.")
```

```python
# tests/test_model.py - unit tests pytest will run in CI
import joblib
import numpy as np
import pytest

@pytest.fixture
def model():
    return joblib.load("model.joblib")

def test_model_loads(model):
    assert model is not None

def test_model_predicts_correct_shape(model):
    X = np.random.rand(5, model.n_features_in_)
    preds = model.predict(X)
    assert preds.shape == (5,)

def test_model_output_is_valid_class(model):
    X = np.random.rand(3, model.n_features_in_)
    preds = model.predict(X)
    assert set(preds).issubset({0, 1})

def test_predict_proba_sums_to_one(model):
    X = np.random.rand(3, model.n_features_in_)
    probas = model.predict_proba(X)
    assert np.allclose(probas.sum(axis=1), 1.0)
```

## Exercise
1. Write one more test that checks the model's prediction on a known input matches an expected output (a "regression test" for the model itself).
2. Add a step to the workflow that fails the pipeline if any feature in the training data has more than 5% missing values.
3. Sketch (in comments/pseudocode) how you'd add a "shadow deployment" step where a new model runs alongside the old one on live traffic without serving its predictions yet.

## Key Takeaways
- ML CI/CD tests three things regular software CI doesn't: data quality, model performance against a fixed bar, and reproducibility of the training process.
- A "quality gate" script that fails the build when accuracy drops below a threshold prevents accidentally shipping a worse model.
- Keeping a fixed, version-controlled evaluation set (separate from the ever-growing training data) is essential — otherwise your quality bar silently drifts too.
