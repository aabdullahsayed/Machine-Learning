# 001 - Python for ML Refresher

## Concept
Machine learning code leans heavily on a small set of Python features: list/dict comprehensions, functions with default/keyword args, classes for models, and iterators/generators for streaming data. This lesson refreshes exactly the subset you'll use constantly in the rest of this course.

## Why It Matters
You don't need to be a Python expert, but shaky fundamentals here will slow down every later module — especially vectorized thinking, which is the bridge to NumPy/Pandas.

## Hands-On

```python
# 1. List comprehensions - the workhorse of quick data transforms
squares = [x**2 for x in range(10)]
evens_only = [x for x in range(20) if x % 2 == 0]

# 2. Dict comprehensions - handy for building lookup tables (e.g., label encoders)
labels = ["cat", "dog", "fish"]
label_to_id = {label: idx for idx, label in enumerate(labels)}
print(label_to_id)  # {'cat': 0, 'dog': 1, 'fish': 2}

# 3. Functions with defaults - mirrors how sklearn estimators use default hyperparameters
def train_test_split_ratio(n_samples, test_size=0.2):
    n_test = int(n_samples * test_size)
    n_train = n_samples - n_test
    return n_train, n_test

print(train_test_split_ratio(1000))       # (800, 200)
print(train_test_split_ratio(1000, 0.3))  # (700, 300)

# 4. Classes - every custom model/transformer you write will look like this
class SimpleScaler:
    def __init__(self):
        self.mean_ = None
        self.std_ = None

    def fit(self, data):
        self.mean_ = sum(data) / len(data)
        variance = sum((x - self.mean_) ** 2 for x in data) / len(data)
        self.std_ = variance ** 0.5
        return self

    def transform(self, data):
        return [(x - self.mean_) / self.std_ for x in data]

scaler = SimpleScaler()
scaler.fit([1, 2, 3, 4, 5])
print(scaler.transform([1, 2, 3, 4, 5]))

# 5. Generators - useful for streaming large datasets without loading everything into memory
def batch_generator(data, batch_size):
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]

for batch in batch_generator(list(range(10)), 3):
    print(batch)
```

## Exercise
1. Write a list comprehension that returns only the odd squares from 1 to 20.
2. Extend `SimpleScaler` with an `inverse_transform` method that undoes the scaling.
3. Write a generator `sliding_window(data, window_size)` that yields overlapping windows — this pattern reappears later in time-series forecasting (module 12).

## Key Takeaways
- Comprehensions replace most manual `for` + `append` loops.
- The `fit` / `transform` pattern in `SimpleScaler` is literally how every scikit-learn transformer works — you'll see it constantly.
- Generators let you process data larger than memory, a core idea in deep learning data loaders.
