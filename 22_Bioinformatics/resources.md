# Resources

## Learning platforms
- Rosalind (rosalind.info) — bioinformatics programming problems, beginner to advanced
- Coursera: "Bioinformatics Specialization" (UC San Diego)
- NCBI's own tutorials and YouTube channel
- Software Carpentry / Data Carpentry — general scientific computing skills

## Documentation
- Biopython: biopython.org/docs
- pysam: pysam.readthedocs.io
- samtools/bcftools: samtools.github.io
- GATK: gatk.broadinstitute.org
- Bioconductor (R): bioconductor.org

## Public data sources
- NCBI (nucleotide, gene, PubMed, SRA): ncbi.nlm.nih.gov
- Ensembl: ensembl.org
- UniProt: uniprot.org
- GEO (Gene Expression Omnibus): ncbi.nlm.nih.gov/geo
- TCGA (The Cancer Genome Atlas): portal.gdc.cancer.gov
- 1000 Genomes Project: internationalgenome.org
- UCSC Genome Browser: genome.ucsc.edu

## Command-line tools to install as you progress
```bash
mamba install -c bioconda -c conda-forge \
  biopython pysam samtools bcftools bwa bowtie2 \
  fastqc multiqc trimmomatic cutadapt \
  spades flye quast mafft iqtree \
  gatk4 snpeff salmon
```

## Workflow managers (for productionizing pipelines)
- Snakemake — Python-based, great for learners already comfortable with Python
- Nextflow — widely used in industry/large consortia

## Communities
- Biostars (biostars.org) — Q&A forum
- r/bioinformatics
- SEQanswers forum
