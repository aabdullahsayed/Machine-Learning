# Bioinformatics + Programming: Beginner to Advanced

A structured, hands-on roadmap for learning bioinformatics through programming (mostly Python, with some R and shell). Each stage has focused Markdown notes, real use cases, code snippets, and exercises.

## How to use this folder

Work through the folders in order. Each `.md` file has:
- **Concept explanation**
- **Real-world use case**
- **Code example**
- **Practice exercise**
- **Tools/libraries used**

```
bioinformatics-learning/
├── README.md                          <- you are here
├── 01-beginner/
│   ├── 01-introduction.md
│   ├── 02-python-basics-for-bioinformatics.md
│   ├── 03-sequence-analysis-basics.md
│   └── 04-biopython-intro.md
├── 02-intermediate/
│   ├── 01-file-formats.md
│   ├── 02-sequence-alignment.md
│   ├── 03-ngs-data-processing.md
│   └── 04-databases-apis.md
├── 03-advanced/
│   ├── 01-genome-assembly.md
│   ├── 02-variant-calling.md
│   ├── 03-rna-seq-analysis.md
│   ├── 04-machine-learning-genomics.md
│   └── 05-phylogenetics.md
├── 04-projects/
│   └── project-ideas.md
└── resources.md
```

## Suggested learning path

| Stage | Focus | Duration (self-paced) |
|---|---|---|
| Beginner | Python + biology fundamentals, simple sequence scripts | 2-4 weeks |
| Intermediate | File formats, alignments, NGS pipelines, public databases | 4-6 weeks |
| Advanced | Assembly, variant calling, RNA-seq, ML on genomic data, phylogenetics | 6-10 weeks |
| Projects | Apply everything to portfolio-worthy projects | Ongoing |

## Core toolchain you'll install along the way

- **Python 3.10+**, `pip`, `conda`/`mamba`
- **Biopython** — sequence parsing, I/O, alignments
- **pandas / numpy** — tabular & numerical data
- **matplotlib / seaborn** — visualization
- **scikit-bio, pysam, scikit-learn** — advanced analysis & ML
- **Command-line tools**: BLAST, samtools, bcftools, bwa/bowtie2, GATK, SPAdes, FastQC, MultiQC
- **R + Bioconductor** (optional but common in RNA-seq/DE analysis: DESeq2, edgeR)

Start with `01-beginner/01-introduction.md`.
