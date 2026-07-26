# 4. Sequence Analysis Basics — Composition, Motifs, k-mers

## Why this matters
Before alignment and machine learning, you need the basic descriptive-statistics toolkit for sequences: composition, sliding windows, and motif search. These are also your first taste of **k-mer thinking**, which underlies genome assembly (ch.9), read mapping, and a lot of modern genomics ML.

## Core concepts

- **GC content**: fraction of G+C bases; varies by organism/region and affects sequencing bias and gene density.
- **k-mers**: all substrings of length k in a sequence. A sequence of length L has `L - k + 1` k-mers. k-mer frequency vectors are a simple, powerful feature representation for sequences (used in classification, species identification, assembly).
- **Sliding-window statistics**: compute GC%, complexity, or motif hits in a moving window — reveals local structure (e.g., CpG islands, low-complexity regions) that a whole-sequence average would hide.
- **Motifs & Position Weight Matrices (PWMs)**: a motif isn't always exact — transcription factor binding sites are described probabilistically per position. A PWM is literally a `k x 4` matrix of probabilities; scoring a sequence window against a PWM is a dot-product-like operation.

## Practice Project 4.1 — Sliding-window GC / k-mer explorer

**Spec:**
1. `gc_window(seq, window=100, step=10) -> list[float]` — sliding-window GC%.
2. Plot it with matplotlib for a bacterial genome; visually identify regions of unusually high/low GC (these often correspond to horizontally-transferred genes or genomic islands — note any you find).
3. `kmer_counts(seq, k) -> dict[str, int]` using a plain dict, then again using `collections.Counter` — benchmark both on a 1 Mb sequence and report timing.
4. Build a **k-mer frequency fingerprint** (normalized frequency vector for all 4^k k-mers, k=4) for 3 different bacterial genomes (download from NCBI) and show with a simple distance metric (Euclidean or cosine) that the fingerprint of two strains of the same species is more similar than of two different species. This is a real technique — it's the basis of alignment-free phylogenetics.

## Practice Project 4.2 — Motif finder with a Position Weight Matrix

**Spec:**
1. Given a set of ~20 known transcription-factor binding site sequences (all the same length — download an example motif from JASPAR, e.g., search "JASPAR CTCF"), build a PWM: for each position, the frequency of each of A/C/G/T (add pseudocounts to avoid zero probabilities).
2. Write `score_window(window, pwm) -> float` — sum of log-probabilities (log-odds) for that window against the PWM.
3. Slide this scorer across a longer genomic sequence and report the top-10 highest-scoring positions as candidate binding sites.
4. Compare your top hits against the real motif matches reported by JASPAR/MEME for the same sequence, if available, and discuss false-positive rate.

**Done when:** you can explain, in your own words, why a PWM score is basically a naive-Bayes-style log-likelihood ratio, and your motif finder recovers at least some known binding sites in a test sequence.

Next: `05_string_algorithms_alignment.md`.
