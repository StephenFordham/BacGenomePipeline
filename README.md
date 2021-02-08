# BacGenomePipeline

## Complete Bacterial Genome Assembly and Annotation Pipeline

#### Program developed by Stephen Fordham

<br>

<img src=https://github.com/StephenFordham/BacGenomePipeline/blob/main/static/nanopore_squiggle.png width=700 >

### General Description
<hr>

Complete bacterial genome assembly pipeline. Assembled and annotated bacterial genomes can be created with only raw reads as input! BacGenomePipeline can accept either fastq or gzipped fastq files. Relax and grab a coffee while BacGenomePipeline does the genomic heavy lifting.

This pipeline filters raw reads to produce the best 500mb reads. The filtering process also places weight on read quality, to ensure small high quality reads are not discarded. This is considered vital to aid the recovery of small plasmids present within bacterial strains.

Optionally, the user can run Nanostat to assess read quality metrics. The best reads are then assembled using the flye genome assembler with settings adjusted to help recovery of plasmids with an imbalanced distribution. The assembly is then polished with one round of medaka-consensus polishing. The polished assembly is annotated using staramr which scans scans bacterial genome contigs against the ResFinder, PointFinder, and PlasmidFinder databases (used by the ResFinder webservice and other webservices offered by the Center for Genomic Epidemiology) and compiles a summary report of detected antimicrobial resistance genes. 


<br>

### Usage Instructions
<hr>
 <b>usage: python BacGenomePipeline.py [-h] -f  [-n] -d  -p -a</b>

              Complete Bacterial Genome Assembly and Annotation Pipeline

              optional arguments:
              -h,  --help           show this help message and exit
              -f , --fastq_file     Specify an input Fastq file for the Pipeline
              -n,  --nanostats      Optionally run a NanoStats report on your filtered read set
              -d , --flye_dir       Specify a Flye Genome assembly directory name
              -p , --polished_dir   Specify a Medaka Polished genome directory name
              -a , --amr_dir        Specify a Antimicrobial resistance directory name
              
       
### Example Usage (Short argument flags)

    python BacGenomePipeline.py -f reads.fastq -n -d flye_amr_dir -p pol_dir -a bac_amr_dir
    
### Example Usage (Long argument flags)

    python BacGenomePipeline.py --fastq_file reads.fastq --nanostats --flye_dir flye_asm_dir --polished_dir complete_pol_dir --amr_dir bac_amr_dir
    
<br>


### Usage Recommendations
<hr>

I recommend running BacGenomePipeline from your virtual environment.
To run BacGenomePipeline anywhere, make sure to run the following commands on your terminal:

    chmod +x BacGenomePipeline.py
    
Move executable to your selected bin directory
To find bin path on Linux, simply run:
 
     echo $PATH
     
Then copy script to bin path, for example:  
    
    cp BacGenomePipeline.py /home/stephen/.local/bin/BacGenomePipeline
    
 Now simply run the script as follows:
 
    BacGenomePipeline -f reads.fastq -n -d flye_amr_dir -p pol_dir -a bac_amr_dir
    
 
Alternatively, run BacGenomePipeline as shown below. Here, the fastq file **must** be
in the same working directory as the script calling it. 

<br>
 
### Running BacGenomePipeline Guide


 <img src=https://github.com/StephenFordham/BacGenomePipeline/blob/main/static/BacGenomePipeline.gif>
     
    
  hhfdfh  
    
    
    
     











    
    
       
       
       
       
       
       
       
       
       
       
       
       
   

