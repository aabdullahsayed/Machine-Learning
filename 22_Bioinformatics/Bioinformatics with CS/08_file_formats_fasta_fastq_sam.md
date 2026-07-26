# 8. Core File Formats — FASTA, FASTQ, SAM/BAM, VCF, GFF/GTF, BED

## Why this matters
Bioinformatics is, at the engineering level, largely about correctly parsing and transforming a small set of plain-text (or lightly-compressed binary) formats. Get these wrong and every downstream analysis is silently corrupted. This chapter is reference + practice for the formats you've been using implicitly and the ones you'll meet next.

## Format cheat sheet

| Format | Holds | Structure |
|---|---|---|
| **FASTA** (`.fa/.fasta`) | Sequences (no quality) | `>id description\nSEQUENCE...` |
| **FASTQ** (`.fastq/.fq`) | Sequencing reads + per-base quality | 4 lines/record: `@id`, sequence, `+`, quality string (Phred, ASCII-encoded) |
| **SAM/BAM** | Aligned reads (SAM=text, BAM=compressed binary) | Header lines (`@...`) + tab-delimited alignment records (position, CIGAR string, mapping quality...) |
| **VCF** | Genetic variants | Header (`##...`) + tab-delimited variant records (CHROM, POS, REF, ALT, INFO...) |
| **GFF/GTF** | Genome annotations (genes, exons...) | Tab-delimited: seqid, source, feature type, start, end, strand, attributes |
| **BED** | Genomic intervals/regions | Tab-delimited: chrom, start, end, (name, score, strand...) |

## Phred quality scores

FASTQ quality characters encode `Q = -10 * log10(P_error)` as ASCII (`chr(Q+33)` in modern Illumina/Sanger encoding). Q30 means 1-in-1000 chance the base call is wrong — this is the number you'll filter reads on constantly.

## The CIGAR string (SAM)

Describes how a read aligns to the reference as a run-length-encoded operation string, e.g. `76M2D24M` = 76 matched/mismatched bases, a 2-base deletion, then 24 more matched bases. Parsing CIGAR strings correctly is a classic "looks easy, has many edge cases" bioinformatics task (soft clips, insertions, and deletions all shift your reference-vs-read coordinate bookkeeping differently).

## Practice Project 8.1 — FASTQ quality-control tool

**Spec:**
1. Download a small real FASTQ dataset (e.g., from the NCBI SRA, or simulate one with `wgsim`/simple Python).
2. Parse it with `Bio.SeqIO` (`"fastq"` format) or manually (4-lines-at-a-time) — do both, and compare speed.
3. Compute and plot: per-base average quality (position vs mean Phred score, the classic "FastQC" plot), read length distribution, per-read average GC%, and overall duplication rate (exact-duplicate reads).
4. Implement a `trim_and_filter(record, min_qual=20, min_length=50)` function: trim low-quality bases from the read ends (sliding window), then drop reads that fall below `min_length` after trimming.
5. Report before/after stats (# reads, mean quality, mean length) — you've just built a simplified, real version of tools like `fastp`/`Trimmomatic`.

## Practice Project 8.2 — SAM parser + coverage calculator

**Spec:**
1. Align your simulated reads from Chapter 5's project (or new ones) to the reference using real `bwa mem` (installed in Ch.1), producing a SAM file.
2. Parse the SAM file **without pysam first** (manual tab-splitting) to understand the raw format: extract FLAG, POS, CIGAR, MAPQ for each record; correctly interpret at least the "reverse strand" and "unmapped" bits of the FLAG field (it's a bitmask — use `&`).
3. Compute **per-base coverage** across the reference genome (an array where `coverage[i]` = number of reads overlapping position `i`) — correctly accounting for CIGAR operations (M consumes both ref and read, D consumes only ref, I consumes only read).
4. Redo the coverage calculation with `pysam` (`pysam.AlignmentFile`) and confirm your manual version matches — this proves you understand what the library is doing under the hood.
5. Plot coverage across the genome; identify any regions of zero coverage.

**Done when:** you can explain the FLAG bitmask and CIGAR operations from memory, and your manual coverage calculation exactly matches `pysam`'s.

Next: `09_genome_assembly.md`.
