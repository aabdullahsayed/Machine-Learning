# Landmark & Foundational Papers

Organized by topic. These are the papers that introduced the algorithms
and methods referenced throughout this roadmap. Read them *after* you
understand the concept from a textbook/course — papers assume more
background than textbooks and are far more rewarding once you already
grasp the basic idea.

## Sequence Alignment

- Needleman, S.B. & Wunsch, C.D. (1970). *A general method applicable to
  the search for similarities in the amino acid sequence of two
  proteins.* Journal of Molecular Biology. — origin of global alignment DP.
- Smith, T.F. & Waterman, M.S. (1981). *Identification of common
  molecular subsequences.* Journal of Molecular Biology. — local
  alignment DP.
- Altschul, S.F. et al. (1990). *Basic local alignment search tool.*
  Journal of Molecular Biology. — the original BLAST paper.
- Altschul, S.F. et al. (1997). *Gapped BLAST and PSI-BLAST.* Nucleic
  Acids Research. — BLAST improvements, still widely cited.

## Genome Assembly & Read Mapping

- Li, H. & Durbin, R. (2009). *Fast and accurate short read alignment
  with Burrows-Wheeler transform.* Bioinformatics. — the BWA paper.
- Langmead, B. et al. (2009). *Ultrafast and memory-efficient alignment
  of short DNA sequences to the human genome.* Genome Biology. — Bowtie.
- Pevzner, P.A., Tang, H., Waterman, M.S. (2001). *An Eulerian path
  approach to DNA fragment assembly.* PNAS. — foundational de Bruijn
  graph assembly paper.
- Bankevich, A. et al. (2012). *SPAdes: A New Genome Assembly Algorithm
  and Its Applications to Single-Cell Sequencing.* Journal of
  Computational Biology.

## Variant Calling & Genomics

- McKenna, A. et al. (2010). *The Genome Analysis Toolkit: A MapReduce
  framework for analyzing next-generation DNA sequencing data.* Genome
  Research. — GATK.
- 1000 Genomes Project Consortium (2015). *A global reference for human
  genetic variation.* Nature.
- International Human Genome Sequencing Consortium (2001). *Initial
  sequencing and analysis of the human genome.* Nature. — historically
  essential, worth reading for context even if methods are dated.

## RNA-seq & Differential Expression

- Mortazavi, A. et al. (2008). *Mapping and quantifying mammalian
  transcriptomes by RNA-Seq.* Nature Methods. — foundational RNA-seq
  paper.
- Love, M.I., Huber, W., Anders, S. (2014). *Moderated estimation of
  fold change and dispersion for RNA-seq data with DESeq2.* Genome
  Biology.
- Robinson, M.D., McCarthy, D.J., Smyth, G.K. (2010). *edgeR: a
  Bioconductor package for differential expression analysis of digital
  gene expression data.* Bioinformatics.
- Trapnell, C. et al. (2012). *Differential gene and transcript
  expression analysis of RNA-seq experiments with TopHat and Cufflinks.*
  Nature Protocols.

## Single-Cell Genomics

- Macosko, E.Z. et al. (2015). *Highly Parallel Genome-wide Expression
  Profiling of Individual Cells Using Nanoliter Droplets.* Cell. —
  Drop-seq.
- Satija, R. et al. (2015). *Spatial reconstruction of single-cell gene
  expression data.* Nature Biotechnology. — early Seurat paper.
- Butler, A. et al. (2018). *Integrating single-cell transcriptomic data
  across different conditions, technologies, and species.* Nature
  Biotechnology. — Seurat v2/integration methods.

## Machine Learning & Deep Learning in Biology

- Alipanahi, B. et al. (2015). *Predicting the sequence specificities of
  DNA- and RNA-binding proteins by deep learning.* Nature Biotechnology.
  — DeepBind.
- Zhou, J. & Troyanskaya, O.G. (2015). *Predicting effects of noncoding
  variants with deep learning-based sequence model.* Nature Methods. —
  DeepSEA.
- Jumper, J. et al. (2021). *Highly accurate protein structure
  prediction with AlphaFold.* Nature. — ⭐ essential reading if
  interested in structural bioinformatics at all.
- Baek, M. et al. (2021). *Accurate prediction of protein structures and
  interactions using a three-track neural network.* Science. —
  RoseTTAFold.
- Rives, A. et al. (2021). *Biological structure and function emerge
  from scaling unsupervised learning to 250 million protein sequences.*
  PNAS. — ESM protein language models.
- Avsec, Ž. et al. (2021). *Effective gene expression prediction from
  sequence by integrating long-range interactions.* Nature Methods. —
  Enformer.

## Phylogenetics

- Saitou, N. & Nei, M. (1987). *The neighbor-joining method: a new
  method for reconstructing phylogenetic trees.* Molecular Biology and
  Evolution.
- Felsenstein, J. (1981). *Evolutionary trees from DNA sequences: a
  maximum likelihood approach.* Journal of Molecular Evolution.

## How to Find & Access These

- Search titles directly on **PubMed** (pubmed.ncbi.nlm.nih.gov) or
  **Google Scholar** — most have free PDF versions via PMC (PubMed
  Central) or the authors' lab websites.
- **bioRxiv.org** — preprint server for current/unpublished
  bioinformatics research; check here for the newest work in your
  chosen track (05-specialized-topics).
- Use your university library's access for paywalled journal versions
  when PMC doesn't have a free copy.

## Reading Strategy

For each paper, write (even just to yourself) one paragraph answering:
1. What problem couldn't prior methods solve?
2. What's the core algorithmic/statistical idea?
3. What's the evidence it works (what did they benchmark against)?
4. What's a limitation the authors acknowledge or a critic could raise?

This turns passive reading into research training.
