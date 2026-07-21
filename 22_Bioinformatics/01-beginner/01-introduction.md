# 01 — Introduction to Bioinformatics with Programming

## What is bioinformatics?

Bioinformatics applies computing and statistics to biological data — DNA/RNA/protein sequences, structures, gene expression, and more. Programming is the primary tool for automating analysis at scale (a human genome is ~3 billion base pairs; nothing that size is done by hand).

## Why programming matters here

| Task | Without code | With code |
|---|---|---|
| Count GC content of 10,000 sequences | Impossible manually | A few lines of Python, seconds |
| Compare a gene across 500 species | Days of manual lookup | Automated database queries + alignment |
| Find mutations in a patient's genome | N/A | Variant calling pipeline |

## Environment setup

```bash
# Install conda/mamba (recommended for bioinformatics)
curl -L -O https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
bash Miniforge3-Linux-x86_64.sh

# Create a dedicated environment
mamba create -n bioinfo python=3.11 biopython pandas numpy matplotlib jupyter -y
mamba activate bioinfo
```

Verify:
```bash
python -c "import Bio; print(Bio.__version__)"
```

## Core biology vocabulary you need before coding

- **DNA**: sequence of A, T, G, C bases; carries genetic information.
- **RNA**: A, U, G, C; intermediate between DNA and protein (transcription).
- **Protein**: built from 20 amino acids (translation from RNA codons).
- **Gene**: a DNA region coding for a functional product.
- **Genome**: an organism's complete DNA.
- **FASTA/FASTQ**: standard text file formats for sequences (see `02-intermediate/01-file-formats.md`).
- **Mutation/Variant**: a difference from a reference sequence (SNP, insertion, deletion).

## Use case: "Hello Genome" — your first script

```python
# hello_genome.py
sequence = "ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG"

def gc_content(seq: str) -> float:
    g = seq.count("G")
    c = seq.count("C")
    return round((g + c) / len(seq) * 100, 2)

print(f"Length: {len(sequence)} bp")
print(f"GC content: {gc_content(sequence)}%")
```

Run it: `python hello_genome.py`

## Exercise

1. Write a function `at_content(seq)` mirroring `gc_content`.
2. Write a function `reverse_complement(seq)` that returns the reverse complement of a DNA string (A↔T, G↔C, then reversed).
3. Test both on the sequence above.

**Next:** `02-python-basics-for-bioinformatics.md`
