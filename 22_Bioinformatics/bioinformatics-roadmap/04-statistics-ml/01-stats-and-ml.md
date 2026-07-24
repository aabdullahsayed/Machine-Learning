# Phase 4: Statistics & Machine Learning for Biological Data

**Goal:** Biological data is high-dimensional, noisy, and often has far
more features than samples ("small n, large p"). Standard ML intuitions
from CS courses need adjusting.

**Time:** 6–8 weeks.

## 4.1 Statistical Foundations (don't skip even if you know general stats)

- Hypothesis testing fundamentals, p-values, and **why multiple testing
  correction matters enormously in genomics** (testing thousands of
  genes/variants simultaneously)
  - Bonferroni correction, Benjamini-Hochberg FDR — know both and when
    to use which
- Distributions relevant to biological count data: Poisson, Negative
  Binomial (RNA-seq counts are overdispersed Poisson — this single fact
  underlies most differential expression tools)
- Experimental design: replicates (biological vs technical), batch
  effects, confounding — batch effect correction is a recurring,
  underrated problem in real analyses
- Power analysis — how many samples do you need?

## 4.2 Differential Expression Analysis (canonical worked example)

Walk through this fully; it's the most common statistical workflow you
will encounter:

- Raw counts → normalization (library size, TMM, or DESeq2's median-of-
  ratios method) — never compare raw counts directly across samples
- Dispersion estimation and shrinkage (empirical Bayes)
- Generalized linear models (negative binomial GLM) for count data
- Multiple testing correction on the results
- Tools: DESeq2 and edgeR (R); understand the statistical model each
  implements, not just the function calls

## 4.3 Dimensionality Reduction & Clustering

Central to genomics, especially single-cell and population genetics:

- PCA — and why it's used for both visualization and batch-effect
  diagnosis
- t-SNE, UMAP — nonlinear embeddings, common in single-cell RNA-seq
  visualization; know their pitfalls (distances between clusters are
  not always meaningful)
- Clustering: k-means, hierarchical clustering, Louvain/Leiden community
  detection (standard for single-cell cell-type clustering)

## 4.4 Classical ML in Bioinformatics

- Feature selection under high dimensionality (LASSO/elastic net
  regularization is heavily used because p >> n)
- Random forests / gradient boosting for variant effect prediction,
  biomarker discovery
- Support Vector Machines — historically dominant for protein
  classification tasks
- Cross-validation pitfalls specific to biology: **data leakage via
  relatedness** (e.g., splitting by read instead of by patient/sample —
  a very common published-paper mistake worth understanding deeply)

## 4.5 Deep Learning in Bioinformatics

Once classical methods are solid:

- CNNs for sequence data (e.g., predicting transcription factor binding
  from DNA sequence — DeepBind, DeepSEA-style models)
- RNNs/LSTMs and now Transformers for sequence modeling
- **Protein structure prediction** — AlphaFold2's architecture
  (Evoformer, structure module) is worth studying in real depth if
  structural biology interests you; it's arguably the most significant
  bioinformatics result of the last decade
- Protein/DNA language models (ESM, DNABERT, Enformer) — self-supervised
  pretraining on biological sequences, direct conceptual transfer from
  NLP
- Graph neural networks for molecular property prediction,
  protein-protein interaction networks

## 4.6 Self-Check

Can you explain:
- Why you can't just run a t-test on raw RNA-seq counts across samples
- Why FDR correction is preferred over Bonferroni in most genomics
  contexts, and what the tradeoff is
- A concrete example of data leakage specific to biological ML that
  wouldn't occur in a typical CS ML dataset
