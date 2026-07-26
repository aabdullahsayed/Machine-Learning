# 11. RNA-seq & Gene Expression Analysis

## Why this matters
DNA tells you what's *possible*; RNA (specifically, mRNA abundance) tells you what a cell is actually *doing* right now. RNA-seq measures genome-wide expression by sequencing the RNA population and counting how many reads map to each gene. This is the workhorse experiment of modern molecular biology (disease mechanisms, drug response, cell-type identification).

## The pipeline

```
FASTQ (RNA reads) --align to transcriptome/genome (STAR/salmon)--> read counts per gene
   --normalize (TPM/CPM, DESeq2-style size factors)--> comparable expression values
   --differential expression test (per gene)--> which genes changed between conditions
   --multiple-testing correction--> which changes are statistically trustworthy
```

## Key ideas

- **Read counts ≠ expression directly** — longer genes and deeper-sequenced samples get more reads by chance alone. **Normalization** (TPM: transcripts per million; or DESeq2/edgeR size-factor normalization) corrects for this.
- **Differential expression (DE)**: for each gene, is its expression significantly different between two conditions (e.g., treated vs. control)? This is thousands of simultaneous hypothesis tests — which is exactly why **multiple-testing correction** (Ch.17, e.g. Benjamini-Hochberg / FDR) is non-negotiable here, not optional statistics trivia.
- **Negative binomial model**: RNA-seq counts are overdispersed (variance > mean) relative to a Poisson, which is why tools like DESeq2/edgeR model counts with a negative binomial rather than assuming Poisson or Gaussian noise.

## Practice Project 11.1 — Count-based DE pipeline from scratch (small scale)

**Spec:**
1. Simulate a toy dataset: 500 "genes," 6 samples (3 control, 3 treatment). Simulate baseline counts from a negative binomial per gene, then make ~50 genes truly differentially expressed by shifting their mean in the treatment group — this gives you ground truth to evaluate against.
2. Normalize counts using a simple median-of-ratios approach (the core idea behind DESeq2's size factors: for each sample, compute the median ratio of its counts to a per-gene geometric-mean reference).
3. For each gene, run a statistical test comparing treatment vs. control (start with a t-test on log-normalized counts; then implement/apply a proper negative-binomial test using `statsmodels` or `scipy` for comparison).
4. Apply Benjamini-Hochberg FDR correction across all 500 tests.
5. Evaluate: how many of your known 50 true DE genes did you recover at FDR < 0.05? How many false positives among the other 450? Report precision/recall, and compare the t-test approach vs. the negative-binomial approach — which does better and why?
6. Make a **volcano plot** (log2 fold-change vs. -log10(p-value)) — the standard visualization for DE results, and a heatmap of the top 20 DE genes across samples.

## Practice Project 11.2 — Real public RNA-seq dataset

**Spec:**
1. Download a small real RNA-seq count matrix from a public source (e.g., GEO/recount3 — pick any two-condition experiment with a gene-level count matrix already provided, to skip raw-read alignment for this project).
2. Run the pipeline from 11.1 on real data (or use `pydeseq2`, a Python port of DESeq2, and compare its results to your from-scratch version).
3. Take your top 10 DE genes and look them up (NCBI Gene / UniProt) — do their known biological functions make sense given the experimental conditions? Write a short biological interpretation paragraph — this "does the statistics make biological sense" step is what separates a real analysis from a numbers exercise.

**Done when:** you understand why multiple-testing correction is essential here (not optional), can explain what a size factor corrects for, and your from-scratch simulation recovers a majority of the true DE genes with reasonably controlled false-positive rate.

Next: `12_phylogenetics.md`.
