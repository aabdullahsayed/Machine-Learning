# 10. Variant Calling — From Reads to VCF

## Why this matters
This is the pipeline behind clinical genetics, GWAS, and cancer genomics: given a person's sequencing reads and a reference genome, find where their DNA differs from the reference. It combines everything so far — alignment (Ch.6/8), file formats (Ch.8), and statistics (Ch.17).

## The pipeline

```
Raw reads (FASTQ)
   --align (bwa mem)-->      SAM/BAM
   --sort & index (samtools)--> sorted BAM
   --pileup / call variants-->  VCF
```

## What a variant caller actually does

At each genome position, look at every read that overlaps it (the "pileup"). If a meaningful fraction of reads disagree with the reference base — more than sequencing error alone would explain — call a variant. Real callers (GATK, bcftools, DeepVariant) use careful statistical models (base quality, mapping quality, strand bias, local realignment around indels) to separate real variants from noise; but the core idea is simple counting + a significance test.

## Practice Project 10.1 — Build a naive variant caller

**Spec:**
1. Take a reference sequence (a few kb) and simulate a "sample" genome by introducing 10-20 known point mutations and a couple of small indels at known positions — this is your ground truth.
2. Simulate reads from the mutated sample (as in Ch.9), align them back to the **original reference** with `bwa mem`, producing a sorted, indexed BAM (`samtools sort`, `samtools index`).
3. Using `pysam`, iterate every reference position with `pileup()`; at each position, count how many reads support each base (A/C/G/T) and the reference base's read depth.
4. Call a SNP if the non-reference allele frequency at a position exceeds a threshold (e.g., >20% of reads, with at least 4 supporting reads) — write these out as a valid VCF file (correct header, CHROM/POS/REF/ALT/QUAL/FILTER/INFO columns).
5. Compare your called variants against your known ground-truth mutations: report **precision, recall, and F1** (true positives = correctly called known mutations; false positives = calls not in ground truth; false negatives = known mutations you missed).
6. Investigate any false negatives/positives — are they near indels, at low coverage, or near read ends? This is exactly the kind of debugging real variant-calling QC involves.

## Practice Project 10.2 — VCF analysis toolkit

**Spec:**
1. Download a real, small public VCF (e.g., a subset of 1000 Genomes Project data for one chromosome region).
2. Parse it with `pysam.VariantFile` or manually.
3. Build a report: total variants, count by type (SNP/insertion/deletion), transition/transversion ratio (Ts/Tv — a classic QC metric; real human whole-genome data has Ts/Tv ≈ 2.0-2.1, and a value far from that signals quality problems), and allele frequency distribution.
4. Filter variants by a quality threshold and annotate which fall inside coding regions using a GTF file (interval overlap — reuse ideas from BED/GTF parsing in Ch.8).

**Done when:** your naive caller achieves reasonable precision/recall on the simulated ground-truth data, and you can explain what Ts/Tv ratio is and why it's used as a sanity check.

Next: `11_rna_seq_gene_expression.md`.
