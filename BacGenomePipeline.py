#!/usr/bin/env python

import subprocess
import os
import sys
import time
import argparse
import re
import shutil


# terminal output retro, slow function
def typewrite(message):
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()

        if char != '\n':
            time.sleep(0.05)
        else:
            time.sleep(0.5)

def _usage():
    return ("BacGenomePipeline (--pipeline | --pipe_red_mem | --assembly | --annotation)\n"
            "--fastq_file READS\n"
            "\t     --help --version\n"
            "\t     [--nanostats] [--medaka_polish]\n"
            "\t     [--mean_q_weight] [--asm_fasta]\n"
            "\t     [--genome_size SIZE]  [--asm_coverage INT]\n"
            "\t     [--flye_dir DIR_NAME] [--polished_dir DIR_NAME]\n"
            "\t     [--amr_dir DIR_NAME]  [--vir_dir DIR_NAME]\n")



def _epilog():
    return ("\nDid you know? BacGenomePipeline can be run in modes\n\n"
            "These modes include: pipeline, which runs the entire BacGenomePipeline workflow,\n"
            "pipe_red_mem, which uses less memory by using use a subset of the longest reads \n"
            "for initial disjointig by specifying --asm-coverage and --genome-size options. \n"
            "The assembly mode runs assembly and polishing steps only. For this step, \n"
            "annotation is excluded. Finally the annotation mode takes a genome assembly and \n"
            "annotates it for antimicrobial and virulence genes \n"
            "\nExample Usage:\n"
            "BacGenomePipeline --pipeline -f reads.fastq\n"
            "BacGenomePipeline --pipeline -f reads.fastq.gz -m -n\n"
            "BacGenomePipeline --pipe_red_mem -f reads.fastq -g 5.7m -c 40 -n -m\n"
            "BacGenomePipeline --annotation -s assembly.fasta\n"
            "BacGenomePipeline --assembly -f reads.fastq -n -m\n")


def fastq_file_validation(input_file):
    m = re.search('(.fastq$|fastq.gz$)', input_file)
    if not m:
        raise argparse.ArgumentTypeError('A valid fastq file must be submitted')
    return input_file


def fasta_file_validation(input_file):
    m = re.search('(.fasta$)', input_file)
    if not m:
        raise argparse.ArgumentTypeError('A valid fasta file must be submitted')
    return input_file




def get_args():


    parser = argparse.ArgumentParser(description='Complete Bacterial Genome Assembly and Annotation Pipeline',
                                     epilog=_epilog(),
                                    formatter_class=argparse.RawDescriptionHelpFormatter,
                                     usage=_usage())

    version = parser.add_argument_group(title='Version')
    version.add_argument('--version', action="version",
                        help='Print version and exit.',
                        version='BacGenomePipeline {}'.format('1.0.0'))


    pipeline_mode = parser.add_mutually_exclusive_group(required=True)
    pipeline_mode.add_argument('--pipeline',
                               help='Runs the entire Pipeline',
                               default=None,
                               action='store_true',
                               )
    pipeline_mode.add_argument('--pipe_red_mem',
                               help='Runs the entire Pipeline with reduced memory consumption',
                               default=None,
                               action='store_true',
                               )
    pipeline_mode.add_argument('--assembly',
                               help='Runs the assembly portion of the pipeline',
                               default=None,
                               action='store_true',
                               )
    pipeline_mode.add_argument('--annotation',
                               help='Runs the annotation portion of the pipeline',
                               default=None,
                               action='store_true',
                               )



    read_input = parser.add_argument_group(title='Input fastq Reads (a fastq file is required)')
    read_input.add_argument('-f', '--fastq_file',
                            help='Specify an input Fastq file for the Pipeline and assembly modes',
                            type=fastq_file_validation,
                            default=None,
                            metavar='')

    pipeline_options = parser.add_argument_group(title='Pipeline Options')

    pipeline_options.add_argument('-n', '--nanostats',
                                  help='Optionally run NanoStats on your filtered read set',
                                  action='store_true')
    pipeline_options.add_argument('-m', '--medaka_polish',
                                  help='Optionally run NanoStats on your filtered read set',
                                  action='store_true')
    pipeline_options.add_argument('-s', '--asm_fasta',
                                  help='Add Genome assembly in fasta format',
                                  default=None,
                                  type=fasta_file_validation)
    pipeline_options.add_argument('-w', '--q_weight',
                                  help='Add mean_q_weight for read filtering',
                                  default=7,
                                  type=int)



    flye_asm_options = parser.add_argument_group(title='Optional flye assembly arguments\n'
                                                       '(To reduce memory consumption for large genome assemblies)')
    flye_asm_options.add_argument('-g', '--genome_size',
                                  help='Estimated genome size (for example, 5m or 2.6g)',
                                  required=False,
                                  default=None,
                                  metavar='')
    flye_asm_options.add_argument('-c', '--asm_coverage',
                                  default=None,
                                  help="reduced coverage for initial "
                                  "disjointig assembly [not set]",
                                  type=int,
                                  metavar='')


    directory_names = parser.add_argument_group(title='Directory names')
    directory_names.add_argument('-d', '--flye_dir',
                                 help='Specify a flye genome assembly directory name',
                                 default='flye_dir',
                                 metavar='')
    directory_names.add_argument('-p', '--polished_dir',
                                 help='Specify a medaka polished genome directory name',
                                 default='pol_dir',
                                 metavar='')
    directory_names.add_argument('-a', '--amr_dir',
                                 help='Specify a antimicrobial resistance directory name',
                                 default='amr_dir',
                                 metavar='')
    directory_names.add_argument('-v', '--vir_dir',
                                 help='Specify a virulence gene directory name',
                                 default='virulence_dir',
                                 metavar='')

    args = parser.parse_args()

    if args.pipe_red_mem:
        if (args.asm_coverage is None) or (args.genome_size is None):
            parser.error("Assembly Pipeline mode: Pipe_red_mem, requires arguements supplied "
                         "for asm_coverage and genome_size")

    if args.pipeline and (args.fastq_file is None):
        parser.error("Assembly Pipeline mode: Pipeline, requires a fastq file as input")

    if args.pipe_red_mem and (args.fastq_file is None):
        parser.error("Assembly Pipeline mode: pipe_red_mem, requires a fastq file as input")

    if args.assembly and (args.fastq_file is None):
        parser.error("Assembly Pipeline mode: Assembly, requires a fastq file as input")

    if args.annotation and (args.asm_fasta is None):
        parser.error("Assembly Pipeline mode: Annotation, requires a fasta file as input")

    return args


    ####linking logic

def main():
    args = get_args()

    if args.annotation == None:
        filtered_reads = args.fastq_file.split('.')[0] + '_filtered.fastq'
        raw_assembly = args.fastq_file.split('.')[0] + '_assembly.fasta'
        consensus_asm = str(args.fastq_file.split('.')[0] + '_consensus.fasta')
        weight = str(args.q_weight)

    def filtlong_filtering(raw_read_set):
        typewrite('Stage 1: Filtering Reads\n\n')
        filtlong_cmds = 'filtlong --min_length 1000  --mean_q_weight ' + weight + \
                        ' --target_bases 500000000 ' + raw_read_set + ' > ' + filtered_reads
        os.system(filtlong_cmds)


    def nanostats_report(reads):
        typewrite('Stage 1a: Producing a Nanostats report of the filtered reads\n\n')
        nanostats_cmd = ['NanoStat', '-o', 'NanoStats_Report', '-n', 'nano_report.txt', '--fastq', reads]
        FNULL = open(os.devnull, 'w')
        subprocess.call(nanostats_cmd, stdout=FNULL, stderr=subprocess.STDOUT)


    def flye_genome_assembly(reads):
        typewrite('Stage 2: Genome Assembly: \nThis step may take up to 30 minutes, go for a coffee\n\n')
        flye_genome_assembly_cmds = ['flye', '-o', str(args.flye_dir), '--plasmids',
                                     '--meta', '--threads', '16', '--nano-raw', reads]
        FNULL = open(os.devnull, 'w')
        subprocess.call(flye_genome_assembly_cmds, stdout=FNULL, stderr=subprocess.STDOUT)
        shutil.move(str(args.flye_dir) + '/assembly.fasta', '.')
        os.rename('assembly.fasta', raw_assembly)


    def flye_genasm_reduced_ram(reads):
        """flye assembly method adjusted for reduced memory consumption"""

        typewrite('Stage 2: Genome Assembly: \nThis step may take up to 30 minutes, go for a coffee\n\n')
        typewrite('Reduced memory genome assembly\nlongest reads used for initial disjointig\n\n')
        flye_genome_assembly_cmds = ['flye', '-o', str(args.flye_dir), '--plasmids',
                                     '--threads', '10','--genome-size', str(args.genome_size), '--asm-coverage',
                                     str(args.asm_coverage), '--nano-raw', reads]
        FNULL = open(os.devnull, 'w')
        subprocess.call(flye_genome_assembly_cmds, stdout=FNULL, stderr=subprocess.STDOUT)
        shutil.move(str(args.flye_dir) + '/assembly.fasta', '.')
        os.rename('assembly.fasta', raw_assembly)


    def medaka_post_asm_pol(assembly):
        typewrite('Stage 3: Post Assembly Polishing\n\n')
        medaka_polishing = ['medaka_consensus', '-i', str(filtered_reads), '-d', assembly,
                            '-o', str(args.polished_dir), '-t', '10', '-m', 'r941_min_high_g303']
        FNULL = open(os.devnull, 'w')
        subprocess.call(medaka_polishing, stdout=FNULL, stderr=subprocess.STDOUT)
        shutil.move(str(args.polished_dir) + '/consensus.fasta', '.')
        os.rename('consensus.fasta', consensus_asm)


    def antimicrobial_resistance_gene_detection(consensus_asm):
        typewrite('Stage 4a: Antimicrobial Resistance Gene detection\n\n')
        amr_input = ['staramr', 'search', '-o', str(args.amr_dir), consensus_asm]
        FNULL = open(os.devnull, 'w')
        subprocess.call(amr_input, stdout=FNULL, stderr=subprocess.STDOUT)


    def virulence_gene_detection(consensus_asm):
        typewrite('Stage 4b: Virulence Gene detection\n\n')
        os.mkdir(str(args.vir_dir))
        vir_cmds = 'abricate --quiet -db vfdb ' + str(consensus_asm) + ' > virulence_metadata.csv'
        os.system(vir_cmds)
        shutil.move('virulence_metadata.csv', str(args.vir_dir))

    if args.annotation == None:
        typewrite('Complete Bacterial Genome pipeline Initialized...\n\n')

    # Pipeline workflow logic

    def pipeline():
        filtlong_filtering(raw_read_set=args.fastq_file)
        if args.nanostats:
            nanostats_report(reads=filtered_reads)
        flye_genome_assembly(reads=filtered_reads)

        if args.medaka_polish:

            medaka_post_asm_pol(assembly=raw_assembly)
            antimicrobial_resistance_gene_detection(consensus_asm=consensus_asm)
            virulence_gene_detection(consensus_asm=consensus_asm)

        else:

            antimicrobial_resistance_gene_detection(consensus_asm=raw_assembly)
            virulence_gene_detection(consensus_asm=raw_assembly)

        typewrite('\u001b[32mSuccess \u2713\n')


    def pipeline_reduced_mem_consumption():
        filtlong_filtering(raw_read_set=args.fastq_file)
        if args.nanostats:
            nanostats_report(reads=filtered_reads)
        flye_genasm_reduced_ram(reads=filtered_reads)

        if args.medaka_polish:

            medaka_post_asm_pol(assembly=raw_assembly)
            antimicrobial_resistance_gene_detection(consensus_asm=consensus_asm)
            virulence_gene_detection(consensus_asm=consensus_asm)

        else:

            antimicrobial_resistance_gene_detection(consensus_asm=raw_assembly)
            virulence_gene_detection(consensus_asm=raw_assembly)

        typewrite('\u001b[32mSuccess \u2713\n')


    def assembly():
        typewrite('Genome Assembly only portion of pipeline initiated...')
        filtlong_filtering(raw_read_set=args.fastq_file)
        if args.nanostats:
            nanostats_report(reads=filtered_reads)
        flye_genome_assembly(reads=filtered_reads)
        if args.medaka_polish:

            medaka_post_asm_pol(assembly=raw_assembly)


    def annotation():
        typewrite('Annotation only portion of pipeline initiated...\n\n')

        antimicrobial_resistance_gene_detection(consensus_asm=args.asm_fasta)
        virulence_gene_detection(consensus_asm=args.asm_fasta)
        typewrite('\u001b[32mSuccess \u2713\n')


    if args.pipeline:
        pipeline()

    if args.pipe_red_mem:
        pipeline_reduced_mem_consumption()

    if args.assembly:
        assembly()

    if args.annotation:
        annotation()

if __name__ == '__main__':
    main()


