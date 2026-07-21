# 04 — Introduction to Biopython

Biopython is the standard Python library for bioinformatics: parsing file formats, running alignments, querying databases, handling sequence objects properly (so you stop reinventing FASTA parsers).

```bash
pip install biopython
```

## The `Seq` object

```python
from Bio.Seq import Seq

seq = Seq("ATGGCCATTGTAATGGGCCGCTGA")

print(seq.reverse_complement())
print(seq.transcribe())          # DNA -> mRNA
print(seq.translate())           # -> protein, stops at first stop codon
print(seq.translate(to_stop=True))
```

Output handles all the biology correctly (ambiguous bases, alternate codon tables, etc.) — far more robust than hand-rolled code.

## Reading FASTA files

```python
from Bio import SeqIO

for record in SeqIO.parse("genes.fasta", "fasta"):
    print(record.id, len(record.seq))
```

A `genes.fasta` example:
```
>gene1 description here
ATGGCCATTGTAATGGGCCGCTGA
>gene2 another description
GGGATCCATGGCATCGTAGCTAGC
```

## Use case: batch GC content report across a FASTA file

```python
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction

results = []
for record in SeqIO.parse("genes.fasta", "fasta"):
    gc = round(gc_fraction(record.seq) * 100, 2)
    results.append((record.id, len(record.seq), gc))

for rid, length, gc in results:
    print(f"{rid}\t{length} bp\t{gc}% GC")
```

## Reading FASTQ files (sequencing reads + quality scores)

```python
from Bio import SeqIO

for record in SeqIO.parse("reads.fastq", "fastq"):
    print(record.id)
    print(record.seq)
    print(record.letter_annotations["phred_quality"])
    break  # just show the first read
```

## Fetching data from NCBI (Entrez)

```python
from Bio import Entrez, SeqIO

Entrez.email = "you@example.com"  # NCBI requires this

handle = Entrez.efetch(db="nucleotide", id="NM_000546", rettype="fasta", retmode="text")
record = SeqIO.read(handle, "fasta")
handle.close()

print(record.id, len(record.seq))
```

This pulls a real human gene sequence (TP53 mRNA) directly from NCBI — your first live-database use case.

## Writing FASTA files back out

```python
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq

record = SeqRecord(Seq("ATGGCCATTGTA"), id="my_seq", description="example")
SeqIO.write([record], "output.fasta", "fasta")
```

## Exercise

1. Download 3 gene sequences via `Entrez.efetch` and save them into one FASTA file.
2. Parse that FASTA and print a table of id, length, GC%.
3. Filter and write out only sequences longer than 500 bp to `long_genes.fasta`.

**You've completed the Beginner track.** Continue to `02-intermediate/01-file-formats.md`.
