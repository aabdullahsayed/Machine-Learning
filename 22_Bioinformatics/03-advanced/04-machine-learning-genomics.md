# 04 — Machine Learning for Genomics

Once you can generate clean tabular data (expression matrices, variant tables, sequence features), standard ML applies — with some domain-specific feature engineering.

## Use case 1: classify samples by gene expression (e.g. cancer subtype)

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler

expr = pd.read_csv("count_matrix.csv", index_col=0).T   # samples x genes
labels = pd.read_csv("sample_labels.csv", index_col=0)["subtype"]

X_train, X_test, y_train, y_test = train_test_split(
    expr, labels, test_size=0.2, stratify=labels, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

clf = RandomForestClassifier(n_estimators=300, random_state=42)
clf.fit(X_train_scaled, y_train)

preds = clf.predict(X_test_scaled)
print(classification_report(y_test, preds))

# Which genes matter most?
importances = pd.Series(clf.feature_importances_, index=expr.columns)
print(importances.sort_values(ascending=False).head(15))
```

High-dimensional gotcha: with ~20,000 genes and often only tens/hundreds of samples, always do feature selection or dimensionality reduction (PCA, top-variance genes) before or alongside modeling to avoid overfitting.

## Use case 2: DNA sequence classification (k-mer features)

Turn variable-length sequences into fixed-length numeric vectors so standard ML models can use them.

```python
from itertools import product
import numpy as np

def kmer_featurize(seq: str, k: int = 4) -> np.ndarray:
    all_kmers = ["".join(p) for p in product("ACGT", repeat=k)]
    counts = {kmer: 0 for kmer in all_kmers}
    for i in range(len(seq) - k + 1):
        kmer = seq[i:i+k]
        if kmer in counts:
            counts[kmer] += 1
    total = sum(counts.values()) or 1
    return np.array([counts[kmer] / total for kmer in all_kmers])

seqs = ["ATGGCCATTGTA", "GGGATCCATGGC", "ATGACCATTGTA"]
X = np.array([kmer_featurize(s, k=3) for s in seqs])
print(X.shape)   # (3, 64) - 4^3 possible 3-mers
```

Feed `X` into any scikit-learn classifier (e.g. distinguishing promoter vs non-promoter sequences, viral vs. human reads).

## Use case 3: predicting variant pathogenicity (structured features)

```python
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier

variants = pd.read_csv("annotated_variants.csv")
# example engineered features: conservation score, allele frequency, predicted impact, CADD score
features = ["conservation_score", "allele_frequency", "cadd_score", "is_coding"]
X = variants[features]
y = variants["is_pathogenic"]

model = GradientBoostingClassifier()
model.fit(X, y)
print(dict(zip(features, model.feature_importances_)))
```

## Deep learning: sequence models (conceptual + minimal example)

For raw DNA sequence prediction tasks (e.g. predicting transcription factor binding sites), sequences are one-hot encoded and fed into CNNs.

```python
import numpy as np

def one_hot_encode(seq: str) -> np.ndarray:
    mapping = {"A": [1,0,0,0], "C": [0,1,0,0], "G": [0,0,1,0], "T": [0,0,0,1]}
    return np.array([mapping.get(base, [0,0,0,0]) for base in seq])

encoded = one_hot_encode("ATGGCCATTGTA")
print(encoded.shape)  # (12, 4)
```

```python
# Minimal 1D-CNN sketch (PyTorch) for binary sequence classification
import torch
import torch.nn as nn

class SeqCNN(nn.Module):
    def __init__(self, seq_len=200):
        super().__init__()
        self.conv1 = nn.Conv1d(4, 32, kernel_size=8)
        self.pool = nn.MaxPool1d(4)
        self.fc = nn.Linear(32 * ((seq_len - 7) // 4), 1)

    def forward(self, x):          # x: (batch, 4, seq_len)
        x = torch.relu(self.conv1(x))
        x = self.pool(x)
        x = x.flatten(1)
        return torch.sigmoid(self.fc(x))
```

Real projects use established architectures (DeepSEA, Enformer, DNABERT) rather than training from scratch — worth knowing they exist and are loadable via HuggingFace/PyTorch Hub.

## Exercise

1. Train a random forest on an expression matrix to classify two conditions; report accuracy and the top 10 most important genes.
2. Build k-mer feature vectors (k=4) for a set of labeled promoter vs. non-promoter sequences and train a logistic regression classifier.
3. Evaluate your classifier with cross-validation (not just a single train/test split) and report mean ± std accuracy.

**Next:** `05-phylogenetics.md`
