# 3. Python for Bioinformatics — Biopython & Data Wrangling

## Why Biopython

You just built ORF-finding by hand — good, that knowledge doesn't go away. Now switch to **Biopython**, the standard toolkit, so you're not reinventing parsers for every file format you'll meet (FASTA, FASTQ, GenBank, PDB, phylogenetic trees, BLAST XML...).

## Core objects

```python
from Bio.Seq import Seq
from Bio import SeqIO

s = Seq("ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG")
print(s.transcribe())          # DNA -> RNA
print(s.translate(to_stop=True))  # RNA/DNA -> protein
print(s.reverse_complement())

# Parsing files
for record in SeqIO.parse("genes.fasta", "fasta"):
    print(record.id, len(record.seq))
```

`SeqRecord` objects carry an id, description, sequence, and (for richer formats) annotations and features — this is the object model you'll use everywhere.

## Data wrangling with pandas

Most real bioinformatics work is: parse a biological file format → shove relevant fields into a pandas DataFrame → filter/aggregate/plot. Get comfortable with:
- `groupby` (e.g., group variants by chromosome)
- boolean masking (e.g., filter reads by quality score)
- merging two DataFrames on a shared key (e.g., joining gene IDs to expression values)

## Practice Project 3.1 — FASTA toolkit CLI

**Goal:** build a general-purpose command-line tool you'll reuse constantly for the rest of the course.

**Spec — `fastatool.py` with subcommands:**
- `stats <file>` — number of sequences, total length, min/max/mean length, overall GC%
- `filter <file> --min-length N` — write only sequences ≥ N to stdout/new file
- `rename <file> --prefix P` — rename all sequence IDs to `P_1, P_2, ...` (keep a mapping table written to a `.tsv`)
- `translate <file> --frame {0,1,2,all}` — output translated protein FASTA
- `dedupe <file>` — remove exact-duplicate sequences, report how many were removed
- `subseq <file> --id ID --start S --end E` — extract a subsequence by coordinates

**Implementation notes:**
- Use `argparse` with subparsers.
- Use `Bio.SeqIO` for I/O, `Bio.SeqUtils.GC` for GC content.
- Handle multi-line FASTA and empty files without crashing.

**Test data:** download any bacterial genome FASTA from NCBI (e.g., *E. coli* K-12 MG1655, a few Mb) and a small multi-FASTA of random genes.

**Done when:** `python fastatool.py stats ecoli.fasta` correctly reports summary stats you can sanity-check against NCBI's published genome length, and you have pytest tests for each subcommand using a small synthetic FASTA fixture.

Next: `04_sequence_analysis_basics.md`.
