# 02 — Variant Calling

Identify positions where a sample's DNA differs from a reference (SNPs, indels) — the basis of clinical genomics, GWAS, and cancer genomics.

## Pipeline overview

```
raw reads → align (BWA) → sort/dedupe → base quality recalibration → call variants (GATK/bcftools) → filter → annotate
```

## Step 1: Align + prepare BAM (recap from NGS processing)

```bash
bwa mem -t 4 reference.fasta sample_R1.fastq.gz sample_R2.fastq.gz | \
  samtools sort -o sample.sorted.bam
samtools index sample.sorted.bam

# Mark duplicates (PCR duplicates bias variant calls)
gatk MarkDuplicates -I sample.sorted.bam -O sample.dedup.bam -M dup_metrics.txt
samtools index sample.dedup.bam
```

## Step 2: Call variants

```bash
# GATK HaplotypeCaller (gold standard, more accurate, slower)
gatk HaplotypeCaller -R reference.fasta -I sample.dedup.bam -O sample.vcf.gz

# bcftools (faster, good for quick pipelines)
bcftools mpileup -f reference.fasta sample.dedup.bam | bcftools call -mv -Oz -o sample.vcf.gz
bcftools index sample.vcf.gz
```

## Step 3: Filter variants

```bash
gatk VariantFiltration \
  -R reference.fasta -V sample.vcf.gz \
  --filter-expression "QD < 2.0" --filter-name "lowQD" \
  --filter-expression "FS > 60.0" --filter-name "highFS" \
  -O sample.filtered.vcf.gz
```

## Parsing and analyzing VCFs in Python

```python
import pysam

vcf = pysam.VariantFile("sample.filtered.vcf.gz")

snps = indels = passed = 0
for rec in vcf:
    if rec.filter.keys() == ["PASS"] or len(rec.filter.keys()) == 0:
        passed += 1
    if len(rec.ref) == 1 and all(len(a) == 1 for a in rec.alts):
        snps += 1
    else:
        indels += 1

print(f"SNPs: {snps}, Indels: {indels}, Passed filters: {passed}")
```

## Use case: building a variant summary table

```python
import pysam
import pandas as pd

vcf = pysam.VariantFile("sample.filtered.vcf.gz")
rows = []
for rec in vcf:
    rows.append({
        "chrom": rec.chrom,
        "pos": rec.pos,
        "ref": rec.ref,
        "alt": ",".join(str(a) for a in rec.alts),
        "qual": rec.qual,
        "filter": ";".join(rec.filter.keys()) or "PASS",
        "depth": rec.info.get("DP"),
    })

df = pd.DataFrame(rows)
df.to_csv("variants_summary.csv", index=False)
print(df[df.filter == "PASS"].sort_values("qual", ascending=False).head(10))
```

## Annotation: what do these variants mean?

```bash
# SnpEff annotates variants with predicted functional effect
snpEff GRCh38.99 sample.filtered.vcf.gz > sample.annotated.vcf
```

```python
import pysam

vcf = pysam.VariantFile("sample.annotated.vcf")
for rec in vcf:
    ann = rec.info.get("ANN")
    if ann:
        effect = ann[0].split("|")[1]   # e.g. "missense_variant"
        gene = ann[0].split("|")[3]
        print(f"{rec.chrom}:{rec.pos} {rec.ref}>{rec.alts[0]} — {effect} in {gene}")
```

## Use case: comparing variants between two samples (tumor vs normal)

```bash
bcftools isec -p compare_out/ tumor.vcf.gz normal.vcf.gz
# compare_out/0000.vcf = tumor-only (somatic candidates)
```

```python
import pysam

tumor_only = pysam.VariantFile("compare_out/0000.vcf")
somatic_candidates = [(r.chrom, r.pos, r.ref, r.alts) for r in tumor_only]
print(f"{len(somatic_candidates)} candidate somatic variants")
```

## Exercise

1. From a filtered VCF, compute the transition/transversion (Ts/Tv) ratio — a common QC metric (expect ~2.0-2.1 for whole genomes).
2. Annotate a VCF with SnpEff and count variants by predicted effect category (missense, synonymous, frameshift, etc.).
3. Given tumor and normal VCFs, identify and list somatic (tumor-only) variants with quality ≥ 30.

**Next:** `03-rna-seq-analysis.md`
