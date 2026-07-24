# Phase 2: Programming & Tooling Stack

**Goal:** Set up the practical toolkit used in real bioinformatics
workflows. As a CS student you likely already know general programming —
this phase is about domain-specific libraries, formats, and habits.

**Time:** 3–4 weeks in parallel with Phase 1's back half.

## 2.1 Unix / Command Line (if not already fluent)

Non-negotiable — nearly every bioinformatics pipeline is command-line
first.

- Shell basics: pipes, redirection, `grep`, `awk`, `sed`, `sort`, `uniq`
- Process large text files without loading them fully into memory
  (streaming with pipes — genomic files are often 10s–100s of GB)
- `screen`/`tmux` for long-running jobs
- Basic SLURM/PBS if you'll touch an HPC cluster (very common in
  academic bioinformatics labs)

## 2.2 Python for Bioinformatics

- **Biopython** — the standard library for parsing FASTA/FASTQ/GenBank,
  running BLAST programmatically, sequence manipulation
- **pandas / numpy** — tabular and numerical data (you likely know these)
- **pysam** — reading/writing SAM/BAM/VCF files
- **scikit-bio** — diversity metrics, phylogenetics utilities
- **scanpy** — single-cell RNA-seq analysis (needed if going that route)
- Jupyter notebooks for exploratory analysis — but learn to graduate
  exploratory code into proper scripts/pipelines for reproducibility

## 2.3 R (yes, you need some)

A large fraction of bioinformatics statistical methods — especially in
genomics/transcriptomics — are published and maintained as R packages
first, some without a good Python equivalent.

- Base R + tidyverse (`dplyr`, `ggplot2`)
- **Bioconductor** — the R ecosystem for bioinformatics (like CRAN, but
  for biology). Learn to install and navigate it.
- Key packages to know exist (don't need to master all yet):
  `DESeq2`, `edgeR`, `limma` (differential expression),
  `GenomicRanges` (interval operations), `Seurat` (single-cell, R
  alternative to scanpy)

## 2.4 Reproducibility & Workflow Management

Research code that can't be rerun is not research. Learn:

- **Conda/Mamba** — environment and dependency management
  (bioinformatics tools have notoriously fragile dependency chains)
- **Git** — you know this, but also learn **git-lfs** or DVC for large
  data files
- **Snakemake** or **Nextflow** — workflow managers for multi-step
  pipelines (alignment → variant calling → annotation, etc.). Pick one;
  Snakemake has a gentler learning curve for Python users, Nextflow is
  more common in production/clinical pipelines
- **Docker/Singularity** — containerizing tools for reproducible
  execution, especially important on shared HPC systems

## 2.5 Command-Line Bioinformatics Tools to Install & Try

Get comfortable running these on a small test dataset:

- `samtools` / `bcftools` — SAM/BAM/VCF manipulation
- `bwa` or `bowtie2` — short-read alignment
- `BLAST+` — sequence similarity search
- `FastQC` — sequencing quality control
- `GATK` — variant calling (industry/academic standard, Java-based)
- `bedtools` — genomic interval arithmetic

## 2.6 A First Practical Exercise

1. Download a small bacterial genome FASTA and a matching FASTQ read set
   (e.g., from SRA/ENA — pick something small, like *E. coli*).
2. Run FastQC on the reads.
3. Align reads to the genome with `bwa mem`.
4. Sort/index the BAM with `samtools`.
5. Call variants with `bcftools call` or GATK.
6. Open the resulting VCF and interpret 3 variants by hand.

This single pipeline touches nearly every file format and tool category
above and is the most common "hello world" of bioinformatics.

## 2.7 Self-Check

You're ready for Phase 3 when you can write a Snakemake/Nextflow
pipeline (even a 3-step toy one) and explain why environment management
matters more in bioinformatics than in typical software engineering.
