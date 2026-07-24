# Phase 3: Core Bioinformatics Algorithms

**Goal:** This is where your CS background pays off directly. Most
foundational bioinformatics algorithms are elegant applications of
dynamic programming, graph theory, hashing, and string algorithms.

**Time:** 4–6 weeks.

## 3.1 Sequence Alignment (start here)

- **Pairwise alignment**
  - Needleman-Wunsch (global alignment) — classic DP
  - Smith-Waterman (local alignment) — classic DP with reset-to-zero
  - Scoring matrices: PAM, BLOSUM — understand *why* substitution costs
    aren't uniform (biochemical similarity of amino acids)
  - Gap penalties: linear vs affine
- **Heuristic alignment (for real-world scale)**
  - BLAST algorithm — seed-and-extend heuristic, why exact DP doesn't
    scale to genome-sized search
  - FASTA algorithm (predecessor to BLAST, good for contrast)
- **Multiple sequence alignment (MSA)**
  - Progressive alignment (ClustalW/Clustal Omega approach)
  - Why MSA is NP-hard exactly, and how heuristics work around it
  - Tools: MAFFT, MUSCLE, Clustal Omega

## 3.2 Read Mapping & Genome Assembly

- **Read alignment to a reference**
  - Suffix trees / suffix arrays — why they matter for fast lookup
  - Burrows-Wheeler Transform (BWT) and FM-index — the backbone of
    `bwa`/`bowtie` — this is one of the most beautiful applications of
    classic string algorithms in any applied CS field, worth deep study
- **De novo genome assembly** (when there's no reference)
  - Overlap-Layout-Consensus (OLC) approach
  - de Bruijn graphs — how k-mers become assembly graphs; the dominant
    modern approach (used by SPAdes, Velvet)
  - Contigs vs scaffolds vs chromosomes; N50 as an assembly quality metric

## 3.3 Variant Calling

- How aligned reads → probabilistic variant calls
- Bayesian genotype likelihood models (conceptual level, GATK's approach)
- Structural variant detection (split reads, discordant pairs, read
  depth signals)

## 3.4 Phylogenetics

- Distance-based methods: UPGMA, Neighbor-Joining
- Character-based methods: Maximum Parsimony
- Probabilistic methods: Maximum Likelihood, Bayesian inference (MCMC) —
  conceptual understanding of why these dominate modern phylogenetics
- Tree representations (Newick format) and visualization

## 3.5 Hidden Markov Models (HMMs) in Biology

Extremely common across bioinformatics — worth mastering deeply.

- Gene prediction (exon/intron boundary detection)
- Profile HMMs for protein family modeling (Pfam database is built this
  way)
- Sequence alignment as an HMM problem
- Forward-backward algorithm, Viterbi algorithm — you likely know these
  from general ML/NLP; the biology application is a direct transfer

## 3.6 Graph Algorithms Recap (applied context)

Since so much of genomics is graph-based, revisit:
- Graph traversal for de Bruijn/overlap graphs
- Eulerian vs Hamiltonian path problems (assembly is fundamentally an
  Eulerian path problem on a de Bruijn graph — classic and important
  insight)
- Shortest path applications in metabolic/regulatory network analysis

## 3.7 Practice Platform

**Rosalind.info** is built exactly for this phase — each problem pairs a
biological question with an algorithmic technique (DP, graphs, strings).
Work through their "Bioinformatics Stronghold" track fully before moving
to Phase 4; it directly reinforces everything above with code.

## 3.8 Self-Check

Can you explain, without notes:
- Why BWT-based indexing made short-read alignment computationally
  feasible at genome scale
- Why genome assembly is modeled as a graph problem, and what a "bubble"
  in a de Bruijn graph represents biologically (hint: heterozygosity or
  sequencing error)
- The difference between what BLAST optimizes for vs Smith-Waterman
