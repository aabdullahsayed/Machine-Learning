# 1. Setup & Environment

## Why this matters
Bioinformatics work fails or succeeds on reproducibility. A pipeline that only runs on your laptop is a liability. We set up a clean, reproducible environment from day one.

## Core tools

- **Python 3.10+** — main language for this course
- **conda / mamba** — manages bioinformatics packages with compiled binaries (samtools, bwa, blast) that pip can't handle well
- **Biopython** — the standard library for sequence/file-format handling
- **Jupyter** — for exploratory analysis
- **Git** — every project goes in version control
- **samtools / bwa / blast+** — command-line bioinformatics tools we'll call from Python

## Install

```bash
# Install miniconda if you don't have it, then:
conda create -n bioinfo python=3.11 -y
conda activate bioinfo
conda install -c bioconda -c conda-forge biopython samtools bwa blast pandas numpy scipy matplotlib scikit-learn jupyter -y
pip install seaborn
```

Verify:
```bash
python -c "import Bio; print(Bio.__version__)"
samtools --version
blastn -version
```

## Project directory convention (use for every project in this course)

```
project-name/
  data/          # raw + downloaded data (gitignore large files)
  scripts/       # your code
  results/       # output files, plots
  notebooks/     # exploratory Jupyter notebooks
  README.md      # what the project does and how to run it
```

## Practice Project 1.1 — "Bio-env" reproducible starter kit

**Goal:** build a template repo you'll reuse for every future project in this course.

**Steps:**
1. Create a git repo `bioinfo-template/`.
2. Add an `environment.yml`:
   ```yaml
   name: bioinfo
   channels: [bioconda, conda-forge]
   dependencies:
     - python=3.11
     - biopython
     - samtools
     - bwa
     - blast
     - pandas
     - numpy
     - scipy
     - matplotlib
     - scikit-learn
   ```
3. Add a `Makefile` (or simple `run.sh`) with targets: `setup`, `test`, `clean`.
4. Write a `scripts/check_env.py` that imports Biopython and prints the version, and shell-calls `samtools --version`, failing loudly if anything is missing.
5. Commit and tag `v0.1`.

**Stretch goal:** containerize it with a `Dockerfile` based on `continuumio/miniconda3`.

**Done when:** running `bash run.sh setup && python scripts/check_env.py` on a fresh machine works with zero manual fixes.

Next: `02_molecular_biology_primer.md`.
