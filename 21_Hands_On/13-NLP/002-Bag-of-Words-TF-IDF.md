# 002 - Bag of Words & TF-IDF

## Concept
Bag of Words (BoW) represents text as a vector of word counts, ignoring order. TF-IDF (Term Frequency-Inverse Document Frequency) improves on this by down-weighting words that appear in many documents (less informative) and up-weighting words that are frequent in a specific document but rare overall.

## Why It Matters
These are the simplest ways to turn text into numeric features a classical ML model can use, and they remain surprisingly strong baselines (see capstone 003) even in the era of transformers.

## Hands-On

```python
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import pandas as pd
import numpy as np

documents = [
    "The cat sat on the mat",
    "The dog sat on the log",
    "Cats and dogs are great pets",
    "I love my pet cat and my pet dog",
]

# 1. Bag of Words
count_vectorizer = CountVectorizer()
bow_matrix = count_vectorizer.fit_transform(documents)

bow_df = pd.DataFrame(bow_matrix.toarray(), columns=count_vectorizer.get_feature_names_out())
print("Bag of Words matrix:")
print(bow_df)

# 2. TF-IDF
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_vectorizer.get_feature_names_out())
print("\nTF-IDF matrix (rounded):")
print(tfidf_df.round(3))

# 3. Compare: "the" appears in every document (low IDF) vs "love" appears once (high IDF)
idf_scores = pd.Series(tfidf_vectorizer.idf_, index=tfidf_vectorizer.get_feature_names_out())
print("\nIDF scores (higher = rarer, more distinctive):")
print(idf_scores.sort_values(ascending=False).head(5))
print(idf_scores.sort_values().head(5))

# 4. N-grams - capture short phrases, not just single words
bigram_vectorizer = TfidfVectorizer(ngram_range=(1, 2))
bigram_matrix = bigram_vectorizer.fit_transform(documents)
print("\nSample bigram features:", [f for f in bigram_vectorizer.get_feature_names_out() if " " in f][:5])

# 5. Cosine similarity between documents using TF-IDF vectors
from sklearn.metrics.pairwise import cosine_similarity
similarity_matrix = cosine_similarity(tfidf_matrix)
print("\nDocument similarity matrix:")
print(np.round(similarity_matrix, 2))
# Documents 0 and 1 (cat/mat vs dog/log) should be more similar to each other
# than to document 3 (a differently-worded pet document) purely from shared function words

# 6. Practical settings: limiting vocabulary size and filtering rare/common words
practical_vectorizer = TfidfVectorizer(
    max_features=1000,     # keep only the top 1000 most frequent terms
    min_df=2,              # ignore terms that appear in fewer than 2 documents
    max_df=0.9,            # ignore terms that appear in more than 90% of documents
    stop_words="english",  # built-in English stopword removal
)
```

## Exercise
1. Add a fifth document that's a near-duplicate of document 0 and confirm it gets a high cosine similarity score.
2. Compare classification accuracy (using `LogisticRegression`) with `CountVectorizer` vs `TfidfVectorizer` on a small labeled text dataset.
3. Experiment with `max_features` values (100, 1000, 10000) on a larger corpus and observe the trade-off between vocabulary size and model performance/training time.

## Key Takeaways
- BoW/TF-IDF both discard word order — "dog bites man" and "man bites dog" get identical representations, a real limitation for tasks where order matters.
- TF-IDF generally outperforms raw counts because it automatically down-weights uninformative, ubiquitous words like "the" without needing a manual stopword list.
- These sparse, high-dimensional representations pair naturally with linear models (Logistic Regression, Linear SVM) — they're fast, interpretable, and a strong first baseline before reaching for embeddings or transformers.
