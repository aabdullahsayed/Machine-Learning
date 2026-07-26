# 7. Heuristic Search & Databases — BLAST

## Why this matters
Smith-Waterman is `O(nm)` per pair — comparing one query against millions of database sequences that way is computationally infeasible. **BLAST** (Basic Local Alignment Search Tool) trades a small amount of sensitivity for enormous speed using a heuristic: find short exact "seed" matches first (fast, via a hash table), then extend only the promising seeds with real alignment.

## The BLAST algorithm, conceptually

1. **Seed**: break the query into overlapping k-mers ("words," typically 11 for DNA, 3 for protein) and look them up in a precomputed hash table of the database's k-mers — `O(1)` average lookup per seed.
2. **Extend**: for each seed hit, extend the alignment in both directions (ungapped, then gapped) using a simplified Smith-Waterman, stopping when the score drops too far below the best score seen (X-drop heuristic).
3. **Evaluate**: score each resulting local alignment and compute an **E-value** — the expected number of alignments with this score or better you'd see by chance in a database this size. Lower E-value = more significant. This is a statistical, not just algorithmic, contribution — know the formula's inputs conceptually: it scales with database size and sequence length, and decreases roughly exponentially with score.

This seed-and-extend pattern reappears everywhere in bioinformatics (read mappers, genome aligners) — it's the general answer to "how do I do approximate matching at scale."

## Practice Project 7.1 — Mini-BLAST from scratch

**Spec:**
1. Build a k-mer index (`dict[str, list[(seq_id, position)]]`) over a database of ~50-100 protein or DNA sequences.
2. Given a query, extract its k-mers and look up seed hits in the index.
3. For each seed hit, extend it in both directions using your Smith-Waterman from Chapter 6 (limit the extension to a window around the seed for speed) rather than aligning the whole sequences.
4. Rank results by alignment score and report top hits with position and score, mimicking a BLAST results table.
5. Compare hit lists (not necessarily exact scores) against running the same query with real `blastn`/`blastp` (installed in Chapter 1) on the same small database — do you find the same top hits?

## Practice Project 7.2 — Real NCBI BLAST + database mining

**Spec:**
1. Take a mystery protein sequence (pick any well-known one, e.g., a random human protein from UniProt) and run it through Biopython's `NCBIWWW.qblast` (or local `blastp` against a downloaded database if you prefer offline work).
2. Parse the XML results with `Bio.Blast.NCBIXML`.
3. Build a small report: top 10 hits with organism, % identity, E-value, alignment length.
4. Programmatically answer: "What organism does this sequence most likely come from, and what's the best-characterized homolog?" using only the BLAST output.
5. **Stretch:** batch this over 20 "mystery" sequences and produce a summary table — this is a realistic day-1 bioinformatics task (sequence identification/annotation).

**Done when:** you understand why BLAST's speed comes from indexing + heuristic extension rather than exhaustive DP, you can read and explain an E-value, and you've successfully run and parsed a real NCBI BLAST search programmatically.

Next: `08_file_formats_fasta_fastq_sam.md`.
