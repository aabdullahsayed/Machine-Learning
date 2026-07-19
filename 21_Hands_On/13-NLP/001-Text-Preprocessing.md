# 001 - Text Preprocessing

## Concept
Raw text needs to be cleaned and standardized before any model can use it: lowercasing, removing punctuation/noise, tokenizing into words, removing stopwords, and reducing words to their root form (stemming/lemmatization).

## Why It Matters
"Garbage in, garbage out" applies especially strongly to NLP — inconsistent casing, stray punctuation, or unhandled contractions can silently fragment your vocabulary and hurt every downstream model.

## Hands-On

```python
# pip install nltk --break-system-packages
import re
import string
import nltk

nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("averaged_perceptron_tagger", quiet=True)

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

text = "The quick brown foxes were running rapidly through the forest's dense undergrowth!!! Don't you think it's amazing?"

# 1. Lowercase
text_lower = text.lower()
print("Lowercased:", text_lower)

# 2. Remove punctuation
text_no_punct = text_lower.translate(str.maketrans("", "", string.punctuation))
print("No punctuation:", text_no_punct)

# 3. Handle contractions (a common gotcha - "don't" -> "do not" BEFORE removing punctuation ideally)
contractions = {"don't": "do not", "it's": "it is", "can't": "cannot"}
def expand_contractions(text, mapping):
    for contraction, expansion in mapping.items():
        text = text.replace(contraction, expansion)
    return text

text_expanded = expand_contractions(text_lower, contractions)
print("Expanded:", text_expanded)

# 4. Tokenize
tokens = word_tokenize(text_no_punct)
print("Tokens:", tokens)

# 5. Remove stopwords (common words with little semantic signal: "the", "is", "and"...)
stop_words = set(stopwords.words("english"))
tokens_no_stop = [t for t in tokens if t not in stop_words]
print("Without stopwords:", tokens_no_stop)

# 6. Stemming - crude, rule-based root reduction (fast but can produce non-words)
stemmer = PorterStemmer()
stemmed = [stemmer.stem(t) for t in tokens_no_stop]
print("Stemmed:", stemmed)

# 7. Lemmatization - dictionary-based, produces real root words (slower, more accurate)
lemmatizer = WordNetLemmatizer()
lemmatized = [lemmatizer.lemmatize(t, pos="v") for t in tokens_no_stop]  # pos="v" helps verbs
print("Lemmatized:", lemmatized)

# 8. A full reusable preprocessing pipeline
def preprocess_text(text, remove_stopwords=True, lemmatize=True):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    tokens = word_tokenize(text)
    if remove_stopwords:
        tokens = [t for t in tokens if t not in stop_words]
    if lemmatize:
        tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return tokens

sample_reviews = [
    "This movie was absolutely fantastic and I loved every minute!",
    "Terrible acting, boring plot, would not recommend.",
]
for review in sample_reviews:
    print(preprocess_text(review))
```

## Exercise
1. Compare stemming vs. lemmatization on the words "running", "better", "studies", "was" — note where they disagree.
2. Extend `preprocess_text` to also strip out numbers and URLs (`re.sub(r"http\S+", "", text)`).
3. Measure vocabulary size (unique tokens) on a paragraph of text before and after stopword removal — how much smaller is it?

## Key Takeaways
- Stemming is fast but crude (e.g., "studies" → "studi"); lemmatization is slower but produces real dictionary words (e.g., "studies" → "study").
- Whether to remove stopwords depends on the task — they're often safe to drop for topic classification, but can matter for sentiment ("not good" loses meaning if "not" is removed as a stopword).
- Always apply the exact same preprocessing function at both training and inference time — a mismatch here is a very common silent bug (see capstone 003).
