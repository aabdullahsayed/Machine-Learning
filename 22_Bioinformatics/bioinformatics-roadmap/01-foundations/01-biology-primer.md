# Phase 1: Biology Foundations for CS Students

**Goal:** Understand enough molecular biology and genetics to know *what*
your data represents and *why* the questions matter — not to become a
biologist, but to stop treating sequences as arbitrary strings.

**Time:** 3–5 weeks, ~8 hrs/week.

## 1.1 Core Molecular Biology (Week 1–2)

Topics to master, in order:

- **Central dogma:** DNA → RNA → Protein (transcription, translation)
- **DNA structure:** nucleotides, base pairing, double helix, chromosomes
- **Genes:** exons, introns, promoters, regulatory regions, splicing
- **The genetic code:** codons, reading frames, start/stop codons
- **Proteins:** amino acids, primary/secondary/tertiary/quaternary structure
- **Cell biology basics:** prokaryote vs eukaryote, organelles, cell cycle
- **Mutation types:** SNPs, insertions/deletions, structural variants,
  synonymous vs non-synonymous mutations

**Why it matters for CS thinking:** a genome is not just a 4-letter
alphabet string — biological constraints (reading frames, splice sites,
protein folding) mean sequence "grammar" has real semantic structure,
similar to how syntax rules constrain a programming language.

## 1.2 Genetics & Genomics Concepts (Week 2–3)

- Genotype vs phenotype
- Mendelian inheritance vs complex traits
- Genome vs exome vs transcriptome vs proteome vs epigenome
  ("multi-omics" — you'll see this word constantly)
- Gene expression and regulation (transcription factors, enhancers)
- Epigenetics: methylation, histone modification (brief overview)
- Population genetics basics: allele frequency, linkage disequilibrium,
  Hardy-Weinberg equilibrium

## 1.3 Sequencing Technology Overview (Week 3–4)

You need to understand where the data *comes from* before analyzing it.

- Sanger sequencing (historical baseline)
- Next-generation sequencing (NGS): Illumina short-read (most common)
- Third-generation: PacBio, Oxford Nanopore (long-read)
- Key concepts: reads, coverage/depth, quality scores (Phred), paired-end
  vs single-end, FASTQ format
- Common experiment types: WGS (whole genome), WES (exome), RNA-seq,
  ChIP-seq, ATAC-seq, single-cell RNA-seq — just recognize the names and
  what each measures for now (depth comes in Phase 5)

## 1.4 File Formats You Must Recognize

| Format | Contains |
|---|---|
| FASTA | Raw sequences (DNA/RNA/protein), no quality scores |
| FASTQ | Raw sequencing reads + per-base quality scores |
| SAM/BAM | Aligned reads (BAM = binary, compressed SAM) |
| VCF | Variant calls (SNPs, indels) |
| GFF/GTF | Genome annotations (gene/exon coordinates) |
| BED | Genomic intervals/regions |
| PDB | 3D protein structure coordinates |

Learn by opening real example files, not just reading a table — download
a small FASTQ and VCF from a public repository (e.g., 1000 Genomes, SRA)
and inspect them by hand.

## 1.5 Recommended Free Resources

- **NCBI's "A Science Primer"** — short, free, well-illustrated
- **Rosalind.info** — bioinformatics problems taught through biology +
  programming exercises simultaneously (excellent for CS learners)
- **Khan Academy: Biology > Molecular Genetics** — visual refresher
- **YouTube: "DNA Learning Center"** animations
- See `06-papers-books/textbooks.md` for full-length textbook options

## 1.6 Self-Check Before Moving On

You're ready for Phase 2 (programming) when you can, without looking it
up, explain:
- Why a gene's DNA sequence differs from its mRNA and protein sequence
- What "coverage" means in sequencing and why more isn't always better
- The difference between a SNP and a structural variant
- Why RNA-seq read counts alone don't tell you gene expression level
  (hint: gene length, library size — sets up Phase 4 normalization topics)
