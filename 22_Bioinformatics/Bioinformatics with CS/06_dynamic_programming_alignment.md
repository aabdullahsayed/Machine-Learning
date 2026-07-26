# 6. Dynamic Programming — Sequence Alignment

## Why this matters
Exact matching (Ch.5) assumes sequences are identical substrings. Real biology is full of mutations, insertions, and deletions — you need **alignment**, which finds the best way to line up two sequences allowing gaps and mismatches. This is the single most important algorithmic idea in classical bioinformatics, and it's a textbook dynamic-programming problem — basically edit distance with biologically-motivated scoring.

## Global alignment — Needleman-Wunsch

Aligns two full sequences end-to-end. Build a `(n+1) x (m+1)` DP matrix where:

```
F(i,0) = -i * gap_penalty
F(0,j) = -j * gap_penalty
F(i,j) = max(
    F(i-1,j-1) + score(a[i], b[j]),   # match/mismatch
    F(i-1,j)   - gap_penalty,          # deletion
    F(i,j-1)   - gap_penalty           # insertion
)
```
Traceback from `F(n,m)` to `F(0,0)` recovers the optimal alignment. Time and space: `O(nm)`.

## Local alignment — Smith-Waterman

Same recurrence but clamp scores at 0 (`F(i,j) = max(0, ...)`) and start traceback from the highest-scoring cell, stopping at a 0. Finds the best-matching **subsequence** rather than forcing a full end-to-end alignment — this is what you want when comparing a short gene against a long genome, or two proteins that share only one domain.

## Scoring matters as much as the algorithm

- DNA: usually simple match/mismatch/gap constants.
- Protein: substitution matrices like **BLOSUM62** or **PAM250** encode which amino-acid swaps are evolutionarily "cheap" (e.g., Leucine↔Isoleucine is nearly free; Leucine↔Proline is costly) based on observed substitution frequencies in real protein families.
- **Affine gap penalties** (`gap_open + k * gap_extend`) model biology better than a flat per-gap cost, since one 5-base deletion is usually one mutational event, not five.

## Practice Project 6.1 — Alignment engine from scratch

**Spec:**
1. Implement `needleman_wunsch(seq1, seq2, match=1, mismatch=-1, gap=-2) -> (score, aligned1, aligned2)` with full traceback.
2. Implement `smith_waterman(seq1, seq2, ...)` similarly, returning the best local alignment.
3. Extend both to accept a substitution-matrix dict instead of flat match/mismatch (load BLOSUM62 — Biopython ships it: `from Bio.Align import substitution_matrices; substitution_matrices.load("BLOSUM62")`).
4. Add **affine gap penalties** (this requires 3 DP matrices instead of 1 — M/Ix/Iy — the classic Gotoh algorithm; this is the hardest and most valuable sub-task in this file).
5. Validate against `Bio.Align.PairwiseAligner` — for at least 5 test sequence pairs, confirm your scores match Biopython's to make sure your implementation is correct.

## Practice Project 6.2 — Real biological comparison

**Spec:**
1. Download two homologous protein sequences from different species (e.g., human and mouse hemoglobin beta chain from UniProt).
2. Run your Smith-Waterman with BLOSUM62 + affine gaps; report percent identity, alignment length, and score.
3. Visualize the alignment (simple text output with `|` for matches is fine; stretch goal: a dot-plot).
4. Do the same for a clearly non-homologous pair (e.g., human hemoglobin vs random unrelated protein) and show the score/identity is much lower — this is your first taste of using alignment score as a homology-detection signal, which is exactly what BLAST automates at scale (next chapter).

**Done when:** your from-scratch aligner's scores match Biopython's `PairwiseAligner` output exactly on test cases, and you can articulate why local alignment (Smith-Waterman) is the right tool for domain/motif matching while global (Needleman-Wunsch) is right for comparing two full, similar-length sequences.

Next: `07_blast_database_search.md`.
