# Phase 6 (Ongoing): Hands-On Projects

Projects are how theory becomes research skill. Do them roughly in order;
each builds on tools/concepts from earlier phases.

## Beginner (during/after Phase 2-3)

1. **Build a pairwise aligner from scratch** — implement Needleman-Wunsch
   and Smith-Waterman yourself (not using Biopython) with a scoring
   matrix. Compare your output to Biopython's `pairwise2`/`Align` module.
2. **FASTQ quality report tool** — write your own mini-FastQC: parse a
   FASTQ, compute per-base quality distributions, GC content, and
   duplicate read rate; plot results.
3. **Codon usage analyzer** — given a genome FASTA + GFF annotation,
   compute codon usage bias across genes and compare between
   highly/lowly expressed genes (need an expression dataset too).
4. **Rosalind problem set completion** — treat the full "Bioinformatics
   Stronghold" as a project; track your solutions in a public GitHub repo.

## Intermediate (during/after Phase 4)

5. **Reproduce a published RNA-seq differential expression analysis** —
   find a paper with public data (GEO/SRA), rerun their pipeline
   (alignment → counts → DESeq2/edgeR), and compare your results to
   their published gene list. Document any discrepancies and why they
   might occur.
6. **Variant calling pipeline with Snakemake** — build an automated,
   reproducible pipeline: FASTQ → alignment → variant calling →
   annotation, packaged with conda environments and a Snakefile.
7. **k-mer based genome assembler** (simplified) — implement a basic
   de Bruijn graph assembler for a small synthetic/bacterial genome;
   visualize the graph and identify assembly "bubbles."
8. **GWAS mini-study** — using a public dataset (e.g., a subset of 1000
   Genomes + simulated phenotype, or a real small public GWAS dataset),
   run association testing, produce a Manhattan plot and QQ plot,
   understand population stratification correction (PCA-based).

## Advanced (Phase 5+, track-specific)

9. **Single-cell RNA-seq full pipeline** — QC → normalization →
   clustering → cell-type annotation → trajectory inference on a public
   dataset (e.g., from the Human Cell Atlas); write up biological
   interpretation, not just code.
10. **Train a small sequence model** — build a CNN or small transformer
    to predict a genomic feature (transcription factor binding site,
    promoter vs non-promoter classification) from raw DNA sequence;
    compare to a published tool's performance.
11. **Protein structure prediction evaluation** — take a set of proteins
    with known structures, run them through a public AlphaFold/ESMFold
    interface, and evaluate prediction accuracy (RMSD, TM-score) versus
    structural properties (length, disorder regions).
12. **Contribute to an open-source bioinformatics tool** — pick a tool
    you've used (Biopython, scanpy, Snakemake plugins), find a "good
    first issue," and submit a PR. This is one of the highest-signal
    things you can put on a research application.

## Capstone-Level

13. **Original small research question** — by this point, pick an open
    question in your chosen track, form a hypothesis, find/generate
    appropriate data, and run a full analysis with a written report
    (introduction, methods, results, discussion — practice writing like
    a real paper). This is the single best preparation for joining a
    research lab or starting a thesis.

## Documentation Habit

For every project: maintain a README with problem statement, data
source, method, and results/limitations. This becomes your portfolio for
lab applications, and forces the same rigor real research requires.
