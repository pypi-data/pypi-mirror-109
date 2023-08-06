import os
import sys
import glob
import argparse

from multiprocessing import Pool
from collections import defaultdict

from PolTools.utils.make_random_filename import generate_random_filename
from PolTools.utils.remove_files import remove_files

def trim_adapters(fastq_gz_files):
    # Run trim_galore
    os.system(
        "trim_galore --illumina --paired --dont_gzip --quality 0 --length 18 " + " ".join(fastq_gz_files)
    )


def combine_lanes(group):
    fastq_gz_files, output_prefix = group

    related_files = []
    for file in fastq_gz_files:
        related_files.extend(
            glob.glob(file.replace(".fastq.gz", "") + "*")
        )

    read_one_fastq_files = [file for file in related_files if '_val_1.fq' in file]
    read_two_fastq_files = [file for file in related_files if '_val_2.fq' in file]

    # Combine the different lanes
    combined_files = {
        'r1': generate_random_filename('.trimmed.fastq'),
        'r2': generate_random_filename('.trimmed.fastq'),
    }

    os.system(
        'cat ' + ' '.join(read_one_fastq_files) + ' > ' + combined_files['r1']
    )

    os.system(
        'cat ' + ' '.join(read_two_fastq_files) + ' > ' + combined_files['r2']
    )

    remove_files(read_one_fastq_files, read_two_fastq_files)

    return combined_files['r1'], combined_files['r2'], output_prefix


def align_data(combined_fastq_group, index, threads):
    # Align the data using hisat2
    read_one_combined_file, read_two_combined_file, output_prefix = combined_fastq_group

    sam_file = output_prefix + ".sam"

    os.system(
        "hisat2 -p " + str(threads) + " --np 0 -x " + index + " --rna-strandness RF -1 " + read_one_combined_file +
        " -2 " + read_two_combined_file + " -S " + sam_file
    )

    remove_files(read_one_combined_file, read_two_combined_file)

    return sam_file


def make_bam_file(sam_file, threads):
    # Make a bam file
    bam_file = sam_file.replace('.sam', '.bam')

    os.system(
        "samtools view -S -u -f 0x3 -@ " + str(threads) + " " + sam_file + " | samtools sort -@ " + str(threads) + " -O bam -o " + bam_file
    )

    return bam_file


def index_bam_file(bam_file, threads):
    os.system(
        "samtools index -@ " + str(threads) + " " + bam_file
    )


def make_bigwig_files(bam_file):
    fw_bigwig_file = bam_file.replace(".bam", "-FW.bw")
    rv_bigwig_file = bam_file.replace(".bam", "-RV.bw")

    os.system(
        "bamCoverage --bam " + bam_file + " -o " + fw_bigwig_file + " --binSize 1 --filterRNAstrand forward"
    )

    os.system(
        "bamCoverage --bam " + bam_file + " -o " + rv_bigwig_file + " --binSize 1 --filterRNAstrand reverse"
    )

def quantify(bam_files, annotation_file, threads):
    tmp_quantification_file = generate_random_filename('.quantification')

    # Do the quantification
    os.system(
        "/home/geoff/subread-2.0.1-source/bin/featureCounts -T " + str(threads) + " -p -a " + annotation_file +
        " -s 2 " + " ".join(bam_files) + " > " + tmp_quantification_file
    )


    # Convert the output to a matrix
    quantification_matrix = generate_random_filename('.matrix')
    os.system(
        "cut -f1,7- " + tmp_quantification_file + " | sed 1d > " + quantification_matrix
    )

    # Get the gene names from the annotation
    gene_names_file = generate_random_filename('.gene_names')
    os.system(
        "grep -w gene " + annotation_file + """ | cut -d '"' -f2,6 | tr '"' '\t' | sort -k 1b,1 > """ + gene_names_file
    )

    # Join the gene names to the gene ids to make the final matrix file
    conversion_dict = {}

    with open(gene_names_file) as file:
        for line in file:
            gene_id, gene_symbol = line.split()
            conversion_dict[gene_id] = gene_symbol

    with open(quantification_matrix) as file:
        with open("quantification.txt", 'w') as outfile:

            for i, line in enumerate(file):
                if i == 0:
                    file.write(line.rstrip() + "\n")
                else:
                    # Add the gene name to the end of the gene_id, separate by an underscore
                    gene_id = line.split()[0]
                    other_fields = "\t".join(line.split()[1:])

                    gene_symbol = conversion_dict[gene_id]

                    file.write(
                        gene_id + "_" + gene_symbol + "\t" + other_fields
                    )


# def quantify(bam_file, annotation_file):
#     # Quantify the file using HTSeq
#     quantification_file = generate_random_filename('quantification.tsv')
#
#     os.system(
#         "htseq-count --format bam --order name --type exon --idattr gene_name --nonunique all "
#         "--stranded reverse --quiet " + bam_file + " " + annotation_file + " > " + quantification_file
#     )
#
#     return quantification_file, bam_file


# def combine_quantification_files(quantification_files):
#     data = defaultdict(lambda: defaultdict(int))
#
#     bam_files = []
#
#     for filename, bam_file in quantification_files:
#         bam_files.append(bam_file)
#
#         with open(filename) as file:
#             for line in file:
#                 gene, counts = line.split("\t")
#
#                 if "__" not in line:
#                     data[gene][bam_file] = int(counts)
#
#         remove_files(filename)
#
#     # Output to a file called quantification.tsv
#     with open("quantification.tsv", 'w') as file:
#         # Write the headers before the data
#         file.write(
#             "\t".join(["Gene"] + bam_files) + "\n"
#         )
#
#         for gene in data:
#             current_data = [str(data[gene][bam_file]) for bam_file in bam_files]
#
#             file.write(
#                 "\t".join([gene] + current_data) + "\n"
#             )


def parse_args(args):
    def positive_int(num):
        try:
            val = int(num)
            if val <= 0:
                raise Exception("Go to the except")
        except:
            raise argparse.ArgumentTypeError(num + " must be positive")

        return val

    parser = argparse.ArgumentParser()

    parser.add_argument('--prefix', metavar=('prefix', 'output_prefix'), type=str, action='append', required=True, nargs=2,
                        help='Prefix to the files to align.')
    parser.add_argument('--index', metavar='index', type=str, help='hisat2 index file prefix', nargs='?', default='/media/genomes/hisat2/hg38/genome')
    parser.add_argument('--chrom_sizes_file', metavar='chrom_sizes_file', nargs='?', default='/media/genomes/hg38/hg38.chrom.sizes')
    parser.add_argument('--annotation_file', metavar='annotation_file', nargs='?', default='/media/genomes/hg38/gencode.v35.annotation.gff3')
    parser.add_argument('-t', '--threads', dest='threads', metavar='threads', type=positive_int, nargs='?', default=1)

    args = parser.parse_args(args)

    # Get all the files to align
    fastq_gz_groups = []

    for prefix, output_prefix in args.prefix:
        current_group = glob.glob(prefix + "*.fastq.gz")

        if len(current_group) == 0 or len(current_group) % 2 != 0:
            sys.stderr.write("You must provide an even number of fastq files for the prefix" + prefix + ". Exiting...\n")
            sys.exit(1)
        else:
            fastq_gz_groups.append((current_group, output_prefix))

    return fastq_gz_groups, args.index, args.chrom_sizes_file, args.annotation_file, args.threads


def main(args):
    fastq_gz_groups, index, chrom_sizes_file, annotation_file, threads = parse_args(args)

    with Pool(threads) as pool:
        fastq_file_groups = []

        for group in fastq_gz_groups:
            files, output_prefix = group

            fastq_file_groups.append(files)

        pool.map(trim_adapters, fastq_file_groups)

    combined_fastq_files = []
    for group in fastq_gz_groups:
        combined_fastq_files.append(
            combine_lanes(group)
        )

    sam_files = []
    for combined_fastq_group in combined_fastq_files:
        sam_files.append(
            align_data(combined_fastq_group, index, threads)
        )

    bam_files = []
    for sam_file in sam_files:
        bam_files.append(
            make_bam_file(sam_file, threads)
        )

    for bam_file in bam_files:
        index_bam_file(bam_file, threads)

    with Pool(int(threads / 2)) as pool:
        pool.starmap(make_bigwig_files, bam_files)

    with Pool(threads) as pool:
        args = [(bam_file, annotation_file) for bam_file in bam_files]
        quantification_files = pool.starmap(quantify, args)

    combine_quantification_files(quantification_files)


if __name__ == '__main__':
    main(sys.argv[1:])