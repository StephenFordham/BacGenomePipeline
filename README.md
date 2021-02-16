# BacGenomePipeline

## Complete Bacterial Genome Assembly and Annotation Pipeline
#### Program developed by Stephen Fordham
<br>

<img src=https://github.com/StephenFordham/BacGenomePipeline/blob/main/static/nanopore_squiggle.png width=1000 >


Table of Contents
=================

   * [BacGenomePipeline](#bacgenomepipeline)
      * [Complete Bacterial Genome Assembly and Annotation Pipeline](#complete-bacterial-genome-assembly-and-annotation-pipeline)
      * [General Description](#general-description)
      * [Installation requirements](#installation-requirements)
         * [Conda Install](#conda-install)
         * [Pip Install](#pip-install)
      * [Usage Instructions](#usage-instructions)
         * [Example Usage (Short argument flags)](#example-usage-short-argument-flags)
         * [Example Usage (Long argument flags)](#example-usage-long-argument-flags)
         * [Terminal Output](#terminal-output)
      * [Example Output](#example-output)
      * [References](#references)

## General Description


BacGenomePipeline is a complete convenience bacterial genome assembly pipeline. Assembled and annotated bacterial genomes can be created with only raw reads as input! BacGenomePipeline can accept either fastq or gzipped fastq files. Relax and grab a coffee while BacGenomePipeline does the genomic heavy lifting.

This pipeline filters raw reads to produce the best 500mb reads. The filtering process also places weight on read quality, to ensure small high quality reads are not discarded. This is considered vital to aid the recovery of small plasmids present within bacterial strains.

Optionally, the user can run Nanostat to assess read quality metrics. The best reads are then assembled using the flye genome assembler with settings adjusted to help recovery of plasmids with an imbalanced distribution. The assembly is then polished with one round of medaka-consensus polishing. The polished assembly is annotated using staramr which scans bacterial genome contigs against the ResFinder, PointFinder, and PlasmidFinder databases (used by the ResFinder webservice and other webservices offered by the Center for Genomic Epidemiology) and compiles a summary report of detected antimicrobial resistance genes. 

Currently BacGenomePipeline has been tested and runs on Linux OS.



<a href="https://anaconda.org/stephenfordham/bacgenomepipeline">BacGenomePipeline on Conda</a> <br><br>
<a href="https://pypi.org/project/BacGenomePipeline/">BacGenomePipeline on PYPI </a> <br>


<br>

## Installation requirements
### Conda Install
[![Anaconda-Server Badge](https://anaconda.org/stephenfordham/bacgenomepipeline/badges/installer/conda.svg)](https://conda.anaconda.org/stephenfordham) 
[![Anaconda-Server Badge](https://anaconda.org/stephenfordham/bacgenomepipeline/badges/platforms.svg)](https://anaconda.org/stephenfordham/bacgenomepipeline)

The simplest way to install BacGenomePipeline is running the following command:

    conda install -c stephenfordham bacgenomepipeline

I recommend installing BacGenomePipeline in a conda virtual environment:
For example:

    conda create -n bio_venv
    
    conda activate bio_venv
    
    (bio_venv) conda install -c stephenfordham bacgenomepipeline

Enter y, when promoted to install dependenies in your terminal window. 

### Pip Install

Alternatively you can run the following commands:

     pip install BacGenomePipeline
     conda install -c bioconda filtlong==0.2.0
     conda install -c bioconda flye==2.8.1
     

## Usage Instructions


```usage: BacGenomePipeline [-h] -f  [-n] -d  -p -a```

              Complete Bacterial Genome Assembly and Annotation Pipeline

              optional arguments:
              -h,  --help           show this help message and exit
              -f , --fastq_file     Specify an input Fastq file for the Pipeline
              -n,  --nanostats      Optionally run a NanoStats report on your filtered read set
              -d , --flye_dir       Specify a Flye Genome assembly directory name
              -p , --polished_dir   Specify a Medaka Polished genome directory name
              -a , --amr_dir        Specify a Antimicrobial resistance directory name
              
       
### Example Usage (Short argument flags)

    BacGenomePipeline -f reads.fastq -n -d flye_amr_dir -p pol_dir -a bac_amr_dir
    
### Example Usage (Long argument flags)

    BacGenomePipeline --fastq_file reads.fastq --nanostats --flye_dir flye_asm_dir --polished_dir complete_pol_dir --amr_dir bac_amr_dir
    
<br>

### Terminal Output

<img src=https://github.com/StephenFordham/BacGenomePipeline/blob/main/static/terminal_output.png >


## Example Output


Assembly of extensively-drug resistant (XDR) strain _Klebsiella pneumoniae_ ATCC700721 <br>
assembly.gfa file in flye directory rendered via Bandage


<img src=https://github.com/StephenFordham/BacGenomePipeline/blob/main/static/bacterial_assembly.png width=500/>


<sub>Figure 1. Whole genome assembly XDR of _K. pneumoniae_ ATCC700721 <br>
1 completely closed chromosome <br>
5 completely closed plasmids <br>
</sub>

<br>

<img src=https://github.com/StephenFordham/BacGenomePipeline/blob/main/static/bac_data_update.png  width=650  />

<sub>Figure 2  Sample AMR data available via amr_dir </sub><br>


<br>

## References


<u><b>Program References:</b></u><br>
<a href="https://github.com/rrwick/Filtlong">Filtlong</a> <br>
<a href="https://pypi.org/project/medaka/">Medaka</a> <br>
<a href="https://pypi.org/project/NanoStat/">NanoStat</a> <br>
<a href="https://anaconda.org/bioconda/flye">Flye</a> <br>
<a href="https://github.com/rrwick/Filtlong">Filtlong</a> <br>







 







    
    
       
       
       
       
       
       
       
       
       
       
       
       
   

