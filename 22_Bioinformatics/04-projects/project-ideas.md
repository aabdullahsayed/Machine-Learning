# Portfolio Projects — Beginner to Advanced

Use these to consolidate learning and build a public GitHub portfolio. Each includes goal, skills exercised, and a suggested dataset source.

## Beginner projects

### 1. GC content & sequence stats explorer
- **Goal:** CLI tool that takes a FASTA file and outputs length, GC%, base composition, per-sequence, as a CSV.
- **Skills:** file I/O, Biopython, argparse.
- **Data:** any FASTA from NCBI, or your own toy sequences.

### 2. Codon usage analyzer
- **Goal:** Given a coding sequence, tabulate codon frequency and compare to known codon usage bias tables.
- **Skills:** dictionaries, string processing, matplotlib bar chart.

### 3. DNA to protein translator web tool
- **Goal:** Small Flask/Streamlit app: paste a DNA sequence, get mRNA + protein + ORFs.
- **Skills:** Biopython `Seq`, simple web app, ORF finding.

## Intermediate projects

### 4. FASTQ quality control dashboard
- **Goal:** Parse multiple FASTQ files, summarize per-read quality, base composition, length distribution; output an HTML report (like a mini FastQC).
- **Skills:** Biopython, pandas, matplotlib/plotly, HTML report generation.
- **Data:** SRA (Sequence Read Archive) public datasets.

### 5. BLAST results explorer
- **Goal:** Run local BLAST of a set of query sequences against a reference DB; build a ranked hit table with filtering by e-value/identity; visualize top hits.
- **Skills:** subprocess, BLAST outfmt 6 parsing, pandas.

### 6. Variant annotation pipeline (mini)
- **Goal:** Take a small VCF, annotate variants with gene names and predicted consequence using SnpEff, summarize variant types in a report.
- **Skills:** pysam, VCF parsing, subprocess pipelines.

### 7. Gene/protein lookup CLI
- **Goal:** CLI that accepts a gene symbol, queries Ensembl + UniProt + KEGG, and prints a unified summary (location, protein, pathways).
- **Skills:** REST APIs, requests, JSON parsing, CLI design.

## Advanced projects

### 8. RNA-seq differential expression pipeline
- **Goal:** End-to-end: raw reads (or public counts) → quantification → PyDESeq2 → volcano plot → pathway enrichment report.
- **Skills:** Salmon/kallisto, PyDESeq2, matplotlib, gseapy.
- **Data:** GEO (Gene Expression Omnibus) public RNA-seq datasets.

### 9. Variant calling + somatic mutation detector
- **Goal:** Tumor vs. normal BAM pair → call variants → filter → identify somatic-only candidates → annotate.
- **Skills:** GATK/bcftools, pysam, pandas.
- **Data:** public tumor/normal test datasets (e.g. GATK's test data, TCGA subsets where accessible).

### 10. De novo genome assembly + QC report
- **Goal:** Assemble a small genome (e.g. bacterial or viral) from simulated/public reads, evaluate with N50/QUAST, visualize contig size distribution.
- **Skills:** SPAdes/Flye, QUAST, Biopython.

### 11. Pathogen phylogenetics / outbreak tracker
- **Goal:** Collect sequences of a virus across samples/time, align, build a tree, identify clusters, plot a simple timeline of divergence.
- **Skills:** MAFFT, Biopython Phylo, IQ-TREE, matplotlib.
- **Data:** GISAID / NCBI Virus / public Nextstrain datasets.

### 12. Genomic ML classifier
- **Goal:** Predict a biological label (cancer subtype from expression, promoter vs. non-promoter from sequence, or pathogenic vs. benign variant) with a trained model, evaluated with proper cross-validation, plus feature-importance interpretation.
- **Skills:** scikit-learn, feature engineering (k-mers or expression), model evaluation.
- **Data:** TCGA, GEO, ClinVar.

## Capstone idea

### 13. End-to-end variant-to-report pipeline
Combine everything: FASTQ → QC → trim → align → call variants → annotate → ML-based pathogenicity scoring → auto-generated PDF/HTML clinical-style report for a sample. This mirrors real clinical/research bioinformatics pipelines and is an excellent portfolio centerpiece. Consider wrapping it in **Snakemake** or **Nextflow** for reproducibility.

## Tips for all projects
- Use **version control** (git) from day one; commit often.
- Write a clear `README.md` per project: goal, how to run, sample output.
- Use small test datasets first — full genomes/large FASTQs will make iteration painfully slow.
- Document assumptions and cite data sources.
- Where possible, containerize with **Docker** or use **conda environments** (`environment.yml`) so others can reproduce your results.
