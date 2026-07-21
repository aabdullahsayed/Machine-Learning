# 02 — Sequence Alignment

Alignment answers: "how similar are these sequences, and where?" It underlies homology detection, read mapping, and variant calling.

## Pairwise alignment with Biopython

```python
from Bio import Align

aligner = Align.PairwiseAligner()
aligner.mode = "global"          # Needleman-Wunsch (end-to-end)
aligner.match_score = 2
aligner.mismatch_score = -1
aligner.open_gap_score = -2
aligner.extend_gap_score = -0.5

seq1 = "ATGGCCATTGTA"
seq2 = "ATGACCATTGTA"

alignments = aligner.align(seq1, seq2)
best = alignments[0]
print(best)
print(f"Score: {best.score}")
```

Switch to `aligner.mode = "local"` for Smith-Waterman (best matching sub-region) — useful when sequences share only a partial region.

## Use case: primer/adapter matching

```python
aligner.mode = "local"
adapter = "AGATCGGAAGAGC"
read = "ATGGCCATTGTAAGATCGGAAGAGCTTTT"

alignment = aligner.align(read, adapter)[0]
print(alignment)  # shows where the adapter sits inside the read
```

This is the core idea behind adapter-trimming tools like `cutadapt`.

## Multiple sequence alignment (MSA)

For 3+ sequences, use a dedicated tool (Biopython doesn't do MSA itself well) — commonly MAFFT or Clustal Omega, called from Python:

```python
import subprocess

subprocess.run(["mafft", "--auto", "input.fasta"], stdout=open("aligned.fasta", "w"))
```

```python
from Bio import AlignIO

alignment = AlignIO.read("aligned.fasta", "fasta")
print(alignment)
for record in alignment:
    print(record.id, record.seq)
```

## BLAST — searching sequence databases

Two ways to run BLAST from Python:

```python
# 1. Remote (NCBI web service) - good for small jobs
from Bio.Blast import NCBIWWW, NCBIXML

result_handle = NCBIWWW.qblast("blastn", "nt", "ATGGCCATTGTAATGGGCCGCTGA")
blast_record = NCBIXML.read(result_handle)

for alignment in blast_record.alignments[:5]:
    for hsp in alignment.hsps:
        print(alignment.title[:60], "| E-value:", hsp.expect)
```

```bash
# 2. Local BLAST (fast, for large-scale searches)
makeblastdb -in reference.fasta -dbtype nucl -out ref_db
blastn -query query.fasta -db ref_db -outfmt 6 -out results.tsv
```

`-outfmt 6` gives a clean tab-separated table you can load straight into pandas:

```python
import pandas as pd

cols = ["qseqid","sseqid","pident","length","mismatch","gapopen",
        "qstart","qend","sstart","send","evalue","bitscore"]
hits = pd.read_csv("results.tsv", sep="\t", names=cols)
top_hits = hits.sort_values("bitscore", ascending=False).head(10)
print(top_hits)
```

## Use case: percent identity matrix across several genes

```python
from itertools import combinations
from Bio import SeqIO, Align

records = list(SeqIO.parse("genes.fasta", "fasta"))
aligner = Align.PairwiseAligner()
aligner.mode = "global"

for a, b in combinations(records, 2):
    aln = aligner.align(str(a.seq), str(b.seq))[0]
    matches = sum(x == y for x, y in zip(*aln.aligned) if x is not None)
    print(f"{a.id} vs {b.id}: score={aln.score}")
```

## Exercise

1. Align two homologous gene sequences (global mode) and report percent identity.
2. Use local alignment to detect whether a short adapter sequence appears in each of 10 reads; report which reads contain it and at what position.
3. Run a local BLAST of one query sequence against a small custom FASTA database and parse the top 3 hits into a pandas DataFrame.

**Next:** `03-ngs-data-processing.md`
