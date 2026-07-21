# 01 — Genome Assembly

Assembly reconstructs a genome from short/long sequencing reads when there's no reference to align to (novel organism, de novo assembly).

## The core idea: overlap graphs / de Bruijn graphs

Short-read assemblers (e.g. SPAdes) build a **de Bruijn graph** from k-mers: each k-mer is a node, and consecutive k-mers in a read create edges. The assembled sequence is a path through this graph.

```python
def build_de_bruijn_graph(reads: list, k: int) -> dict:
    graph = {}
    for read in reads:
        for i in range(len(read) - k + 1):
            kmer = read[i:i+k]
            prefix, suffix = kmer[:-1], kmer[1:]
            graph.setdefault(prefix, []).append(suffix)
    return graph

reads = ["ATGGCC", "GGCCAT", "CCATTG"]
graph = build_de_bruijn_graph(reads, k=4)
for node, edges in graph.items():
    print(node, "->", edges)
```

This toy version illustrates the concept; real assemblers handle sequencing errors, repeats, and branching paths with far more sophistication.

## Running a real assembler

```bash
# SPAdes for short reads (Illumina)
spades.py -1 reads_R1.fastq.gz -2 reads_R2.fastq.gz -o spades_output/

# Flye for long reads (Nanopore/PacBio)
flye --nano-raw long_reads.fastq.gz --out-dir flye_output/ --threads 8
```

## Evaluating assembly quality

Key metrics: **N50** (the contig length at which 50% of the assembly is contained in contigs of that length or longer — higher is generally better), total assembly size, number of contigs.

```python
from Bio import SeqIO

def calculate_n50(fasta_path: str) -> int:
    lengths = sorted([len(r.seq) for r in SeqIO.parse(fasta_path, "fasta")], reverse=True)
    total = sum(lengths)
    running = 0
    for length in lengths:
        running += length
        if running >= total / 2:
            return length
    return 0

n50 = calculate_n50("spades_output/contigs.fasta")
print(f"N50 = {n50} bp")
```

```bash
# Or use QUAST for a full report
quast.py spades_output/contigs.fasta -o quast_report/
```

## Use case: filtering low-quality/short contigs

```python
from Bio import SeqIO

records = [r for r in SeqIO.parse("contigs.fasta", "fasta") if len(r.seq) >= 500]
SeqIO.write(records, "contigs.filtered.fasta", "fasta")
print(f"Kept {len(records)} contigs >= 500bp")
```

## Scaffolding & gap-filling (conceptual)

After assembly, contigs are ordered/oriented into scaffolds using paired-end/long-read information, then gaps between them are filled. Tools: SSPACE, AGOUTI, LINKS. Usually driven via command line, results parsed/QC'd in Python exactly like above.

## Exercise

1. Implement a simple Eulerian-path walker over the toy de Bruijn graph function above to reconstruct a sequence from overlapping reads.
2. Run SPAdes (or use a small test dataset) and compute N50, total length, and number of contigs > 1kb.
3. Compare assemblies from two different k-mer sizes and discuss trade-offs (contiguity vs. accuracy).

**Next:** `02-variant-calling.md`
