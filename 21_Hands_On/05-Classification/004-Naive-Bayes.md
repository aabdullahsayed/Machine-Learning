# 004 - Naive Bayes

## Concept
Naive Bayes applies Bayes' theorem (module 01, file 006) with a "naive" assumption: all features are conditionally independent given the class. Despite this often-false assumption, it works remarkably well, especially for text classification.

## Why It Matters
It's extremely fast to train, works well with high-dimensional sparse data (like word counts), and directly demonstrates Bayes' theorem in action for classification — a great conceptual bridge from module 01's probability lesson.

## Hands-On

```python
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

# --- 1. Naive Bayes for text (spam detection) - the classic use case ---
documents = [
    "win money now", "free lottery winner claim prize",
    "meeting scheduled for tomorrow", "please review the attached report",
    "you have won a free vacation", "let's grab lunch tomorrow",
    "urgent claim your reward now", "quarterly earnings call notes",
    "congratulations you are selected winner", "project deadline extended to friday",
]
labels = [1, 1, 0, 0, 1, 0, 1, 0, 1, 0]  # 1 = spam, 0 = not spam

vectorizer = CountVectorizer()
X_counts = vectorizer.fit_transform(documents)
print("Vocabulary:", vectorizer.get_feature_names_out())
print("Document-term matrix shape:", X_counts.shape)

X_train, X_test, y_train, y_test = train_test_split(
    X_counts, labels, test_size=0.3, random_state=42
)
nb_text = MultinomialNB()
nb_text.fit(X_train, y_train)
print("\nSpam detection accuracy:", accuracy_score(y_test, nb_text.predict(X_test)))

new_email = vectorizer.transform(["claim your free prize now"])
print("New email prediction (1=spam):", nb_text.predict(new_email)[0])
print("Probability breakdown:", nb_text.predict_proba(new_email))

# --- 2. Naive Bayes for continuous features (GaussianNB) ---
from sklearn.datasets import load_iris
iris = load_iris()
X_train_g, X_test_g, y_train_g, y_test_g = train_test_split(
    iris.data, iris.target, test_size=0.3, random_state=42
)
gnb = GaussianNB()
gnb.fit(X_train_g, y_train_g)
print("\nIris GaussianNB accuracy:", accuracy_score(y_test_g, gnb.predict(X_test_g)))

# --- 3. Manually applying Bayes' theorem to understand what's happening ---
# P(spam | words) is proportional to P(words | spam) * P(spam)
# Naive Bayes assumes P(word1, word2 | spam) = P(word1|spam) * P(word2|spam)
class_priors = np.exp(nb_text.class_log_prior_)
print(f"\nClass priors: P(not spam)={class_priors[0]:.3f}, P(spam)={class_priors[1]:.3f}")

feature_log_prob = nb_text.feature_log_prob_
vocab = vectorizer.get_feature_names_out()
word_idx = list(vocab).index("free") if "free" in vocab else None
if word_idx is not None:
    print(f"\nP('free' | not spam) = {np.exp(feature_log_prob[0, word_idx]):.4f}")
    print(f"P('free' | spam)     = {np.exp(feature_log_prob[1, word_idx]):.4f}")
    print("-> 'free' is far more likely to appear in spam, which drives the classifier's decision.")

# --- 4. Why "naive"? Demonstrate the independence assumption is imperfect ---
print("""
The independence assumption says: knowing a message contains "free" tells you
nothing extra about whether it also contains "winner", given the class. In
reality these words co-occur, but Naive Bayes still performs well because it
only needs the RELATIVE ranking of class probabilities to be correct, not
perfectly calibrated absolute probabilities.
""")
```

## Exercise
1. Add 5 more example documents (mixing spam/not-spam) and retrain — does accuracy improve or worsen? Explain in terms of training data size.
2. Compare `MultinomialNB` against `BernoulliNB` (binary word-presence instead of counts) on the same text dataset.
3. On the Iris dataset, compare `GaussianNB`'s accuracy to `LogisticRegression`'s — which assumption (Gaussian feature distributions vs linear decision boundary) fits this data better?

## Key Takeaways
- Naive Bayes is fast, simple, and surprisingly effective for text classification despite its unrealistic independence assumption.
- `MultinomialNB` suits count/frequency data (like word counts); `GaussianNB` suits continuous features assumed to be normally distributed per class.
- Because it directly implements Bayes' theorem, Naive Bayes naturally outputs class probabilities, not just predicted labels.
