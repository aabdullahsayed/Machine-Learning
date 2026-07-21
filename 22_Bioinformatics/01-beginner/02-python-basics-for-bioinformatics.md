# 02 — Python Basics Applied to Bioinformatics

Focused on the Python features you'll use constantly when handling biological data.

## Strings = sequences

DNA/RNA/protein data is almost always represented as strings, so string manipulation is a core skill.

```python
seq = "ATGGCCATTGTAATGGGCCGCTGA"

# Slicing = extracting sub-sequences (e.g. a codon or exon region)
codon1 = seq[0:3]          # "ATG" (start codon)
last_codon = seq[-3:]      # last 3 bases

# Counting motifs / bases
seq.count("ATG")           # occurrences of start codon motif

# Finding position of a motif
seq.find("GGCC")           # index of first match, -1 if absent

# Iterating in fixed-size chunks (codons = 3 bases)
codons = [seq[i:i+3] for i in range(0, len(seq) - 2, 3)]
print(codons)
```

## Dictionaries = lookup tables (codon tables, k-mer counts)

```python
codon_table = {
    "ATG": "Met", "TAA": "Stop", "TAG": "Stop", "TGA": "Stop",
    "TTT": "Phe", "TTC": "Phe",
}

def translate_codon(codon: str) -> str:
    return codon_table.get(codon, "Unknown")

print(translate_codon("ATG"))   # Met
```

## Use case: k-mer counting (foundation of genome assembly & alignment indexing)

```python
from collections import defaultdict

def kmer_counts(seq: str, k: int) -> dict:
    counts = defaultdict(int)
    for i in range(len(seq) - k + 1):
        counts[seq[i:i+k]] += 1
    return dict(counts)

seq = "ATGGCCATTGTAATGGGCCGCTGA"
print(kmer_counts(seq, 3))
```

## Working with files (every real dataset is a file)

```python
# Reading a plain text file of sequences, one per line
with open("sequences.txt") as f:
    seqs = [line.strip() for line in f if line.strip()]

# Writing results
with open("gc_report.txt", "w") as out:
    for s in seqs:
        gc = round((s.count("G") + s.count("C")) / len(s) * 100, 2)
        out.write(f"{s}\t{gc}\n")
```

## Functions + error handling (real biological data is messy)

```python
def gc_content(seq: str) -> float:
    seq = seq.upper().strip()
    if not seq:
        raise ValueError("Empty sequence")
    valid_bases = set("ATGC")
    if not set(seq).issubset(valid_bases):
        raise ValueError(f"Invalid characters in sequence: {set(seq) - valid_bases}")
    return round((seq.count("G") + seq.count("C")) / len(seq) * 100, 2)
```

## Use case: parsing a simple multi-sequence text block

```python
raw = """
>gene1
ATGGCCATTGTAATGGGCCGCTGA
>gene2
GGGATCCATGGCATCGTAGCTAGC
"""

def parse_simple_fasta(text: str) -> dict:
    records = {}
    name = None
    for line in text.strip().splitlines():
        line = line.strip()
        if line.startswith(">"):
            name = line[1:]
            records[name] = ""
        elif name:
            records[name] += line
    return records

print(parse_simple_fasta(raw))
```

This is literally a mini FASTA parser — you're about to learn why Biopython exists so you don't have to write this yourself for every edge case.

## Exercise

1. Write `kmer_counts` for k=2 (dinucleotides) on a genome-like string and find the most frequent k-mer.
2. Extend `parse_simple_fasta` to also compute and print GC content per record.
3. Handle the case where a sequence contains lowercase letters (soft-masked regions) — normalize with `.upper()`.

**Next:** `03-sequence-analysis-basics.md`
