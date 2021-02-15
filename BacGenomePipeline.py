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
            


def fastq_file_validation(input_file):
    m = re.search('(.fastq$|fastq.gz$)', input_file)
    if not m:
        raise argparse.ArgumentTypeError('A valid fastq file must be submitted')
    return input_file


def get_args():

    parser = argparse.ArgumentParser(description='Complete Bacterial Genome Assembly and Annotation Pipeline')
                                     
    parser.add_argument('-f', '--fastq_file', help='Specify an input Fastq file for the Pipeline',
                        type=fastq_file_validation, required=True, metavar='')
    parser.add_argument('-n', '--nanostats', help='Optionally run a NanoStats report on your filtered read set',
                        action='store_true')
    parser.add_argument('-d', '--flye_dir', help='Specify a Flye Genome assembly directory name',
                        required=True, metavar='')
    parser.add_argument('-p', '--polished_dir', help='Specify a Medaka Polished genome directory name',
                        required=True, metavar='')
    parser.add_argument('-a', '--amr_dir', help='Specify a Antimicrobial resistance directory name',
                        required=True, metavar='')
    args = parser.parse_args()

    return args


    ####linking logic

def main():
    args = get_args()

    filtered_reads = args.fastq_file.split('.')[0] + '_filtered.fastq'
    raw_assembly = args.fastq_file.split('.')[0] + '_assembly.fasta'
    consensus_asm = str(args.fastq_file.split('.')[0] + '_consensus.fasta')


    def filtlong_filtering(raw_read_set):
        typewrite('Stage 1: Filtering Reads\n\n')
        filtlong_cmds = 'filtlong --min_length 1000 --keep_percent 90 --mean_q_weight 5 ' \
                        '--target_bases 500000000 ' + raw_read_set + ' > ' + filtered_reads
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


    def medaka_post_asm_pol(assembly):
        typewrite('Stage 3: Post Assembly Polishing\n\n')
        medaka_polishing = ['medaka_consensus', '-i', str(filtered_reads), '-d', assembly,
                            '-o', str(args.polished_dir), '-t', '10', '-m', 'r941_min_high_g303']
        FNULL = open(os.devnull, 'w')
        subprocess.call(medaka_polishing, stdout=FNULL, stderr=subprocess.STDOUT)
        shutil.move(str(args.polished_dir) + '/consensus.fasta', '.')
        os.rename('consensus.fasta', consensus_asm)


    def antimicrobial_resistance_gene_detection(consensus_asm):
        typewrite('Stage 4: Antimicrobial Resistance Gene detection\n\n')
        amr_input = ['staramr', 'search', '-o', str(args.amr_dir), consensus_asm]
        FNULL = open(os.devnull, 'w')
        subprocess.call(amr_input, stdout=FNULL, stderr=subprocess.STDOUT)


    typewrite('Complete Bacterial Genome pipeline Initialized...\n\n')

    # Pipeline workflow

    filtlong_filtering(raw_read_set=args.fastq_file)
    if args.nanostats:
        nanostats_report(reads=filtered_reads)
    flye_genome_assembly(reads=filtered_reads)
    medaka_post_asm_pol(assembly=raw_assembly)
    antimicrobial_resistance_gene_detection(consensus_asm=consensus_asm)

    print('\n')

    typewrite('\u001b[32mSuccess!\n')


if __name__ == '__main__':
    main()
