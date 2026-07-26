# 9. Genome Assembly — Graph Algorithms

## Why this matters
Sequencing machines don't read whole genomes — they produce millions of short (or long) overlapping fragments ("reads"). **Assembly** is the algorithmic problem of reconstructing the original genome from these fragments. It's one of the most elegant applications of graph theory in all of CS.

## Two classical models

### Overlap-Layout-Consensus (OLC)
Build a graph where each read is a node, and an edge connects two reads if they overlap sufficiently. Find a Hamiltonian-like path through the graph that visits reads in genome order. Good for long, noisy reads (PacBio/Nanopore). Hamiltonian path is NP-hard in general, so real tools use heuristics.

### De Bruijn graph assembly (the standard for short reads)
1. Break every read into overlapping **k-mers**.
2. Build a graph where each **(k-1)-mer is a node**, and each k-mer is a directed edge connecting its prefix (k-1)-mer to its suffix (k-1)-mer.
3. The genome corresponds to a path that uses every edge exactly once — an **Eulerian path**, which (unlike Hamiltonian path) is solvable in linear time via Hierholzer's algorithm.
4. Real genomes have repeats, which create graph cycles/branches — this is why assembly is hard in practice, not just in theory. Sequencing errors also create spurious short branches ("tips") and bubbles that assemblers must detect and prune.

This is the same de Bruijn graph idea used by all major short-read assemblers (SPAdes, Velvet) and read-error-correction tools.

## Practice Project 9.1 — De Bruijn graph assembler from scratch

**Spec:**
1. Simulate ground truth: take a real bacterial gene or small genome region (a few kb) as your "true" sequence.
2. Simulate reads: cut it into hundreds of overlapping reads of length ~100 with some overlap, optionally injecting a small sequencing-error rate (~1%).
3. Build the de Bruijn graph for k=21 (or experiment with a few k values): nodes = (k-1)-mers, edges = k-mers observed in your reads, with edge multiplicity = number of times that k-mer was observed.
4. Implement **tip removal**: drop short dead-end branches (likely sequencing errors) below some length threshold.
5. Implement **Eulerian path finding** (Hierholzer's algorithm) to reconstruct contigs by walking the graph.
6. Compare your assembled contig(s) against the true sequence — did you fully reconstruct it? If not, find where it broke (usually at a repeat) and explain why, using your knowledge of the graph structure.
7. **Experiment:** rerun with different k values (a classic parameter in real assembly) and empirically show the tradeoff — small k connects more reads but creates more spurious branches from repeats; large k resolves repeats better but requires more read overlap and is more fragile to errors.

## Practice Project 9.2 — Assembly quality assessment

**Spec:**
1. Run a real short-read simulator (e.g., `wgsim` or `art_illumina`) on a small real reference (a few Mb bacterial genome) to get realistic paired-end reads.
2. Assemble with a real tool (e.g., `SPAdes` if you can install it, or reuse your Chapter 9.1 assembler at larger scale if feasible).
3. Compute standard assembly-quality metrics yourself: **N50** (the contig length such that 50% of total assembly length is in contigs ≥ this length), number of contigs, total assembly length vs. true genome length.
4. Align your contigs back to the true reference (BLAST or your Ch.6 aligner) to check for **misassemblies** (contigs that don't align cleanly, or align to two disjoint regions).

**Done when:** you can compute N50 by hand/code and explain why it's preferred over a simple mean contig length (it's weighted toward longer contigs, which matter more for genome usability), and your from-scratch assembler correctly reconstructs a repeat-free test sequence.

Next: `10_variant_calling_vcf.md`.
