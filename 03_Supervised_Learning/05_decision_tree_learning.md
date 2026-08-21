# 05 — Decision Tree Learning

## Analogy: the "20 Questions" game

Think of the game "20 Questions," where you guess an object by asking a
series of yes/no questions, each one narrowing down the possibilities:
"Is it alive?" → "Is it bigger than a breadbox?" → "Does it fly?" ...
Decision trees learn to play exactly this game automatically: given
labeled data, they figure out the **best sequence of yes/no questions**
(on your features) that most efficiently narrows down to the correct label.

```
                  "Is income > $50k?"
                    /            \
                 yes              no
                  /                \
        "Age > 30?"          "Owns a home?"
          /      \                /      \
        yes       no            yes       no
         │         │              │         │
     "Approve"  "Review"      "Review"   "Deny"
      loan        further        further    loan
```

## Anatomy of a tree

```
                     ┌───────────────┐
                     │   Root Node    │   ← first, most informative question
                     └───────┬───────┘
                 ┌───────────┴───────────┐
                 ▼                       ▼
         ┌──────────────┐        ┌──────────────┐
         │ Internal Node │        │ Internal Node │   ← further questions
         └───────┬───────┘        └───────┬───────┘
             ┌────┴────┐               ┌────┴────┐
             ▼         ▼               ▼         ▼
         ┌───────┐ ┌───────┐      ┌───────┐  ┌───────┐
         │ Leaf  │ │ Leaf  │      │ Leaf  │  │ Leaf  │   ← final predictions
         │ "Yes" │ │ "No"  │      │ "Yes" │  │ "No"  │
         └───────┘ └───────┘      └───────┘  └───────┘
```

| Term | Meaning |
|---|---|
| Root node | the first split — the single most informative question |
| Internal node | a further yes/no split based on some feature |
| Branch | outcome of a split (e.g. "yes" or "no", or a threshold split) |
| Leaf node | terminal node holding the final prediction (class or value) |
| Depth | number of splits from root to a leaf |

## How does the tree pick the "best" question?

At each node, the algorithm tries every possible feature/threshold split
and picks the one that makes the resulting groups **most "pure"** (i.e.,
each group is as close to a single class as possible). Purity is measured
using metrics like **Gini impurity** or **entropy**.

### Gini impurity

```
Gini = 1 − Σ (p_k)²
```

where `p_k` is the fraction of examples in class `k` at that node.

```
Perfectly pure node             Maximally impure node (50/50 split)
(all same class)

   ●●●●●●●●                       ●●●●○○○○
   Gini = 1 − 1² = 0               Gini = 1 − (0.5² + 0.5²) = 0.5
   (best possible — no                  (worst for binary case —
    more splitting needed)               totally mixed)
```

### Entropy (Information Gain)

```
Entropy = − Σ p_k · log2(p_k)

Information Gain = Entropy(parent) − weighted average Entropy(children)
```

The tree picks the split that **maximizes information gain** (or
equivalently, minimizes weighted Gini impurity) at each step.

### Worked mini-example

Node has 10 examples: 6 "Approve", 4 "Deny".

```
Gini(parent) = 1 − ( (6/10)² + (4/10)² ) = 1 − (0.36 + 0.16) = 0.48
```

Try splitting on "Income > $50k?":

```
Left  (Income > 50k):  5 Approve, 1 Deny   → Gini = 1−((5/6)²+(1/6)²) = 0.278
Right (Income ≤ 50k):  1 Approve, 3 Deny   → Gini = 1−((1/4)²+(3/4)²) = 0.375

Weighted Gini after split = (6/10)*0.278 + (4/10)*0.375 = 0.317

Gini decrease = 0.48 − 0.317 = 0.163   ← this is the "gain" from this split
```

The algorithm compares this gain across *all* candidate splits (every
feature, every threshold) and picks the biggest gain at each node,
recursively, until a stopping condition is met.

## Stopping criteria (avoiding an infinitely deep tree)

| Criterion | Effect |
|---|---|
| Max depth reached | limits tree size directly |
| Min samples per leaf | prevents tiny, overfit leaves |
| Min impurity decrease | stop splitting if gain is negligible |
| All examples in a node share one class | naturally pure — nothing left to split |

## Overfitting in trees — and how to fix it

An unconstrained tree can grow until every leaf has just 1 training example
— perfect training accuracy, terrible generalization (classic overfitting,
see file `02`).

```
Shallow tree (underfit-ish)      Deep, unconstrained tree (overfit)

     ┌───┐                              ┌───┐
     │ ? │                              │ ? │
    ╱     ╲                            ╱     ╲
  leaf    leaf                       ┌───┐   ┌───┐
                                     ╱     ╲ ╱     ╲
  simple, may miss                ┌─┐ ┌─┐ ...  ...   (goes very deep,
  some real patterns              ...  memorizing individual
                                           training points)
```

**Fixes:**

| Technique | How it helps |
|---|---|
| **Pruning** | Remove branches that don't improve validation performance |
| **Max depth limit** | Caps how many questions deep the tree can go |
| **Min samples per split/leaf** | Prevents splits based on tiny, noisy subsets |
| **Ensembling (Random Forest, Gradient Boosting)** | Combine many trees to average out individual overfitting |

## Regression trees

Trees aren't just for classification — for regression, each leaf predicts
the **average `y` value** of training examples that land there, and splits
are chosen to minimize variance (instead of Gini/entropy) within each group.

```
Split criterion for regression trees: minimize weighted variance/MSE
of y within each resulting branch (instead of impurity)
```

## Decision Trees vs. Linear/Logistic Regression

| | Linear/Logistic Regression | Decision Trees |
|---|---|---|
| Decision boundary shape | straight line/hyperplane | axis-aligned "staircase" boundaries |
| Captures non-linear patterns? | only with manual feature engineering | naturally, out of the box |
| Interpretability | coefficients | easy to visualize & explain ("if-then" rules) |
| Sensitive to feature scaling? | yes | no |
| Prone to overfitting? | less (especially with regularization) | more (without pruning/limits) |
| Handles categorical features directly? | needs encoding | naturally |

```
Decision tree's "staircase" boundary vs. logistic regression's straight line

  x2                                    x2
   │  ●  ●  ●                            │  ●  ●  ●
   │  ●  ●┌──┐                           │  ●  ●  ╲
   │  ●   │  │  ○                        │  ●      ╲   ○
   │  ─────┘  └───                       │  ────────╲───
   │  ○    ○   ○                         │  ○    ○   ╲ ○
   └──────────── x1                      └──────────── x1
   (tree: rectangular regions)           (logistic regression: single
                                           straight decision boundary)
```

## When to use decision trees

✅ Good for: mixed feature types (numeric + categorical), non-linear
relationships, when interpretability/explainability matters, as building
blocks for powerful ensembles (Random Forest, XGBoost, LightGBM).

❌ Not ideal for: situations needing smooth decision boundaries, small
datasets prone to overfitting a single deep tree (mitigate with pruning
or use an ensemble instead).
