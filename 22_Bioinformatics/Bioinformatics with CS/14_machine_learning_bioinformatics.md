# 14. Classical Machine Learning on Biological Data

## Why this matters
Once you can turn biological objects (sequences, expression profiles, structures) into feature vectors, standard ML applies directly. The hard part in bioinformatics ML is almost always **feature engineering from domain knowledge** and **handling small-n, high-dimensional data** correctly — not the model itself.

## Common feature representations

- **k-mer frequency vectors** (Ch.4) — turn any sequence into a fixed-length numeric vector.
- **One-hot encoding** — represent each position of a fixed-length sequence window as a 4-dim (DNA) or 20-dim (protein) one-hot vector, concatenated.
- **Gene expression profiles** — each sample is a vector of expression values across thousands of genes (Ch.11's output) — classic high-dimensional, low-sample-size ML setting.
- **Physicochemical descriptors** — for proteins, features like hydrophobicity, charge, molecular weight per residue.

## Practical pitfalls specific to biological ML

- **Data leakage via homology**: if you split train/test randomly on sequences that include near-duplicate or homologous pairs, your model "cheats" by memorizing similar sequences rather than learning general patterns. Real papers cluster sequences by similarity first, then split by cluster.
- **Class imbalance**: e.g., true splice sites are vastly outnumbered by non-splice-site positions in a genome — accuracy is a misleading metric; use precision/recall/AUROC/AUPRC instead.
- **p >> n**: gene expression datasets often have thousands of genes (features) but only tens of samples — regularization (L1/L2) and dimensionality reduction (PCA) aren't optional, they're required to avoid trivial overfitting.

## Practice Project 14.1 — Splice-site classifier

**Spec:**
1. Get labeled data: positive examples are real donor/acceptor splice-site sequence windows (a fixed-length window around known exon-intron boundaries — extract from a genome + GTF annotation, or use a public splice-site benchmark dataset), negative examples are random windows *not* at splice sites, sampled to be somewhat balanced but not artificially easy.
2. **Split by genomic region/chromosome**, not randomly by window, to avoid leakage from overlapping/adjacent windows.
3. Feature engineering: one-hot encode each window; also try a k-mer frequency featurization; compare which works better.
4. Train and compare at least 3 classical models: logistic regression, random forest, gradient boosting (`scikit-learn`).
5. Evaluate with precision/recall/F1/AUROC/AUPRC (not just accuracy, given class imbalance), and plot a precision-recall curve.
6. Inspect feature importances (for the random forest/GBM) — do the most important positions correspond to the known biological consensus splice-site motif (GT...AG for introns)? This is the "does the model rediscover known biology" check that real bioinformatics ML papers always include.

## Practice Project 14.2 — Disease classification from gene expression

**Spec:**
1. Use a small public gene expression dataset with case/control labels (many are available via GEO; pick a manageable one, e.g., a cancer-vs-normal microarray or RNA-seq dataset with tens to low-hundreds of samples).
2. Preprocess: normalize, and reduce dimensionality with PCA; visualize the first 2 PCs colored by label — do cases and controls separate at all, even roughly?
3. Train an L1-regularized logistic regression (LASSO) — the sparsity is useful here because it naturally selects a small set of "important" genes, which is directly interpretable.
4. Use proper **cross-validation** (stratified k-fold, given likely class imbalance and small n) rather than a single train/test split, since with small n a single split is unreliable.
5. Report which genes got non-zero coefficients — look them up (NCBI Gene) and check if they have known relevance to the disease in question.

**Done when:** you can explain, for your own project, exactly how you avoided data leakage, and your models' selected features/importances plausibly connect to real known biology (not just numbers your model produced).

Next: `15_deep_learning_genomics.md`.
