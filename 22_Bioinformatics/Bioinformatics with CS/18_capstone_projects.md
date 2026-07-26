# 18. Capstone Projects

Three end-to-end projects that combine everything from Chapters 1-17 into portfolio-quality work. Pick at least one; ideally do all three across different domains (genomics, transcriptomics, structure/ML) to show range.

---

## Capstone A — Variant-Calling Pipeline (Genomics Engineering)

**Combines:** Ch.1, 6, 8, 9, 10, 17

**Goal:** a real, runnable pipeline: raw reads → aligned BAM → called, filtered, annotated VCF → summary report.

**Requirements:**
1. Takes paired-end FASTQ + a reference FASTA as input.
2. QC + trim reads (reuse Ch.8 tool).
3. Align with `bwa mem`, sort/index with `samtools`.
4. Call variants — either wrap a real caller (`bcftools call`) or extend your Ch.10 naive caller with proper statistical filtering (quality, depth, strand bias).
5. Annotate variants against a GTF (which gene/exon do they fall in — reuse Ch.10.2 logic).
6. Produce a clean summary report (Markdown or HTML) with: variant counts, Ts/Tv ratio, a coverage plot, and a table of high-confidence variants in coding regions.
7. Wrap the whole thing as a single CLI command or Snakemake/Nextflow workflow (bonus: learning a real workflow manager is a strong resume signal).
8. Test on both simulated data (known ground truth, report precision/recall) and one small real public dataset.

**Deliverable:** a GitHub repo with README, example data, and a one-command run.

---

## Capstone B — RNA-seq Differential Expression & Pathway Report

**Combines:** Ch.11, 14, 16, 17

**Goal:** given raw or count-level RNA-seq data for two conditions, produce a full analysis report a biologist collaborator could actually read and trust.

**Requirements:**
1. Load counts, normalize, run DE analysis with proper multiple-testing correction (reuse/extend Ch.11 + Ch.17 tools).
2. Produce standard plots: PCA of samples, volcano plot, heatmap of top DE genes.
3. Build a co-expression network of DE genes (Ch.16) and run community detection; report discovered modules.
4. For each significant module/gene set, do a simple **enrichment test**: is this set of genes enriched for genes on a known pathway list more than expected by chance (a Fisher's exact test against a gene-set list — you can use a small curated pathway list rather than a full formal GO/KEGG enrichment tool)?
5. Optionally train a Ch.14-style classifier on the same data to see if condition is predictable from expression, as an independent sanity check on effect size.
6. Output: a single well-organized Markdown/HTML report with all plots and a written biological interpretation section.

**Deliverable:** repo + rendered report on one real public dataset.

---

## Capstone C — Sequence-to-Function Deep Learning Project

**Combines:** Ch.4, 6, 14, 15

**Goal:** train and rigorously evaluate a model that predicts a biological property directly from sequence, with honest baselines and interpretability.

**Requirements:**
1. Pick a task: TF binding (reuse/extend Ch.15), promoter vs. non-promoter classification, or protein subcellular localization from sequence.
2. Build **three** models of increasing complexity: (a) a simple k-mer + logistic regression baseline (Ch.14), (b) a random forest/GBM on engineered features, (c) a 1D-CNN (Ch.15).
3. Split data correctly to avoid leakage (by genomic region or sequence-similarity clustering, not randomly).
4. Report a fair, honest comparison — precision/recall/AUROC/AUPRC for all three, on the same held-out test set, with a clear statement of which model actually wins and by how much.
5. Interpret the winning model: extract and visualize what it learned (motif logos from CNN filters, or feature importances from the tree model) and check them against known biology (JASPAR motifs, known functional domains).
6. Write a short "limitations" section — what would you need (more data? better negatives? different architecture?) to actually trust this model in a real research setting. This kind of honest self-critique is what distinguishes a strong portfolio project from a toy exercise.

**Deliverable:** repo + a short write-up (README or notebook) presentable as if it were a workshop paper.

---

## After the capstones

You now have hands-on experience across the full bioinformatics stack: sequence algorithms, alignment, assembly, variant calling, expression analysis, structure, networks, classical ML, and deep learning — plus the statistical rigor to back all of it up. From here, natural next steps: contribute to an open-source bioinformatics tool (samtools, Biopython, scikit-bio), reproduce a published paper's analysis end-to-end, or specialize deeper into one area (e.g., long-read genomics, single-cell RNA-seq, or protein structure prediction).
