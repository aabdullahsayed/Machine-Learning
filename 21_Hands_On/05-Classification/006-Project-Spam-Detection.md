# 006 - Project: Spam Detection

## Concept
An end-to-end text classification project combining text preprocessing, feature extraction (Bag-of-Words / TF-IDF, previewed here and formalized in module 13), and comparing multiple classifiers (Naive Bayes, Logistic Regression, SVM) with proper evaluation.

## Why It Matters
Text classification is one of the most common real-world ML applications, and this project reinforces the full workflow: raw text → numeric features → model comparison → evaluation with the right metrics for imbalanced classes.

## Hands-On

```python
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# 1. Simulated labeled dataset (in practice: load a real CSV, e.g. SMS Spam Collection)
np.random.seed(0)
spam_templates = [
    "win a free {} now click here", "congratulations you won a {}",
    "urgent claim your {} prize today", "limited offer free {} click now",
    "you have been selected for a free {}"
]
ham_templates = [
    "let's meet for {} tomorrow", "can you send the {} report",
    "reminder about the {} meeting", "thanks for the {} update",
    "please review the {} document"
]
fillers = ["gift", "vacation", "lottery", "phone", "lunch", "call",
           "project", "budget", "trip", "voucher"]

texts, labels = [], []
for _ in range(150):
    t = np.random.choice(spam_templates).format(np.random.choice(fillers))
    texts.append(t); labels.append(1)
for _ in range(150):
    t = np.random.choice(ham_templates).format(np.random.choice(fillers))
    texts.append(t); labels.append(0)

df = pd.DataFrame({"text": texts, "label": labels})
print(df["label"].value_counts())

# 2. Split BEFORE vectorizing (avoid leakage, module 02 file 006)
X_train, X_test, y_train, y_test = train_test_split(
    df["text"], df["label"], test_size=0.25, stratify=df["label"], random_state=42
)

# 3. TF-IDF vectorization - fit only on train
vectorizer = TfidfVectorizer(stop_words="english", max_features=200)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)
print(f"\nTF-IDF matrix shape: {X_train_tfidf.shape}")

# 4. Compare multiple classifiers with cross-validation
models = {
    "Naive Bayes": MultinomialNB(),
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Linear SVM": LinearSVC(),
}

print("\n--- 5-fold CV comparison (accuracy) ---")
for name, model in models.items():
    scores = cross_val_score(model, X_train_tfidf, y_train, cv=5)
    print(f"{name:20s} -> {scores.mean():.4f} (+/- {scores.std():.4f})")

# 5. Fit the best model and evaluate on the test set
best_model = LogisticRegression(max_iter=1000).fit(X_train_tfidf, y_train)
y_pred = best_model.predict(X_test_tfidf)
print("\n", classification_report(y_test, y_pred, target_names=["ham", "spam"]))

# 6. Confusion matrix
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(cm, display_labels=["ham", "spam"])
disp.plot(cmap="Blues")
plt.title("Spam Detection Confusion Matrix")
plt.savefig("spam_confusion_matrix.png")
plt.close()

# 7. Inspect the most predictive words (interpretability)
feature_names = vectorizer.get_feature_names_out()
coefs = best_model.coef_[0]
top_spam_words = feature_names[np.argsort(coefs)[-10:]]
top_ham_words = feature_names[np.argsort(coefs)[:10]]
print("\nTop spam-indicating words:", list(top_spam_words))
print("Top ham-indicating words:", list(top_ham_words))

# 8. Test on new, unseen messages
new_messages = ["free vacation click now to claim", "let's discuss the quarterly report"]
new_tfidf = vectorizer.transform(new_messages)
predictions = best_model.predict(new_tfidf)
for msg, pred in zip(new_messages, predictions):
    print(f"\n'{msg}' -> {'SPAM' if pred == 1 else 'HAM'}")
```

## Exercise
1. Swap `TfidfVectorizer` for `CountVectorizer` and compare cross-validation results — does TF-IDF weighting help here?
2. Add `ngram_range=(1, 2)` to the vectorizer to include word pairs — does it improve accuracy?
3. Load a real spam dataset (e.g., search for "SMS Spam Collection Dataset") and repeat this entire pipeline, reporting precision/recall specifically for the spam class.

## Key Takeaways
- Text must be vectorized into numbers before any classifier can use it; TF-IDF down-weights common words and up-weights distinctive ones.
- Always fit the vectorizer only on training data — fitting on the full dataset before splitting is a leakage bug (module 02, file 006).
- For imbalanced or asymmetric-cost problems like spam detection, look beyond accuracy to precision/recall per class (module 06).
