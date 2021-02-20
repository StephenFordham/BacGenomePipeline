BacGenomePipeline

Complete Bacterial Genome Assembly and Annotation Pipeline

Program developed by Stephen Fordham


General Description

BacGenomePipeline is a complete convenience bacterial genome assembly pipeline. Assembled and annotated bacterial
genomes can be created with only raw reads as input! BacGenomePipeline can accept either fastq or gzipped fastq files.
Relax and grab a coffee while BacGenomePipeline does the genomic heavy lifting.


This pipeline filters raw reads to produce the best 500mb reads.
The filtering process also places weight on read quality, to ensure small high quality reads are not discarded.
This is considered vital to aid the recovery of small plasmids present within bacterial strains.


Optionally, the user can run Nanostat to assess read quality metrics. The best reads are then assembled using the
flye genome assembler with settings adjusted to help recovery of plasmids with an imbalanced distribution.
Optionally, the assembly is then polished with one round of medaka-consensus polishing. The polished assembly is annotated 
using staramr which scans bacterial genome contigs against the ResFinder, PointFinder, and PlasmidFinder databases
(used by the ResFinder webservice and other webservices offered by the Center for Genomic Epidemiology) and abricate and 
compiles a summary report of detected antimicrobial resistance and virulence genes.

Additionally, BacGenomePipeline can be run in 4 modes. 

These modes include:

1. --pipeline        Running the entire pipeline workflow,
2. --pipe_red_mem    Running the pipeline using reduced memory by setting parameters for genome size and coverage for initial disjointings, 
3. --assembly        Running a genome only assembly 
4. --annotation      Running the annotation step on an pre-exisiing genome assembly in FASTA format.

For usage instructions, run:

    BacGenomePipeline --help

Currently BacGenomePipeline has been tested and runs on Linux OS.

To run BacGenomePipeline, you must also install the following programs by running the following commands:

    conda install -c bioconda filtlong==0.2.0

    conda install -c bioconda flye==2.8.1
    
    conda install -c bioconda abricate==1.0.1




