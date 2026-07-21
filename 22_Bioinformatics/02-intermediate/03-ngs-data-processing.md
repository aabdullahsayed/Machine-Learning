# 03 — NGS (Next-Generation Sequencing) Data Processing

A typical NGS pipeline: raw reads → QC → trimming → alignment → sorting/indexing → downstream analysis (variants, expression, etc.)

## Step 1: Quality control

```bash
fastqc reads_R1.fastq.gz reads_R2.fastq.gz
multiqc .    # aggregates FastQC (and other tool) reports into one HTML
```

Parse FastQC results programmatically:

```python
import zipfile, re

with zipfile.ZipFile("reads_R1_fastqc.zip") as z:
    data = z.read("reads_R1_fastqc/fastqc_data.txt").decode()

match = re.search(r"%GC\t(\d+)", data)
print("GC%:", match.group(1) if match else "not found")
```

## Step 2: Adapter/quality trimming

```bash
# Trimmomatic
trimmomatic PE reads_R1.fastq.gz reads_R2.fastq.gz \
  trimmed_R1.fastq.gz unpaired_R1.fastq.gz \
  trimmed_R2.fastq.gz unpaired_R2.fastq.gz \
  ILLUMINACLIP:adapters.fa:2:30:10 SLIDINGWINDOW:4:20 MINLEN:36

# or cutadapt
cutadapt -a AGATCGGAAGAGC -q 20 -m 36 \
  -o trimmed_R1.fastq.gz reads_R1.fastq.gz
```

## Step 3: Alignment to a reference genome

```bash
# Build index once
bwa index reference.fasta

# Align paired-end reads
bwa mem -t 4 reference.fasta trimmed_R1.fastq.gz trimmed_R2.fastq.gz > aligned.sam

# Convert, sort, index
samtools view -bS aligned.sam | samtools sort -o aligned.sorted.bam
samtools index aligned.sorted.bam
```

## Step 4: Alignment QC in Python

```python
import pysam

bam = pysam.AlignmentFile("aligned.sorted.bam", "rb")

total = mapped = duplicates = 0
for read in bam:
    total += 1
    if not read.is_unmapped:
        mapped += 1
    if read.is_duplicate:
        duplicates += 1

print(f"Total reads: {total}")
print(f"Mapped: {mapped} ({mapped/total*100:.1f}%)")
print(f"Duplicates: {duplicates}")
```

## Use case: coverage calculation across a region

```python
import pysam

bam = pysam.AlignmentFile("aligned.sorted.bam", "rb")
coverage = bam.count_coverage("chr1", 1000, 2000)  # returns per-base A/C/G/T depth arrays

total_depth = [sum(base[i] for base in coverage) for i in range(len(coverage[0]))]
avg_depth = sum(total_depth) / len(total_depth)
print(f"Average coverage chr1:1000-2000 = {avg_depth:.1f}x")
```

Or from the command line for whole-genome summaries:
```bash
samtools depth -a aligned.sorted.bam | awk '{sum+=$3} END {print "Average depth:", sum/NR}'
```

## Use case: building a lightweight pipeline script

```python
import subprocess

def run(cmd: str):
    print(f"$ {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def align_sample(sample: str, reference: str):
    run(f"bwa mem -t 4 {reference} {sample}_R1.fastq.gz {sample}_R2.fastq.gz > {sample}.sam")
    run(f"samtools sort {sample}.sam -o {sample}.sorted.bam")
    run(f"samtools index {sample}.sorted.bam")

for sample in ["sample1", "sample2", "sample3"]:
    align_sample(sample, "reference.fasta")
```

This is the seed of a real Snakemake/Nextflow pipeline (see `03-advanced` and `resources.md`).

## Exercise

1. Given a BAM file, compute the percentage of properly paired reads.
2. Write a script that iterates over multiple samples' FASTQ files, runs FastQC, and flags any sample with average quality below a threshold.
3. Compute per-chromosome average coverage and identify the chromosome with the lowest coverage.

**Next:** `04-databases-apis.md`
