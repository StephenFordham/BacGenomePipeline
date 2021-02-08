# BacGenomePipeline

## Complete Bacterial Genome Assembly and Annotation Pipeline

### General Description

<img src=https://github.com/StephenFordham/BacGenomePipeline/blob/main/static/nanopore_squiggle.png width=700 >


Complete bacterial genome assembly pipeline. Assembled and annotated bacterial genomes can be <br>
created with only raw reads as input! BacGenomePipeline can accept either fastq or gzipped fastq files. <br>
Relax and grab a coffee while BacGenomePipeline does the genomic heavy lifting.<br>

 This pipeline filters raw reads to produce the best 500mb reads. <br>
 The filtering process also places weight on read quality, to ensure small high quality reads are not discarded.<br>
 This is considered vital to aid the recovery of small plasmids present within bacterial strains.<br>
 
Optionally, the user can run Nanostat to assess read quality metrics. The best reads are then assembled <br>
using the flye genome assembler with settings adjusted to help recovery of plasmids with an imbalanced <br>
distribution. The assembly is then polished with one round of medaka-consensus polishing. The polished <br>
assembly is annotated using staramr whichscans scans bacterial genome contigs against the ResFinder, <br>
PointFinder, and PlasmidFinder databases (used by the ResFinder webservice and other webservices offered <br>
by the Center for Genomic Epidemiology) and compilesa summary report of detected antimicrobial resistance genes. <br>
