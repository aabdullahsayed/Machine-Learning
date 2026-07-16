# 002 - Supervised vs Unsupervised vs Reinforcement Learning

## Concept
- **Supervised learning**: learn a mapping from inputs to known outputs (labels). Subdivided into regression (continuous output) and classification (discrete output).
- **Unsupervised learning**: find structure in data with no labels (clustering, dimensionality reduction).
- **Reinforcement learning**: an agent learns by interacting with an environment, receiving rewards/penalties for actions.

## Why It Matters
Choosing the right paradigm determines your entire toolkit for the rest of the course: modules 04-07 and 09 focus on supervised learning, module 08 on unsupervised, and module 16 introduces RL.

## Hands-On

```python
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

# --- 1. SUPERVISED: Regression example ---
# We have labeled data: (house_size, price)
house_sizes = np.array([[50], [80], [120], [150], [200]])
prices = np.array([150000, 220000, 310000, 400000, 500000])  # KNOWN labels
reg_model = LinearRegression()
reg_model.fit(house_sizes, prices)
print("Supervised (regression) prediction for 100 sqm:",
      reg_model.predict([[100]])[0])

# --- 2. SUPERVISED: Classification example ---
from sklearn.linear_model import LogisticRegression
emails_length = np.array([[50], [500], [30], [800], [45], [900]])
is_spam = np.array([1, 0, 1, 0, 1, 0])  # KNOWN labels: 1=spam, 0=not spam
clf_model = LogisticRegression()
clf_model.fit(emails_length, is_spam)
print("Supervised (classification) prediction for length=40:",
      clf_model.predict([[40]])[0])

# --- 3. UNSUPERVISED: Clustering example ---
# We have NO labels - just raw customer data, and we want to discover groups
X_customers, _ = make_blobs(n_samples=200, centers=3, random_state=42)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
cluster_labels = kmeans.fit_predict(X_customers)  # labels are DISCOVERED, not given
print("\nUnsupervised: discovered cluster assignments for first 10 customers:",
      cluster_labels[:10])
print("Cluster centers (discovered 'archetypes'):\n", kmeans.cluster_centers_)

# --- 4. REINFORCEMENT LEARNING: conceptual sketch (full example in module 16) ---
# An agent (e.g., a robot) takes actions in an environment (e.g., a maze)
# and learns a policy purely from reward signals, with no labeled "correct
# action" ever provided.
class SimpleGridWorld:
    """A minimal RL environment: agent moves left/right on a 1D line,
    goal is to reach position 4."""
    def __init__(self):
        self.position = 0
        self.goal = 4

    def step(self, action):  # action: -1 (left) or +1 (right)
        self.position += action
        reward = 1.0 if self.position == self.goal else -0.1
        done = self.position == self.goal
        return self.position, reward, done

env = SimpleGridWorld()
total_reward = 0
for _ in range(10):
    action = 1  # naive fixed policy: always move right
    pos, reward, done = env.step(action)
    total_reward += reward
    if done:
        print(f"\nReinforcement Learning: reached goal! Total reward: {total_reward:.2f}")
        break
```

## Exercise
1. Classify each of the following as supervised, unsupervised, or RL: predicting stock prices from historical data with known outcomes; grouping news articles by topic with no topic labels; training a game-playing agent that only receives win/loss signals; detecting fraudulent transactions using past labeled fraud cases.
2. Modify the `SimpleGridWorld` example so the agent starts at a random position and needs at least 2 different actions to reach the goal.
3. Take an unlabeled dataset and run both `KMeans` (unsupervised) and — after manually assigning plausible labels — a `LogisticRegression` (supervised) to compare the two paradigms on the same data.

## Key Takeaways
- The presence (or absence) of labels is the single biggest decision factor for algorithm choice.
- Unsupervised learning is exploratory by nature — there's no ground truth to check accuracy against, only structural/statistical quality.
- RL is fundamentally different: it learns from sequential feedback (rewards) rather than static input-output pairs.
