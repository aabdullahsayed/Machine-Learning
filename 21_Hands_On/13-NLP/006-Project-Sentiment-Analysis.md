# 006 - Project: Sentiment Analysis

## Concept
This project builds and compares two full sentiment analysis pipelines on the same dataset — a classical TF-IDF + Logistic Regression baseline, and a fine-tuned DistilBERT model — to see the accuracy/complexity trade-off firsthand.

## Why It Matters
In real projects, you almost always want to try the simple baseline first. This capstone shows exactly how much (or how little) a transformer buys you over TF-IDF, and lets you make that judgment call yourself instead of assuming "bigger model = always better."

## Hands-On

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import re

# --- Step 1: Data ---
# In a real project: pd.read_csv("imdb_reviews.csv") - here, a small illustrative set
reviews = [
    "This movie was absolutely fantastic, best film I've seen all year!",
    "Terrible plot, wooden acting, complete waste of time.",
    "A masterpiece of modern cinema, I was moved to tears.",
    "Boring from start to finish, I nearly fell asleep.",
    "Incredible performances and a gripping story.",
    "Poorly written and badly directed, avoid this one.",
    "One of the best films of the decade, highly recommend.",
    "I want my money back, this was awful.",
    "Charming, funny, and heartfelt - loved every minute.",
    "Disappointing sequel that ruins the original's legacy.",
] * 15
labels = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0] * 15

df = pd.DataFrame({"text": reviews, "label": labels})

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    return text

df["clean_text"] = df["text"].apply(clean_text)

X_train, X_test, y_train, y_test = train_test_split(
    df["clean_text"], df["label"], test_size=0.2, random_state=42, stratify=df["label"]
)

# --- Step 2: Baseline - TF-IDF + Logistic Regression ---
tfidf = TfidfVectorizer(ngram_range=(1, 2))
X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)

baseline_model = LogisticRegression(max_iter=1000)
baseline_model.fit(X_train_tfidf, y_train)
baseline_preds = baseline_model.predict(X_test_tfidf)

baseline_acc = accuracy_score(y_test, baseline_preds)
print(f"Baseline (TF-IDF + LogReg) accuracy: {baseline_acc:.4f}")
print(classification_report(y_test, baseline_preds))

# --- Step 3: Fine-tuned DistilBERT ---
# pip install transformers torch --break-system-packages
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, AdamW
from torch.utils.data import Dataset, DataLoader

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
bert_model = DistilBertForSequenceClassification.from_pretrained(
    "distilbert-base-uncased", num_labels=2
).to(device)

class ReviewDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len=64):
        self.texts, self.labels, self.tokenizer, self.max_len = texts.tolist(), labels.tolist(), tokenizer, max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        enc = self.tokenizer(self.texts[idx], truncation=True, padding="max_length",
                              max_length=self.max_len, return_tensors="pt")
        return {
            "input_ids": enc["input_ids"].squeeze(0),
            "attention_mask": enc["attention_mask"].squeeze(0),
            "label": torch.tensor(self.labels[idx]),
        }

train_loader = DataLoader(ReviewDataset(X_train, y_train, tokenizer), batch_size=8, shuffle=True)
test_loader = DataLoader(ReviewDataset(X_test, y_test, tokenizer), batch_size=8, shuffle=False)

optimizer = AdamW(bert_model.parameters(), lr=2e-5)
bert_model.train()
for epoch in range(3):
    for batch in train_loader:
        optimizer.zero_grad()
        outputs = bert_model(
            input_ids=batch["input_ids"].to(device),
            attention_mask=batch["attention_mask"].to(device),
            labels=batch["label"].to(device),
        )
        outputs.loss.backward()
        optimizer.step()

# --- Step 4: Evaluate DistilBERT ---
bert_model.eval()
all_preds, all_labels = [], []
with torch.no_grad():
    for batch in test_loader:
        outputs = bert_model(
            input_ids=batch["input_ids"].to(device),
            attention_mask=batch["attention_mask"].to(device),
        )
        preds = outputs.logits.argmax(dim=1).cpu().numpy()
        all_preds.extend(preds)
        all_labels.extend(batch["label"].numpy())

bert_acc = accuracy_score(all_labels, all_preds)
print(f"\nDistilBERT accuracy: {bert_acc:.4f}")

# --- Step 5: Compare ---
print(f"\nSummary:\nBaseline (TF-IDF + LogReg): {baseline_acc:.4f}\nDistilBERT: {bert_acc:.4f}")
```

## Exercise
1. Repeat this comparison on a real, larger dataset (e.g., the IMDB 50k reviews dataset) where the gap between approaches is usually more informative than on this tiny toy set.
2. Time both training runs (`time.time()`) and compare — how much slower is fine-tuning DistilBERT than training the TF-IDF baseline?
3. Build a small ensemble that averages both models' predicted probabilities — does it beat either model alone?

## Key Takeaways
- On small or simple datasets, a well-tuned TF-IDF + Logistic Regression baseline can be competitive with — or even outperform — a fine-tuned transformer, while being far faster and cheaper to run.
- Transformers tend to pull ahead on larger, messier, more nuanced datasets where context and word order carry a lot of signal (sarcasm, negation, subtle sentiment).
- Always establish the simple baseline first — it tells you whether the added complexity of a transformer is actually buying you anything for your specific problem.
