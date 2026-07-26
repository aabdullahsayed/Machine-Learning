# 15. Deep Learning for Genomics

## Why this matters
DNA is a sequence, and modern deep architectures (CNNs, RNNs, Transformers) are built exactly for sequence data. Deep learning has produced the field's biggest recent breakthroughs — AlphaFold for structure prediction, and CNN/Transformer models that predict regulatory activity, splicing, and variant effects directly from raw DNA sequence.

## Why CNNs fit genomics so well

A 1D convolution sliding across a one-hot-encoded DNA sequence is, at the first layer, literally learning **motif detectors** — each filter is a soft, trainable, differentiable version of the Position Weight Matrix you hand-built in Chapter 4. Stacking convolution + pooling layers lets the network compose simple motifs into larger regulatory "grammar" (e.g., combinations of transcription-factor binding sites), which is conceptually similar to how a CNN composes edges into shapes into objects for images. This is *the* intuition to hold onto in this chapter.

## Practice Project 15.1 — CNN for transcription-factor binding prediction

**Spec:**
1. Get a labeled dataset: DNA sequence windows (e.g., 100-200bp) labeled bound/not-bound for a specific transcription factor. (ChIP-seq peak data for a TF, downsampled and paired with negative windows from elsewhere in the genome, is the classic setup — several such benchmark datasets are publicly available, e.g., via ENCODE-derived tutorials.)
2. One-hot encode sequences to shape `(length, 4)`.
3. Build a small 1D-CNN in PyTorch or TensorFlow/Keras: a couple of `Conv1D` layers (e.g., 16-32 filters, kernel size ~8-15 to roughly match real motif lengths) + `MaxPool1D` + a dense head with sigmoid output for binary classification.
4. Train with proper train/val/test split (split by genomic region, as in Ch.14, to avoid leakage from overlapping windows).
5. Evaluate with AUROC/AUPRC; compare against your Chapter 14 classical-ML baseline (k-mer + logistic regression / random forest) on the *same* data — does the CNN actually beat the simpler baseline? (Sometimes it doesn't on small datasets — that's a real and important finding, not a failure.)
6. **Interpretability**: visualize what the first-layer convolutional filters learned by converting each filter's weights into a sequence logo (this is directly comparable to the PWM you built in Ch.4) — do any filters resemble a known motif for your TF (check against JASPAR)?

## Practice Project 15.2 — Variant effect scoring (mini)

**Spec:**
1. Using your trained model from 15.1, take real sequence windows and, for each, generate all possible single-base mutations (an "in-silico saturation mutagenesis" — every position × 3 alternate bases).
2. For each mutation, compute the model's predicted change in binding probability (mutant score − reference score).
3. Plot this as a heatmap: position (x-axis) × alternate base (y-axis), colored by predicted effect size — this is a real, standard visualization used in published deep-learning-genomics papers.
4. Check whether positions your model considers most sensitive to mutation line up with positions you'd expect to matter based on your Chapter 4 PWM/motif analysis of the same TF.

**Done when:** you can explain in plain language why 1D convolution is a natural fit for motif detection in DNA, you have an honest comparison of CNN vs. classical-ML baseline performance (not just "deep learning wins" assumed), and you've extracted at least one interpretable, biologically-plausible motif from your trained filters.

Next: `16_biological_networks_systems_biology.md`.
