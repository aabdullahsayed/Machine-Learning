# 12. Phylogenetics — Trees from Sequences

## Why this matters
Given a set of related sequences, how did they evolve from a common ancestor? This is a tree-reconstruction problem — pure CS (graph/tree algorithms) applied to evolutionary biology, used for everything from tracking viral outbreaks (e.g., COVID lineage tracking) to classifying new species.

## Two core approaches

### Distance-based methods
1. Compute a pairwise distance matrix between all sequences (e.g., from alignment identity, or a proper evolutionary distance model like Jukes-Cantor that corrects for multiple mutations at the same site).
2. Build a tree from the distance matrix:
   - **UPGMA**: repeatedly merge the two closest clusters, assuming a constant mutation rate (a "molecular clock") — simple but often biologically wrong.
   - **Neighbor-Joining (NJ)**: corrects for unequal evolutionary rates across lineages; the standard baseline method in practice.

### Character-based methods
- **Maximum Parsimony**: find the tree that requires the fewest total mutations to explain the observed sequences.
- **Maximum Likelihood** (and Bayesian methods): given an explicit model of sequence evolution, find the tree (and branch lengths) that maximizes the probability of observing the data — the modern gold standard, computationally heavier.

## Practice Project 12.1 — UPGMA and Neighbor-Joining from scratch

**Spec:**
1. Take 6-10 homologous protein or gene sequences (e.g., cytochrome c from several species — a classic phylogenetics teaching dataset, downloadable from UniProt/NCBI).
2. Multiple-align them (use `Bio.Align` or a quick pairwise-based multiple alignment; a full progressive multiple-sequence-alignment implementation is optional/stretch).
3. Compute a pairwise distance matrix (percent difference, or Jukes-Cantor corrected distance for DNA: `d = -3/4 * ln(1 - 4/3 * p)` where p is the observed fraction of differing sites).
4. Implement **UPGMA**: represent the tree as a simple node structure; repeatedly find and merge the closest pair of clusters, updating distances (average linkage), until one root remains.
5. Implement **Neighbor-Joining**: implement the Q-matrix transformation and neighbor-selection step, which is the part that differs from UPGMA and is worth understanding in real depth — it's what allows unequal branch lengths.
6. Visualize both trees (text-based ASCII tree, or use `Bio.Phylo.draw` for a proper plot) and compare — do UPGMA and NJ agree on topology? Where do they differ, and can you relate that to known differences in evolutionary rate between your species?
7. Compare against a tree built by a real tool (e.g., run the same sequences through a quick `Bio.Phylo.TreeConstructor` call, or an online tool like phylogeny.fr) as a sanity check.

## Practice Project 12.2 — Outbreak lineage tracing (mini)

**Spec:**
1. Simulate a small viral outbreak: start from one "ancestral" sequence, and simulate 15-20 "samples" by copying it forward through several generations with a low per-generation mutation rate and branching (some samples share more recent common ancestors than others) — record the true tree as ground truth.
2. Reconstruct the tree from only the final sequences using your NJ implementation.
3. Compare reconstructed topology to the true simulated tree (a simple check: do the same clusters of "closely related" samples group together?).

**Done when:** you can explain the difference between UPGMA and Neighbor-Joining and why NJ is generally preferred, and your reconstructed tree recovers the correct clustering on your simulated outbreak data.

Next: `13_structural_bioinformatics.md`.
