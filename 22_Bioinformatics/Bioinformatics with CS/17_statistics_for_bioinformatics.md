# 17. Statistics for Bioinformatics

## Why this matters
Bioinformatics is fundamentally an exercise in drawing reliable conclusions from noisy, high-dimensional biological measurements. You've already used most of these ideas implicitly in earlier chapters (Ch.11's DE testing, Ch.7's E-values) — this chapter makes them explicit and gives you the toolkit to apply correctly and defend rigorously.

## Core topics

### Hypothesis testing fundamentals
- Null hypothesis, p-value (probability of seeing data this extreme *if the null were true* — not "probability the null is true," a common and important misconception to be able to correct).
- Choosing the right test: t-test (continuous, ~normal), Mann-Whitney U (non-parametric alternative), Fisher's exact test / chi-square (categorical counts — e.g., "is this mutation enriched in cases vs controls?"), and the negative-binomial-based tests used for count data (Ch.11).

### The multiple testing problem
Test 20,000 genes at p<0.05 and you expect ~1,000 false positives by chance alone even with zero real effects. Two standard corrections:
- **Bonferroni**: divide alpha by number of tests — controls family-wise error rate, very conservative.
- **Benjamini-Hochberg (FDR)**: controls the *expected proportion* of false positives among your significant hits — much less conservative, standard for genomics (used throughout Ch.11).

### Power and sample size
Given expected effect size and variance, how many samples do you need to reliably detect a real effect? Underpowered studies are a chronic, real problem in genomics (e.g., early GWAS with too few samples produced many false "hits" that never replicated).

### Bayesian thinking
Priors matter — e.g., BLAST's E-value (Ch.7) is implicitly about how surprised you should be given the size of the search space; the same logic applies to interpreting any single result out of thousands of simultaneous tests.

## Practice Project 17.1 — Hypothesis-testing & multiple-testing toolkit

**Spec:**
1. Build a small library `stats_toolkit.py` implementing (using `scipy.stats` under the hood, but wrapped with clear, documented function signatures you understand): `t_test`, `mann_whitney`, `fishers_exact`, `chi_square`, `bonferroni_correct(pvalues)`, `benjamini_hochberg(pvalues)`.
2. Simulate a dataset of 10,000 independent "gene tests" where you know the ground truth: 200 are truly different between groups (effect size you choose), 9,800 are pure noise (null true).
3. Run t-tests across all 10,000; without correction, count how many nulls you falsely call significant at p<0.05 — confirm it's roughly what theory predicts (~490, i.e. 5% of 9,800).
4. Apply Bonferroni and BH correction separately; for each, report precision/recall against your known ground truth, and compare — quantify exactly how much more conservative Bonferroni is (fewer false positives, but how many more of your true 200 effects does it miss compared to BH?).
5. Vary the true effect size and sample size in your simulation and plot statistical power (fraction of true positives detected) as a function of sample size — reproduce, in miniature, the "why do underpowered studies fail to replicate" phenomenon.

## Practice Project 17.2 — Permutation testing for a real biological question

**Spec:**
1. Pick a question from an earlier project where you eyeballed a pattern without formally testing it (e.g., Ch.16's "are DE genes enriched in this network module?" or Ch.9's contact-map secondary-structure observation).
2. Implement a **permutation test** from scratch: repeatedly shuffle labels/group assignments, recompute your statistic of interest under the null, and build an empirical null distribution; compute a p-value as the fraction of permuted statistics as extreme as your observed one.
3. Compare your permutation-test p-value to a parametric test's p-value (if applicable) on the same data — do they roughly agree? When would you trust the permutation test more (e.g., when the data clearly violates the parametric test's assumptions)?

**Done when:** you can explain in one sentence what a p-value actually means (and doesn't mean), you can justify when to use Bonferroni vs. BH in your own words, and your simulation concretely demonstrates the false-positive explosion that motivates multiple-testing correction in the first place.

Next: `18_capstone_projects.md`.
