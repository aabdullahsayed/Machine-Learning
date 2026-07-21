# 03 — Sequence Analysis Basics

## Central dogma in code: DNA → RNA → Protein

```python
dna = "ATGGCCATTGTAATGGGCCGCTGA"

# Transcription: DNA -> mRNA (T becomes U)
mrna = dna.replace("T", "U")

# Translation: mRNA -> protein using the standard genetic code
from textwrap import wrap

codon_table = {
    'UUU':'F','UUC':'F','UUA':'L','UUG':'L','CUU':'L','CUC':'L','CUA':'L','CUG':'L',
    'AUU':'I','AUC':'I','AUA':'I','AUG':'M','GUU':'V','GUC':'V','GUA':'V','GUG':'V',
    'UCU':'S','UCC':'S','UCA':'S','UCG':'S','CCU':'P','CCC':'P','CCA':'P','CCG':'P',
    'ACU':'T','ACC':'T','ACA':'T','ACG':'T','GCU':'A','GCC':'A','GCA':'A','GCG':'A',
    'UAU':'Y','UAC':'Y','UAA':'*','UAG':'*','CAU':'H','CAC':'H','CAA':'Q','CAG':'Q',
    'AAU':'N','AAC':'N','AAA':'K','AAG':'K','GAU':'D','GAC':'D','GAA':'E','GAG':'E',
    'UGU':'C','UGC':'C','UGA':'*','UGG':'W','CGU':'R','CGC':'R','CGA':'R','CGG':'R',
    'AGU':'S','AGC':'S','AGA':'R','AGG':'R','GGU':'G','GGC':'G','GGA':'G','GGG':'G',
}

def translate(mrna: str) -> str:
    protein = ""
    for codon in wrap(mrna, 3):
        if len(codon) < 3:
            break
        aa = codon_table.get(codon, "X")
        if aa == "*":
            break
        protein += aa
    return protein

print(translate(mrna))   # -> "MAIVMGR"
```

## Reverse complement (needed constantly — genes exist on both DNA strands)

```python
complement = str.maketrans("ACGT", "TGCA")

def reverse_complement(seq: str) -> str:
    return seq.translate(complement)[::-1]

print(reverse_complement("ATGGCC"))   # -> "GGCCAT"
```

## Use case: finding open reading frames (ORFs)

An ORF is a stretch starting with ATG and ending with a stop codon — a candidate protein-coding region. Gene finders start here.

```python
def find_orfs(seq: str, min_len: int = 30) -> list:
    orfs = []
    for frame in range(3):
        for i in range(frame, len(seq) - 2, 3):
            if seq[i:i+3] == "ATG":
                for j in range(i, len(seq) - 2, 3):
                    if seq[j:j+3] in ("TAA", "TAG", "TGA"):
                        orf = seq[i:j+3]
                        if len(orf) >= min_len:
                            orfs.append((i, j+3, orf))
                        break
    return orfs

seq = "ATGGCCATTGTAATGGGCCGCTGAAAATGCCCTAAGGGTAG"
for start, end, orf in find_orfs(seq, min_len=9):
    print(f"ORF at {start}-{end}: {orf}")
```

## Sequence similarity: Hamming distance (equal-length sequences)

```python
def hamming_distance(a: str, b: str) -> int:
    if len(a) != len(b):
        raise ValueError("Sequences must be equal length")
    return sum(x != y for x, y in zip(a, b))

print(hamming_distance("ATGGCC", "ATGACC"))  # -> 1
```

## Use case: simple point-mutation scanner

```python
reference = "ATGGCCATTGTA"
sample    = "ATGACCATTGTA"

for i, (r, s) in enumerate(zip(reference, sample)):
    if r != s:
        print(f"Mutation at position {i}: {r} -> {s}")
```

This is the conceptual seed of variant calling, covered properly in `03-advanced/02-variant-calling.md`.

## Exercise

1. Modify `find_orfs` to also search the reverse complement strand (genes can be encoded on either strand).
2. Write a function that translates a full DNA sequence directly (DNA → mRNA → protein in one call).
3. Given two equal-length sequences, report the percent identity (`1 - hamming/len`).

**Next:** `04-biopython-intro.md`
