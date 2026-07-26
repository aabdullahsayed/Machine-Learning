# 5. String Algorithms — Exact Matching, Suffix Structures

## Why this matters
"Where does this short read occur in a 3-billion-character genome?" is asked billions of times a day by real pipelines. Naive substring search (`O(nm)`) is too slow at genome scale — this chapter is where classical CS string algorithms earn their keep.

## Algorithms to actually implement

1. **Naive search** — `O(nm)` baseline, know it cold, use it as your correctness oracle.
2. **Knuth-Morris-Pratt (KMP)** — `O(n+m)` using a prefix-function/failure table; good for a single fixed pattern searched many times.
3. **Boyer-Moore** — skips ahead using a bad-character/good-suffix heuristic; often faster in practice on DNA's small 4-letter alphabet.
4. **Suffix arrays** — sort all suffixes of the genome; binary search over the sorted array turns pattern search into `O(m log n)`. This is the real workhorse for repeated queries against one large reference.
5. **(Optional, advanced) Burrows-Wheeler Transform + FM-index** — this is literally what `bwa`, `bowtie`, and `samtools` use under the hood for real-world read alignment. Understanding it demystifies the tools you'll call in Chapter 10.

## Practice Project 5.1 — Pattern search engine + benchmark

**Spec:**
1. Implement `naive_search`, `kmp_search`, `boyer_moore_search`, each returning all match start positions.
2. Implement a `SuffixArray` class: `build(text)`, `search(pattern) -> list[int]` via binary search on the sorted suffix array (start with the `O(n² log n)` naive construction — sorting Python strings — then optimize with the `O(n log n)` prefix-doubling method if you want the harder version).
3. Correctness: for at least 5 randomly generated DNA strings and patterns, assert all four methods agree on the returned positions.
4. Benchmark: download a bacterial genome (~4-5 Mb) as your "text." Search for 100 random 20-mers actually drawn from the genome (guaranteed hits) plus 100 random 20-mers not in it (guaranteed misses). Plot search time for each algorithm as pattern count grows, and explain in a short writeup why the suffix array wins when you search many patterns against one fixed text, but may lose for a single one-off search.

## Practice Project 5.2 — Read mapper (toy, but real logic)

**Spec:**
1. Given a reference genome and a file of thousands of short "reads" (simulate them: randomly cut 100 substrings of length 50–150 from the genome, optionally introduce 1-2 random point mutations per read to mimic sequencing error), build a suffix-array index of the reference.
2. Map each read: exact-match first; if that fails, try splitting the read into two halves and mapping each half (a crude seed-and-extend approach — this is conceptually what BWA does, just simplified).
3. Output a simple mapping report: read ID, position, strand, and number of mismatches found by extending the alignment.
4. Report the mapping rate (% of reads successfully placed) and compare it to the known true positions (since you generated the reads yourself, you know ground truth) — compute mapping accuracy.

**Done when:** your mapper achieves >90% correct placement on reads with 0-1 simulated mismatches, and you understand conceptually why real mappers need indexing (BWT/FM-index or hashing) rather than naive search at genome scale.

Next: `06_dynamic_programming_alignment.md`.
