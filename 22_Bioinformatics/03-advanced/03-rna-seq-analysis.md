# 03 — RNA-Seq Analysis

RNA-seq measures gene expression genome-wide. Core question: which genes are up/down-regulated between conditions (e.g. treated vs. control, tumor vs. normal)?

## Pipeline overview

```
raw reads → QC/trim → align or pseudo-align → quantify → normalize → differential expression → pathway analysis
```

## Step 1: Quantification with pseudo-alignment (fast, modern approach)

```bash
# Build index once
salmon index -t transcripts.fasta -i salmon_index

# Quantify each sample
salmon quant -i salmon_index -l A \
  -1 sample_R1.fastq.gz -2 sample_R2.fastq.gz \
  -p 4 -o sample_quant
```

Output: `sample_quant/quant.sf` — a table of transcript-level counts (TPM, estimated reads).

## Step 2: Load counts into Python

```python
import pandas as pd

quant = pd.read_csv("sample_quant/quant.sf", sep="\t")
print(quant[["Name", "TPM", "NumReads"]].sort_values("TPM", ascending=False).head(10))
```

## Building a gene x sample count matrix across many samples

```python
import pandas as pd
import glob

samples = glob.glob("*_quant/quant.sf")
dfs = []
for path in samples:
    sample_name = path.split("_quant")[0]
    df = pd.read_csv(path, sep="\t")[["Name", "NumReads"]]
    df = df.rename(columns={"NumReads": sample_name}).set_index("Name")
    dfs.append(df)

count_matrix = pd.concat(dfs, axis=1)
count_matrix.to_csv("count_matrix.csv")
print(count_matrix.head())
```

## Step 3: Differential expression (Python: PyDESeq2)

```python
import pandas as pd
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats

counts = pd.read_csv("count_matrix.csv", index_col=0).T.round().astype(int)
metadata = pd.DataFrame({
    "condition": ["control", "control", "treated", "treated"]
}, index=counts.index)

dds = DeseqDataSet(counts=counts, metadata=metadata, design="~condition")
dds.deseq2()

stats = DeseqStats(dds, contrast=["condition", "treated", "control"])
stats.summary()
results = stats.results_df
results.to_csv("differential_expression.csv")

significant = results[(results.padj < 0.05) & (abs(results.log2FoldChange) > 1)]
print(f"{len(significant)} significantly differentially expressed genes")
```

(Equivalent classic workflow in R uses DESeq2/edgeR — very common in wet-lab-adjacent teams; same statistical ideas.)

## Use case: volcano plot of results

```python
import matplotlib.pyplot as plt
import numpy as np

results["neg_log10_padj"] = -np.log10(results["padj"])
colors = ["red" if (p < 0.05 and abs(lfc) > 1) else "grey"
          for p, lfc in zip(results["padj"], results["log2FoldChange"])]

plt.figure(figsize=(8, 6))
plt.scatter(results["log2FoldChange"], results["neg_log10_padj"], c=colors, s=8, alpha=0.6)
plt.axvline(1, ls="--", color="black", lw=0.5)
plt.axvline(-1, ls="--", color="black", lw=0.5)
plt.axhline(-np.log10(0.05), ls="--", color="black", lw=0.5)
plt.xlabel("log2 Fold Change")
plt.ylabel("-log10 adjusted p-value")
plt.title("Volcano Plot: Treated vs Control")
plt.savefig("volcano_plot.png", dpi=150)
```

## Step 4: Pathway / enrichment analysis

```python
import gseapy as gp

gene_list = significant.index.tolist()
enrichment = gp.enrichr(
    gene_list=gene_list,
    gene_sets=["KEGG_2021_Human", "GO_Biological_Process_2021"],
    outdir="enrichr_results"
)
print(enrichment.results.sort_values("Adjusted P-value").head(10))
```

## Exercise

1. Build a gene x sample count matrix from several `quant.sf` outputs and normalize it to counts-per-million (CPM).
2. Run PyDESeq2 on a two-condition dataset and export the top 20 differentially expressed genes.
3. Take the significant gene list and run enrichment analysis; report the top 5 enriched pathways.

**Next:** `04-machine-learning-genomics.md`
