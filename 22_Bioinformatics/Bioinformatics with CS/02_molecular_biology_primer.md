# 2. Molecular Biology Primer (for programmers)

## The central dogma, as a data pipeline

Think of biology as a pipeline with three data types and two transformations:

```
DNA  --(transcription)-->  RNA  --(translation)-->  Protein
```

- **DNA**: a string over the alphabet `{A, C, G, T}`. Double-stranded; strands are reverse-complementary.
- **RNA**: a string over `{A, C, G, U}` (T becomes U). Single-stranded, produced by transcribing a DNA template.
- **Protein**: a string over a 20-letter amino-acid alphabet, produced by translating RNA 3 letters (a **codon**) at a time.

This is literally: `DNA -> RNA` is a character substitution (T→U) plus picking a strand; `RNA -> Protein` is a **lookup table applied to a sliding window of size 3**, terminated by a stop codon. If you know regex and hash maps, you already understand the mechanism — the codon table is just a `dict[str, str]` with 64 keys.

## Key vocabulary (minimum viable glossary)

| Term | CS analogy |
|---|---|
| **Gene** | A named substring/region of the genome that encodes a product |
| **Genome** | The full DNA "file" for an organism |
| **Chromosome** | One "file" in the genome (a directory of files, essentially) |
| **Reading frame** | Which of 3 possible offsets you use to chunk a sequence into codons |
| **Reverse complement** | Reverse the string, then map A↔T, C↔G |
| **Mutation** | An edit operation on the string: substitution, insertion, deletion |
| **SNP** | A single-character substitution that's common in a population |
| **Exon/Intron** | Exons are "kept" substrings after splicing; introns are "spliced out" |
| **Promoter** | A regulatory region upstream of a gene — think "config header" |
| **Ortholog/Paralog** | Same gene in different species / duplicated gene in same species |

## Reading a codon table

There are 64 codons (4³) mapping to 20 amino acids + stop — a many-to-one function, which is why the genetic code is called "degenerate" (redundant), not "ambiguous."

## Practice Project 2.1 — DNA → RNA → Protein simulator (no libraries)

**Goal:** implement the central dogma from scratch to internalize it — don't use Biopython yet.

**Spec:**
1. Write `transcribe(dna: str) -> str` (T→U).
2. Write `reverse_complement(dna: str) -> str`.
3. Write a Python dict `CODON_TABLE` for all 64 codons → amino acid (1-letter code) or `'*'` for stop. (Look this up — copying the standard codon table accurately is itself a good exercise in careful data entry / testing.)
4. Write `translate(rna: str, frame: int = 0) -> str` that reads codons starting at `frame` (0, 1, or 2) and stops at the first stop codon.
5. Write `find_orfs(dna: str) -> list[tuple[int,int,str]]` that scans **all 6 reading frames** (3 forward + 3 on the reverse complement) and returns all Open Reading Frames (start codon `ATG` ... to a stop codon) longer than some minimum length, with their start/end coordinates and translated protein.
6. CLI: `python orf_finder.py my_sequence.txt --min-length 100`

**Test it on:** a real gene sequence — download the human *insulin* gene (INS) CDS from NCBI (search "insulin NM_000207 FASTA") and confirm your translated protein roughly matches the known insulin preproprotein sequence.

**Done when:** your ORF finder correctly identifies the known coding region in a real gene, and you have unit tests for `reverse_complement`, `translate`, and at least 3 edge cases (empty string, sequence with no stop codon, sequence with `N` ambiguity codes).

Next: `03_python_for_bioinformatics.md`.
