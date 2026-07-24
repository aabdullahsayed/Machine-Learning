# Phase 5: Specialized Tracks

**Goal:** After Phases 1–4 you have a general foundation. Now pick 1–2
tracks aligned with your research interest and go deep. Each track below
lists what's distinct about it, key methods, and where to start.

## Track A: Genomics & Variant Analysis

Focus: whole genome/exome sequencing, population genetics, disease
association studies.

- GWAS (genome-wide association studies) methodology, population
  stratification, linkage disequilibrium
- Variant annotation and effect prediction (VEP, ANNOVAR, SIFT/PolyPhen)
- Clinical genomics: ACMG variant classification guidelines
- Key tools: GATK Best Practices pipeline, PLINK

## Track B: Transcriptomics & RNA-seq

Focus: gene expression, alternative splicing, regulatory biology.

- Bulk RNA-seq differential expression (builds directly on Phase 4.2)
- Alternative splicing detection (rMATS, MAJIQ)
- Gene set enrichment analysis (GSEA), pathway analysis (KEGG, Reactome
  databases)
- Long non-coding RNA and regulatory RNA analysis

## Track C: Single-Cell Genomics

Focus: cell-type heterogeneity, developmental trajectories.

- Single-cell RNA-seq pipeline: QC, normalization, clustering,
  annotation (Seurat/scanpy)
- Trajectory inference / pseudotime (Monocle, Slingshot)
- Spatial transcriptomics (rapidly growing subfield — worth knowing it
  exists even if not your focus)
- Multi-omics single-cell integration (CITE-seq, multiome)

## Track D: Structural Bioinformatics

Focus: protein/RNA 3D structure, drug discovery, molecular dynamics.

- Protein structure basics: secondary structure prediction, homology
  modeling
- AlphaFold2/3, RoseTTAFold — study the papers directly (see
  `06-papers-books/`)
- Molecular docking, virtual screening basics
- Molecular dynamics simulation concepts (GROMACS as an entry tool)

## Track E: Metagenomics & Microbiome

Focus: community sequencing, environmental/microbiome samples.

- Taxonomic classification (Kraken2, MetaPhlAn)
- Diversity metrics (alpha/beta diversity, UniFrac)
- Metagenome assembly and binning (MetaBAT, functional annotation)

## Track F: Computational Systems Biology

Focus: networks, models of biological systems.

- Gene regulatory network inference
- Protein-protein interaction network analysis (STRING database)
- ODE-based modeling of biological pathways
- Boolean network models

## Track G: Cancer Genomics

Focus: somatic mutation analysis, tumor evolution.

- Somatic vs germline variant calling (Mutect2)
- Tumor mutational burden, mutational signatures (COSMIC signatures)
- Clonal evolution and tumor heterogeneity inference

## How to Choose

Pick based on:
1. What kind of data excites you more — sequences, images (structures),
   networks, or population-scale tables?
2. What's available at your institution/lab (mentorship matters more
   than the "best" topic on paper)
3. Look at 2–3 recent papers in each track's `06-papers-books/` entry
   and see which you'd want to have written

It's normal and encouraged to combine two tracks (e.g., Track B +
Track C is extremely common as "single-cell transcriptomics").
