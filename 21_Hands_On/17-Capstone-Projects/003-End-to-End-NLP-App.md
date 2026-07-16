# 003 - Capstone: End-to-End NLP App

## Concept
A complete, simple text classification app: raw text reviews → clean and vectorize the text → train a classifier → evaluate → save it → write a `predict_sentiment(text)` function.

## Why It Matters
Sentiment/text classification is the "hello world" of NLP applications (spam filters, review analysis, support-ticket routing). This capstone shows the whole pipeline works with plain scikit-learn — no huge models required for a solid baseline.

## Hands-On

```python
import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report
import joblib

# --- Step 1: Data (small illustrative example; swap in a real CSV of reviews) ---
texts = [
    "This product is amazing, I love it!",
    "Absolutely terrible, waste of money.",
    "Best purchase I've made all year.",
    "Do not buy this, it broke in a week.",
    "Great quality and fast shipping.",
    "Horrible customer service, very disappointed.",
    "Works perfectly, exactly as described.",
    "Cheaply made and overpriced.",
    "Highly recommend, exceeded expectations.",
    "Complete garbage, do not waste your time.",
] * 10  # repeat to have enough samples for a demo split
labels = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0] * 10   # 1 = positive, 0 = negative

df = pd.DataFrame({"text": texts, "label": labels})

# --- Step 2: Clean text ---
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)   # strip punctuation/numbers
    text = re.sub(r"\s+", " ", text).strip()
    return text

df["clean_text"] = df["text"].apply(clean_text)

# --- Step 3: Train/test split ---
X_train, X_test, y_train, y_test = train_test_split(
    df["clean_text"], df["label"], test_size=0.2, random_state=42, stratify=df["label"]
)

# --- Step 4: Build a pipeline (TF-IDF + classifier bundled together) ---
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
    ("model", LogisticRegression(max_iter=1000)),
])

# --- Step 5: Train ---
pipeline.fit(X_train, y_train)

# --- Step 6: Evaluate ---
y_pred = pipeline.predict(X_test)
print("Test accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# --- Step 7: Save the pipeline (vectorizer + model together) ---
joblib.dump(pipeline, "sentiment_pipeline.pkl")

# --- Step 8: A predict function a real app could call ---
def predict_sentiment(text, pipeline):
    clean = clean_text(text)
    pred = pipeline.predict([clean])[0]
    proba = pipeline.predict_proba([clean])[0]
    label = "positive" if pred == 1 else "negative"
    confidence = proba[pred]
    return label, confidence

loaded_pipeline = joblib.load("sentiment_pipeline.pkl")
print(predict_sentiment("I'm really happy with this purchase!", loaded_pipeline))
print(predict_sentiment("This was a huge disappointment.", loaded_pipeline))
```

## Exercise
1. Replace the toy `texts`/`labels` lists with a real dataset (e.g., the IMDB reviews dataset from `sklearn` or a Kaggle CSV) and re-run everything.
2. Try `TfidfVectorizer(ngram_range=(1,1))` vs `(1,2)` vs `(1,3)` — how does accuracy change as you add longer phrases?
3. Wrap `predict_sentiment` in a tiny command-line loop that reads user input and prints predictions until they type "quit".

## Key Takeaways
- Cleaning text consistently at both training and prediction time is essential — mismatched preprocessing is a common silent bug.
- Bundling the vectorizer and model in one `Pipeline` means you only need to save/load a single object, and the exact same transformation is guaranteed at prediction time.
- Classic TF-IDF + Logistic Regression is a genuinely strong, fast baseline — only reach for transformer models (module 13) when this baseline isn't enough.
