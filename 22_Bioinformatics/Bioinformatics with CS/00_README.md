# Bioinformatics with CS — A Practical Curriculum

A project-based path into bioinformatics for people who already think like programmers.
Every topic has: **core theory**, **the CS/algorithms angle**, and a **hands-on project** you build yourself.

## How to use this course

1. Go in order the first time through — later files assume earlier ones.
2. Each file is self-contained: read the concept section, then **do the project** before moving on. You learn bioinformatics by writing code that touches real biological data, not by reading about it.
3. Use Python 3.10+ throughout. R is introduced only where it genuinely wins (stats-heavy RNA-seq work).
4. Push every project to a GitHub repo — by the end you'll have a portfolio, not just notes.

## Roadmap

| # | File | Topic | You'll build |
|---|------|-------|---------------|
| 1 | `01_setup_environment.md` | Environment & tooling | A reproducible bioinformatics dev environment |
| 2 | `02_molecular_biology_primer.md` | Biology for programmers | A DNA→RNA→protein simulator |
| 3 | `03_python_for_bioinformatics.md` | Biopython & data wrangling | A FASTA toolkit CLI |
| 4 | `04_sequence_analysis_basics.md` | Sequence stats & motifs | A GC-content / motif-finder |
| 5 | `05_string_algorithms_alignment.md` | Exact string matching | A DNA pattern-search engine (KMP, Boyer-Moore, suffix arrays) |
| 6 | `06_dynamic_programming_alignment.md` | Global/local alignment | Needleman-Wunsch & Smith-Waterman from scratch |
| 7 | `07_blast_database_search.md` | Heuristic search & databases | A mini-BLAST + real NCBI BLAST queries |
| 8 | `08_file_formats_fasta_fastq_sam.md` | Core file formats | A FASTQ quality-control tool |
| 9 | `09_genome_assembly.md` | Graph algorithms for assembly | A de Bruijn graph genome assembler |
| 10 | `10_variant_calling_vcf.md` | Variant calling & VCF | A read-mapper + naive variant caller |
| 11 | `11_rna_seq_gene_expression.md` | Gene expression analysis | An RNA-seq differential expression pipeline |
| 12 | `12_phylogenetics.md` | Trees & evolutionary distance | A phylogenetic tree builder (UPGMA/NJ) |
| 13 | `13_structural_bioinformatics.md` | Protein structure | A PDB structure analyzer + contact map |
| 14 | `14_machine_learning_bioinformatics.md` | Classical ML on biological data | A splice-site / disease classifier |
| 15 | `15_deep_learning_genomics.md` | Deep learning for genomics | A CNN that predicts transcription factor binding |
| 16 | `16_biological_networks_systems_biology.md` | Graphs & networks | A protein-protein interaction network analyzer |
| 17 | `17_statistics_for_bioinformatics.md` | Statistics you actually need | A hypothesis-testing & multiple-testing toolkit |
| 18 | `18_capstone_projects.md` | Capstones | 3 full end-to-end pipelines to build your portfolio |

## Prerequisites

- Comfortable with Python (functions, classes, basic OOP)
- Basic CS: Big-O, arrays, hash maps, recursion, graphs
- No biology background required — Chapter 2 builds it from zero

## Time estimate

~8–14 weeks at 6–10 hrs/week if you build every project, longer if you go deep on the capstones.

Start with `01_setup_environment.md`.
