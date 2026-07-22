# Machine Learning Hands-On

A complete, project-based Machine Learning curriculum — from Python/math foundations through classical ML, deep learning, NLP, computer vision, MLOps, and real capstone projects. Every lesson follows the same format: **Concept → Why It Matters → Hands-On (runnable code) → Exercise → Key Takeaways.**

93 lessons across 17 modules. Work through them in order — later modules build directly on earlier ones.

## How to Use This Repo
1. Read the **Concept** and **Why It Matters** sections first for context.
2. Run the **Hands-On** code yourself — don't just read it. Most snippets are copy-paste runnable (`pip install` lines are included where a lesson needs a library beyond the standard scikit-learn/PyTorch stack).
3. Attempt the **Exercise** before moving on — this is where the actual learning happens.
4. Review **Key Takeaways** as a quick recap or later refresher.

---

## Module Map

### 01 — Foundations
The math and tooling every later module assumes: Python for ML, NumPy, Pandas, visualization, linear algebra, probability/statistics, and calculus/gradients.

### 02 — Data Handling and EDA
Loading and cleaning real data, handling missing values and outliers, exploratory data analysis, proper train/val/test splitting, and how to spot and avoid data leakage.

### 03 — Core ML Concepts
The vocabulary and theory behind everything else: what ML is, supervised vs. unsupervised vs. RL, the bias-variance tradeoff, overfitting/underfitting, loss functions, and gradient descent.

### 04 — Regression
Linear regression from scratch and with scikit-learn, polynomial regression, Ridge/Lasso regularization, capped with a house price prediction project.

### 05 — Classification
Logistic regression, KNN, decision trees, Naive Bayes, SVMs, and two projects: spam detection and customer churn prediction.

### 06 — Model Evaluation
Cross-validation, confusion matrices, precision/recall/F1, ROC-AUC, and hyperparameter tuning with grid/random search.

### 07 — Feature Engineering
Scaling, encoding categoricals, feature selection, dimensionality reduction (PCA), and handling imbalanced data.

### 08 — Unsupervised Learning
K-Means, hierarchical clustering, DBSCAN, anomaly detection, and a customer segmentation project.

### 09 — Ensemble Methods
Bagging, Random Forest, AdaBoost, Gradient Boosting, and the modern XGBoost/LightGBM/CatBoost trio — plus a Kaggle-style tabular competition workflow project.

### 10 — Neural Networks Fundamentals
The perceptron, feedforward networks, backpropagation derived by hand, activation functions, a neural net built from scratch in NumPy, and an intro to PyTorch/TensorFlow.

### 11 — Deep Learning: CNNs
Convolution and pooling mechanics, building a CNN, transfer learning, data augmentation, and an image classification project.

### 12 — Deep Learning: Sequence Models
RNN basics, LSTM/GRU, sequence-to-sequence models with attention, and a time series forecasting project.

### 13 — NLP
Text preprocessing, bag-of-words/TF-IDF, word embeddings (Word2Vec/GloVe), an intro to Transformers, fine-tuning BERT, and a sentiment analysis project comparing classical vs. transformer approaches.

### 14 — Computer Vision: Advanced
Object detection with YOLO, image segmentation, GANs, and a face detection app project.

### 15 — MLOps and Deployment
Saving/loading models, building an ML API with FastAPI/Flask, model monitoring and drift detection, Docker, CI/CD for ML pipelines, and a full deploy-to-production project.

### 16 — Advanced Topics
A deeper dive into attention mechanisms, an overview of how LLMs are built and aligned, reinforcement learning basics, self-supervised learning, and explainable AI (SHAP/LIME).

### 17 — Capstone Projects
Five end-to-end projects that tie the whole course together: a tabular ML pipeline, a computer vision app, an NLP app, a Kaggle competition walkthrough, and a full MLOps pipeline.

---

## Suggested Learning Paths

**Classical ML track (fastest path to a solid, employable skillset):**
01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 17 (skip capstones 002/003 which are vision/NLP)

**Deep Learning / AI track (continue into modern architectures):**
Classical ML track above, then → 10 → 11 → 12 → 13 → 14 → 16 → 17

**MLOps / Production track (for engineers focused on shipping models):**
01 → 02 → 03 (skim) → 04 or 05 (pick one) → 06 → 15 → 17-001, 17-005

## Prerequisites
- Comfortable reading and writing basic Python.
- No prior ML experience required — module 01 starts from the fundamentals.
- A Python environment with `pip` access. Each lesson lists any extra packages it needs beyond `numpy`, `pandas`, `matplotlib`, and `scikit-learn` (e.g., `torch`, `transformers`, `xgboost`).

## A Note on the Code
Snippets favor clarity over production polish — variable names are verbose on purpose, and "from scratch" implementations (backprop, attention, gradient boosting, Q-learning, etc.) are included specifically so the underlying mechanics aren't hidden behind a library call. Once a concept is demonstrated from scratch, later lessons switch to the standard library/framework version, matching how you'd actually use it in practice.

Happy learning.
