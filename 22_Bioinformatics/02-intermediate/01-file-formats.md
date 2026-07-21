# 01 — Bioinformatics File Formats

Real pipelines live and die by correct file format handling. Know these cold.

## FASTA — sequences

```
>seq1 optional description
ATGGCCATTGTAATGGGCCGCTGA
>seq2
GGGATCCATGGCATCGTAGCTAGC
```
Used for: reference genomes, gene sets, protein sequences.

## FASTQ — sequencing reads + quality

```
@read1
ATGGCCATTGTA
+
IIIIIIIIIIII
```
4 lines per read: id, sequence, `+` separator, quality (Phred-encoded ASCII).

```python
from Bio import SeqIO

for rec in SeqIO.parse("reads.fastq", "fastq"):
    avg_q = sum(rec.letter_annotations["phred_quality"]) / len(rec.seq)
    if avg_q < 20:
        print(f"Low quality read: {rec.id} (avg Q={avg_q:.1f})")
```

## SAM/BAM — aligned reads

SAM (text) / BAM (binary, compressed) store reads aligned to a reference genome, with position, CIGAR string (alignment shape), and mapping quality.

```python
import pysam

bam = pysam.AlignmentFile("aligned.bam", "rb")
for read in bam.fetch("chr1", 1000, 2000):
    print(read.query_name, read.reference_start, read.cigarstring)
bam.close()
```

Command-line essentials:
```bash
samtools view -h aligned.bam | head        # inspect
samtools sort aligned.bam -o sorted.bam    # sort by coordinate
samtools index sorted.bam                  # create .bai index for random access
```

## VCF — variants

```
##fileformat=VCFv4.2
#CHROM  POS   ID   REF  ALT  QUAL  FILTER  INFO
chr1    12345 rs1  A    G    99    PASS    DP=30
```

```python
import pysam

vcf = pysam.VariantFile("variants.vcf")
for rec in vcf:
    print(rec.chrom, rec.pos, rec.ref, rec.alts, rec.qual)
```

## BED — genomic intervals

```
chr1  1000  2000  feature1  0  +
chr1  5000  5500  feature2  0  -
```
Tab-separated: chrom, start (0-based), end, name, score, strand. Used for gene annotations, peaks, regions of interest.

```python
import pandas as pd

bed = pd.read_csv("regions.bed", sep="\t", header=None,
                   names=["chrom", "start", "end", "name", "score", "strand"])
print(bed[bed.chrom == "chr1"])
```

## GFF/GTF — gene annotation

```
chr1  ensembl  gene  1000  9000  .  +  .  gene_id "GENE1"; gene_name "TP53";
```
Describes genes, exons, transcripts and their coordinates.

```python
import pandas as pd

cols = ["seqid","source","type","start","end","score","strand","frame","attributes"]
gtf = pd.read_csv("annotation.gtf", sep="\t", comment="#", names=cols)
genes = gtf[gtf.type == "gene"]
print(len(genes), "genes found")
```

## Use case: quick QC summary across formats

```python
from Bio import SeqIO

def fasta_summary(path):
    lengths = [len(r.seq) for r in SeqIO.parse(path, "fasta")]
    return {
        "n_sequences": len(lengths),
        "total_bp": sum(lengths),
        "avg_length": sum(lengths) / len(lengths) if lengths else 0,
        "max_length": max(lengths, default=0),
    }

print(fasta_summary("genes.fasta"))
```

## Exercise

1. Write a script that reads a FASTQ file and reports the % of reads with average quality ≥ 30.
2. Parse a GTF and count how many genes are on each strand (+/-).
3. Given a BED file and a FASTA reference, extract the sequence under each interval (hint: `Bio.Seq` slicing + coordinates).

**Next:** `02-sequence-alignment.md`
