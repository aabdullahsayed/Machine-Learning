# 1. Linear Algebra Basics (The Language of Data)

Machine Learning models don't see "rows in a spreadsheet" — they see **numbers arranged in vectors and matrices**. This file gives you just enough linear algebra to follow the rest of the guide.

## 🔹 What is a Vector?

A vector is simply **a list of numbers**. Think of it as one row of data — for example, a house with 3 features:

```
house = [size_sqft, num_bedrooms, age_years]
house = [1500, 3, 10]
```

That's a vector with 3 numbers (we say it has 3 **dimensions**).

## 🔹 What is a Matrix?

A matrix is just **many vectors stacked together** — like a full spreadsheet:

```
Size | Bedrooms | Age
1500 |    3     | 10
1800 |    4     | 5
1200 |    2     | 20
```

This is a matrix with 3 rows (houses) and 3 columns (features).

## 🔹 The Dot Product (the most important operation in ML)

The dot product multiplies two vectors together and adds up the results. This is literally how a model turns your features into a prediction.

Example: predicting a house price using weights (importance of each feature):

```
features = [1500, 3, 10]        # size, bedrooms, age
weights  = [0.1,  50, -2]       # how much each feature matters

prediction = (1500 × 0.1) + (3 × 50) + (10 × -2)
prediction = 150 + 150 - 20
prediction = 280   (in thousands, say $280,000)
```

That's it — that's the core math inside linear regression, logistic regression, and even the first layer of a neural network.

## 🔹 Why this matters

Every ML model does two things repeatedly:
1. **Multiply** your data by some numbers (weights) → dot product
2. **Adjust** those weights to make better predictions → this is where *gradient descent* comes in (next files!)

## 📝 Quick Recap
- **Vector** = a list of numbers (one data point)
- **Matrix** = a table of vectors (a full dataset)
- **Dot product** = multiply matching numbers, then sum → gives you a single prediction number

Next up: [02_calculus_basics.md](02_calculus_basics.md) — how a model knows *which way* to adjust its weights.
