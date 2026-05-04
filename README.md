# ChIP-seq-Pipeline-Epigenetic-Control-of-Gene-Expression
This repository contains the implementation of a full ChIP-seq (Chromatin Immunoprecipitation Sequencing) analysis pipeline, developed through the specialization course led by Alexander Abdulkader Kheirallah, PhD. The project focuses on assessing the effect of epigenetic modifications on gene expression at a genome-wide level.
Scientific Context
Chromatin immunoprecipitation followed by next-generation sequencing (ChIP-seq) is a powerful technique for studying cell identity and cell-specific gene expression. This project utilizes NGS data to identify protein-DNA interaction sites and histone modifications across the genome.

Bioinformatics Workflow
The analysis is conducted within a Linux/HPC and R environment using Conda for version control and Docker for reproducibility.

Quality Control: Raw read assessment using FastQC.

Alignment: Genome indexing and read mapping using Bowtie2.

Data Filtering: Post-alignment processing to remove low-quality mappings and duplicates.

Peak Calling: Identification of enriched genomic regions using the MACS3 algorithm.

Interpretation: Functional study principles applied to interpret epigenetic data and environmental interactions.

Technical Stack
Environment: Docker, Conda, UNIX Command Line

Languages: R, Bash

Tools: FastQC, Bowtie2, MACS3

Project Structure
/scripts: Bash and R scripts for the automated pipeline.

/configs: Conda environment .yml files and Docker setup instructions.

capstone_project.md: Summary of the final analysis and biological interpretation of the provided NGS dataset.
