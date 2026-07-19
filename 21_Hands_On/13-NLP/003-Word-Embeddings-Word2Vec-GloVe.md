# 003 - Word Embeddings: Word2Vec & GloVe

## Concept
Word embeddings represent each word as a dense, low-dimensional vector (e.g., 100-300 dimensions) learned so that words with similar meanings end up close together in vector space — unlike TF-IDF's sparse, meaning-blind vectors.

## Why It Matters
Embeddings capture semantic relationships (king - man + woman ≈ queen) and let models generalize across synonyms, something bag-of-words approaches fundamentally cannot do.

## Hands-On

```python
# pip install gensim --break-system-packages
import numpy as np
from gensim.models import Word2Vec
import gensim.downloader as api

# 1. Train a tiny Word2Vec model on a small corpus (to see the mechanism)
sentences = [
    ["the", "cat", "sat", "on", "the", "mat"],
    ["the", "dog", "sat", "on", "the", "log"],
    ["cats", "and", "dogs", "are", "great", "pets"],
    ["the", "king", "ruled", "the", "kingdom"],
    ["the", "queen", "ruled", "the", "kingdom"],
]

model = Word2Vec(sentences, vector_size=50, window=3, min_count=1, sg=1)  # sg=1 -> skip-gram
print("Vector for 'cat':", model.wv["cat"][:5], "... (50 dims total)")

# 2. Find similar words (on a real, tiny corpus this is limited - see step 3 for pretrained)
similar = model.wv.most_similar("cat", topn=3)
print("Words most similar to 'cat':", similar)

# 3. Use a large PRETRAINED embedding model for meaningful results
# (downloads ~66MB the first time)
print("\nLoading pretrained GloVe vectors...")
glove_vectors = api.load("glove-wiki-gigaword-50")

# 4. The famous analogy: king - man + woman ≈ queen
result = glove_vectors.most_similar(positive=["king", "woman"], negative=["man"], topn=3)
print("king - man + woman ≈", result)

# 5. Semantic similarity between real words
print("Similarity(cat, dog):", glove_vectors.similarity("cat", "dog"))
print("Similarity(cat, car):", glove_vectors.similarity("cat", "car"))

# 6. Nearest neighbors of a word
print("Words closest to 'computer':", glove_vectors.most_similar("computer", topn=5))

# 7. Building a document vector by averaging word vectors (a simple but effective technique)
def document_vector(tokens, embedding_model, dim=50):
    vectors = [embedding_model[t] for t in tokens if t in embedding_model]
    if not vectors:
        return np.zeros(dim)
    return np.mean(vectors, axis=0)

doc_tokens = ["the", "cat", "sat", "on", "the", "mat"]
doc_vec = document_vector(doc_tokens, glove_vectors)
print("Averaged document vector shape:", doc_vec.shape)

# 8. Use averaged embeddings as features for a classifier (compare to TF-IDF from lesson 002)
from sklearn.linear_model import LogisticRegression

texts = ["i love this movie", "this film was terrible", "amazing acting and story", "worst movie ever"]
labels = [1, 0, 1, 0]

X = np.array([document_vector(t.split(), glove_vectors) for t in texts])
clf = LogisticRegression()
clf.fit(X, labels)
print("Trained a classifier on averaged GloVe embeddings, coef shape:", clf.coef_.shape)
```

## Exercise
1. Try the analogy `paris - france + italy` and check if the model returns something close to "rome".
2. Compare classification accuracy using averaged GloVe embeddings vs. TF-IDF (lesson 002) on the same small text dataset.
3. Explore `glove_vectors.most_similar("bank")` — note that a single vector per word means embeddings can't distinguish "river bank" from "money bank" (a limitation solved by contextual embeddings from Transformers, next lesson).

## Key Takeaways
- Word2Vec learns embeddings by predicting context words from a target word (skip-gram) or vice versa (CBOW), directly from a training corpus.
- Pretrained embeddings (GloVe, Word2Vec trained on huge corpora) capture rich semantic relationships and are useful even on small downstream datasets.
- A key limitation: these are *static* embeddings — a word has exactly one vector regardless of context, unlike the contextual embeddings from Transformers (lesson 004), which solves the polysemy problem (e.g., "bank" the riverbank vs. "bank" the financial institution).
