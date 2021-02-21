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
         * [BacGenomePipeline](#bacgenomepipeline-1)
      * [General Description](#general-description-1)
      * [Installation requirements](#installation-requirements)
         * [Conda Install](#conda-install)
         * [Pip Install](#pip-install)
      * [Usage Instructions](#usage-instructions)
         * [Example Usage](#example-usage)
         * [Example usage on the command line](#example-usage-on-the-command-line)
            * [Pipeline mode](#pipeline-mode)
            * [Pipeline reduced memory mode](#pipeline-reduced-memory-mode)
            * [Assembly mode](#assembly-mode)
            * [Annotation mode](#annotation-mode)
      * [Example Output](#example-output)
      * [References](#references)



## General Description

### BacGenomePipeline

Complete Bacterial Genome Assembly and Annotation Pipeline

Program developed by Stephen Fordham


## General Description

BacGenomePipeline is a complete convenience bacterial genome assembly pipeline. Assembled and annotated bacterial
genomes can be created with only Oxford Nanopore long raw reads as input! BacGenomePipeline can accept 
either fastq or gzipped fastq files.

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

The default settings selected in BacGenomePipeline have been tested against challenging gemomes, such as _Klebsiella pneumoniae_ 
strain ATCC700721/MGH78578. This strain contains 2 small plasmids (3.4kb and 4.2kb), two medium sized plasmids (88kb and 107.5kb),
and one large plasmid (175kb) in addtion to the chromosome (5.3mb). The pipeline was able to successfully build to closure (i.e.
assemble as a circular unitig) all structures exlusively using ONT long reads! 

BacGenomePipline can now be run in 4 modes. These modes include; pipeline, pipe_red_mem, assembly and annotation. These modes
offer the user more flexibility when using BacGenomePipe. For example, the user may want to _only_ run an assembly, alternatively the 
user may have a gemome assembly in FASTA format and want to annotate the assembly for antimicrobial resistance and virulence genes.

BacGenomePipeline can be run in 4 modes. 

These modes include:
1. Running the entire pipeline workflow. <br>
  ```--pipeline```
2. Running the pipeline using reduced memory by setting parameters for genome size and coverage for initial disjointings. <br>
  ```--pipe_red_mem```
3.  Running a genome only assembly. <br>
  ```--assembly```
4. Running the annotation step on an pre-exisiing genome assembly in FASTA format. <br>
```--annotation```

<br>
For usage instructions, run:

    BacGenomePipeline --help


Currently, BacGenomePipeline has been tested and runs on Linux OS.


<a href="https://anaconda.org/stephenfordham/bacgenomepipeline">BacGenomePipeline on Conda</a> <br><br>
<a href="https://pypi.org/project/BacGenomePipeline/">BacGenomePipeline on PYPI </a> <br>


<br>

## Installation requirements
### Conda Install
[![Anaconda-Server Badge](https://anaconda.org/stephenfordham/bacgenomepipeline/badges/installer/conda.svg)](https://anaconda.org/StephenFordham/bacgenomepipeline
) 
[![Anaconda-Server Badge](https://anaconda.org/stephenfordham/bacgenomepipeline/badges/platforms.svg)](https://anaconda.org/stephenfordham/bacgenomepipeline)

The simplest way to install BacGenomePipeline is running the following command:

    conda install -c stephenfordham bacgenomepipeline

I recommend installing BacGenomePipeline in a conda virtual environment:
For example:

    conda create -n pipeline
    
    conda activate pipeline
    
    (pipeline) conda install -c stephenfordham bacgenomepipeline

Enter y, when promoted to install dependenies in your terminal window. 

### Pip Install

Alternatively you can run the following commands:

     pip install BacGenomePipeline
     conda install -c bioconda filtlong==0.2.0
     conda install -c bioconda flye==2.8.1
     conda install -c bioconda abricate==1.0.1
     

## Usage Instructions

For useful usage instructions, run
```BacGenomePipline --help```

BacGenomePipline can be run in one of four usage modes. The usage mode must be specified explicitly in the terminal.
A selection of examples of BacGenomePipeline run in different usage modes is shown at the bottom of the help
message and in the usage example section on this page.

    usage: BacGenomePipeline (--pipeline | --pipe_red_mem | --assembly | --annotation)
    --fastq_file READS
           --help --version
           [--nanostats] [--medaka_polish]
           [--mean_q_weight] [--asm_fasta]
           [--genome_size SIZE]  [--asm_coverage INT]
           [--flye_dir DIR_NAME] [--polished_dir DIR_NAME]
           [--amr_dir DIR_NAME]  [--vir_dir DIR_NAME]

    Complete Bacterial Genome Assembly and Annotation Pipeline

    optional arguments:
      -h, --help            show this help message and exit
      --pipeline            Runs the entire Pipeline
      --pipe_red_mem        Runs the entire Pipeline with reduced memory
                            consumption
      --assembly            Runs the assembly portion of the pipeline
      --annotation          Runs the annotation portion of the pipeline

    Version:
      --version             Print version and exit.

    Input fastq Reads (a fastq file is required):
      -f , --fastq_file     Specify an input Fastq file for the Pipeline and
                            assembly modes

    Pipeline Options:
      -n, --nanostats       Optionally run NanoStats on your filtered read set
      -m, --medaka_polish   Optionally run NanoStats on your filtered read set
      -s , --asm_fasta      Add Genome assembly in fasta format
      -w , --q_weight       Add mean_q_weight for read filtering

    Optional flye assembly arguments
    (To reduce memory consumption for large genome assemblies):
      -g , --genome_size    Estimated genome size (for example, 5m or 2.6g)
      -c , --asm_coverage   reduced coverage for initial disjointig assembly [not
                            set]

    Directory names:
      -d , --flye_dir       Specify a flye genome assembly directory name
      -p , --polished_dir   Specify a medaka polished genome directory name
      -a , --amr_dir        Specify a antimicrobial resistance directory name
      -v , --vir_dir        Specify a virulence gene directory name

    Did you know? BacGenomePipeline can be run in modes

    These modes include: pipeline, which runs the entire BacGenomePipeline workflow,
    pipe_red_mem, which uses less memory by using use a subset of the longest reads 
    for initial disjointig by specifying --asm-coverage and --genome-size options. 
    The assembly mode runs assembly and polishing steps only. For this step, 
    annotation is excluded. Finally the annotation mode takes a genome assembly and 
    annotates it for antimicrobial and virulence genes 

    Example Usage:
    BacGenomePipeline --pipeline -f reads.fastq
    BacGenomePipeline --pipeline -f reads.fastq.gz -m -n
    BacGenomePipeline --pipe_red_mem -f reads.fastq -g 5.7m -c 40 -n -m
    BacGenomePipeline --annotation -s assembly.fasta
    BacGenomePipeline --assembly -f reads.fastq -n -m

              
       
### Example Usage 
    BacGenomePipeline --pipeline -f reads.fastq
    BacGenomePipeline --pipeline -f reads.fastq.gz -m -n
    BacGenomePipeline --pipe_red_mem -f reads.fastq -g 5.7m -c 40 -n -m
    BacGenomePipeline --annotation -s assembly.fasta
    BacGenomePipeline --assembly -f reads.fastq -n -m

    
<br>

### Example usage on the command line 
#### Pipeline mode 
<img src=https://github.com/StephenFordham/BacGenomePipeline/blob/main/static/pipeline_mode.png />

#### Pipeline reduced memory mode 
<img src=https://github.com/StephenFordham/BacGenomePipeline/blob/main/static/pipe_red_mem_mode.png />

#### Assembly mode
<img src=https://github.com/StephenFordham/BacGenomePipeline/blob/main/static/assembly_only_mode.png />

#### Annotation mode 
<img src=https://github.com/StephenFordham/BacGenomePipeline/blob/main/static/annotation_mode.png />

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

<img src=https://github.com/StephenFordham/BacGenomePipeline/blob/main/static/virulence_metadata.png />

<sub>Figure 3  Sample virulence gene data obtained when the entire pipeline or the annotaion portion of the pipeline runs </sub><br>

<br>

## References


<u><b>Program References:</b></u><br>
<a href="https://github.com/rrwick/Filtlong">Filtlong</a> <br>
<a href="https://pypi.org/project/medaka/">Medaka</a> <br>
<a href="https://pypi.org/project/NanoStat/">NanoStat</a> <br>
<a href="https://anaconda.org/bioconda/flye">Flye</a> <br>
<a href="https://github.com/rrwick/Filtlong">Filtlong</a> <br>







 







    
    
       
       
       
       
       
       
       
       
       
       
       
       
   

