# The goal is to make a table containing the following fields

# chrom, left, right, tsrPicker id, strand, total 5' end reads in TSR, maxTSS left, maxTSS right, 5' counts in maxTSS
# nearest truQuant gene name, distance to closest truQuant gene (not strand specific),
# quantification of maxTSS and TSR for each dataset, sequences around the TSR


# Input is the truQuant file, all dmso dataset, then all the quantifying datasets
import sys
import os

import pandas as pd
from pathlib import Path

from collections import defaultdict
from multiprocessing import Pool

from PolTools.utils.make_random_filename import generate_random_filename
from PolTools.utils.bedtools_utils.run_bedtools_subtract import run_subtract
from PolTools.utils.constants import rna_blacklist_file
from PolTools.utils.remove_files import remove_files


def blocklist_all_dmso_file(all_dmso_file):
    return run_subtract(all_dmso_file, rna_blacklist_file, strand_specific=False)


def get_tsrs(blocklisted_all_dmso_file):
    # First run tsrPicker with a min read count of 100 reads
    tsr_picker_output_file = blocklisted_all_dmso_file.rsplit(".")[0] + "_min_100-TSR.bed"

    tsr_picker_location = str(Path(__file__).parent.absolute()) + "/tsr_picker.py"

    os.system(
        'python3 ' + tsr_picker_location + ' ' + blocklisted_all_dmso_file + ' 100 '
    )

    # This file will have columns of chrom, left, right, name, score, and strand
    df = pd.read_csv(tsr_picker_output_file, sep='\t', header=None)
    df.rename(columns={
        0: 'Chromosome',
        1: 'Left',
        2: 'Right',
        3: 'Name',
        4: "maxTSS 5' end reads",
        5: 'Strand'
    }, inplace=True)

    df.insert(4, column='maxTSS Left', value=[val + 5 for val in df['Left']])
    df.insert(4, column='maxTSS Right', value=[val + 1 for val in df['maxTSS Left']])

    return df, tsr_picker_output_file


def add_five_reads_in_tsr(df, blocklisted_all_dmso_file, tsr_picker_output_file):
    # Get the number of 5' end reads in the TSR
    five_reads_in_tsr_file = generate_random_filename('.five_reads')

    os.system(
        'PolTools multicoverage five ' + tsr_picker_output_file + ' ' + blocklisted_all_dmso_file + ' > ' + five_reads_in_tsr_file
    )

    five_reads_df = pd.read_csv(five_reads_in_tsr_file, sep='\t')
    five_reads_df.rename(columns={blocklisted_all_dmso_file: "5' reads in maxTSS"}, inplace=True)

    remove_files(five_reads_in_tsr_file)

    return df.merge(five_reads_df, on=['Chromosome', 'Left', 'Right', 'Name', 'Strand'])


def load_truQuant_data(truQuant_file):
    # Will load a dictionary containing the chrom, strand, and a tuple of the location with the gene name
    tq_max_tss_file = generate_random_filename('.truQuant_maxTSS')

    os.system(
        'PolTools make_regions_file_centered_on_max_tss ' + truQuant_file + ' 1 > ' + tq_max_tss_file
    )

    data_dict = defaultdict(lambda: {
        '+': [],
        '-': []
    })

    with open(tq_max_tss_file) as file:
        for line in file:
            chrom, left, right, name, score, strand = line.split()

            data_dict[chrom][strand].append(
                (int(left), name)
            )

    remove_files(tq_max_tss_file)

    return data_dict


def get_closest_truQuant_gene(tq_data, max_tss_left, chrom):
    # If there are no genes on the same chromosome, the distance is -1
    if not (tq_data[chrom]["-"] or tq_data[chrom]["+"]):
        return [-1, 'No gene on chromosome', "?"]

    # Assume that the first gene in the positive dictionary is the closest
    if tq_data[chrom]["+"]:
        distance = abs(max_tss_left - tq_data[chrom]["+"][0][0])

        closest_gene = [distance, tq_data[chrom]["+"][0][1], "+"]
    else:
        # There was + instead of -'s here
        distance = abs(max_tss_left - tq_data[chrom]["+"][0][0])

        closest_gene = [distance, tq_data[chrom]["-"][0][1], "-"]

    # Go through all the positive genes first
    for tq_location, tq_gene in tq_data[chrom]["+"]:
        # If the gene is closer, then update the closest gene
        curr_distance = abs(max_tss_left - tq_location)

        if curr_distance < closest_gene[0]:
            closest_gene = [curr_distance, tq_gene, "+"]

    # Then the negative strand genes
    for tq_location, tq_gene in tq_data[chrom]["-"]:
        # If the gene is closer, then update the closest gene
        curr_distance = abs(max_tss_left - tq_location)

        if curr_distance < closest_gene[0]:
            closest_gene = [curr_distance, tq_gene, "-"]

    return closest_gene


def add_column_for_nearest_truQuant_gene(df, truQuant_file):
    tq_data = load_truQuant_data(truQuant_file)

    closest_genes_dict = {
        'Distance to Closest truQuant Gene': [],
        'Closest truQuant Gene': [],
        'truQuant Gene Strand': []
    }

    for i, row in df.iterrows():
        distance, gene_name, gene_strand = get_closest_truQuant_gene(tq_data, row['maxTSS Left'], row['Chromosome'])

        closest_genes_dict['Distance to Closest truQuant Gene'].append(distance)
        closest_genes_dict['Closest truQuant Gene'].append(gene_name)
        closest_genes_dict['truQuant Gene Strand'].append(gene_strand)

    closest_gene_df = pd.DataFrame.from_dict(closest_genes_dict)

    # Combine the dfs
    df = df.merge(closest_gene_df, left_index=True, right_index=True)

    return df


def get_closest_blocklisted(data, max_tss_left, chrom, strand):
    # If there are no genes on the same chromosome, the distance is -1
    if not data[chrom][strand]:
        return [-1, 'No gene on chromosome', "?"]


    # Assume that the first region is the closest
    closest = data[chrom][strand][0]
    min_distance = abs(data[chrom][strand][0][0] - max_tss_left)

    for location, name in data[chrom][strand]:
        curr_distance = abs(max_tss_left - location)

        if curr_distance < min_distance:
            min_distance = curr_distance
            closest = (min_distance, name)

    return closest


def add_column_for_nearest_blocklisted_region(df):
    # Load the blocklist file
    blocklist_data = defaultdict(lambda: {
        '+': [],
        '-': []
    })

    with open(rna_blacklist_file) as file:
        for line in file:
            chrom, left, right, name, score, strand = line.rstrip().split("\t")

            blocklist_data[chrom][strand].append(
                (int(left), name)
            )

    closest_blocklisted_dict = {
        'Distance to Closest Blocklisted Region': [],
        'Closest Blocklisted Region': [],
    }

    for i, row in df.iterrows():
        distance, name = get_closest_blocklisted(blocklist_data, row['maxTSS Left'], row['Chromosome'], row['Strand'])

        closest_blocklisted_dict['Distance to Closest Blocklisted Region'].append(distance)
        closest_blocklisted_dict['Closest Blocklisted Region'].append(name)

    next_df = pd.DataFrame.from_dict(closest_blocklisted_dict)

    df = df.merge(next_df, left_index=True, right_index=True)

    return df


# Functions from https://stackoverflow.com/questions/45718523/pass-kwargs-to-starmap-while-using-pool-in-python
from itertools import repeat

def starmap_with_kwargs(pool, fn, args_iter, kwargs_iter):
    args_for_starmap = zip(repeat(fn), args_iter, kwargs_iter)
    return pool.starmap(apply_args_and_kwargs, args_for_starmap)


def apply_args_and_kwargs(fn, args, kwargs):
    return fn(*args, **kwargs)


def quantify_datasets(df, quantifying_datasets, tsr_picker_output_file, threads):
    # First blocklist all the datasets
    pool = Pool(threads)

    args = [(dataset, rna_blacklist_file) for dataset in quantifying_datasets]
    kwargs = [(dict(output_filename=dataset.replace('.bed', 'blocklisted.bed'), strand_specific=False))
              for dataset in quantifying_datasets]

    starmap_with_kwargs(pool, run_subtract, args, kwargs)

    # Quantify the TSRs
    datasets = [file.replace('.bed', 'blocklisted.bed') for file in quantifying_datasets]

    tsr_quantification_file = generate_random_filename('.tsr_quant')
    os.system(
        'PolTools multicoverage -t ' + str(threads) + ' five ' + ' '.join([tsr_picker_output_file] + datasets) + ' > ' + tsr_quantification_file
    )

    quant_df = pd.read_csv(tsr_quantification_file, sep='\t')

    # Rename the columns to include TSR quantification
    quant_df.columns = [str(col) + " TSR 5' Counts" if '.bed' in col else str(col) for col in quant_df.columns]

    df = df.merge(quant_df, on=['Chromosome', 'Left', 'Right', 'Name', 'Strand'])

    remove_files(tsr_quantification_file)

    # Now quantify just the maxTSSs
    tsr_picker_max_tss_file = generate_random_filename('.tsrPicker_maxTSS')

    with open(tsr_picker_output_file) as file:
        with open(tsr_picker_max_tss_file, 'w') as outfile:
            for line in file:
                chrom, left, right, name, score, strand = line.split()

                outfile.write(
                    "\t".join(
                        [chrom, str(int(left) + 5), str(int(left) + 6), name, score, strand]
                    ) + '\n'
                )

    tsr_quantification_file = generate_random_filename('.tsr_quant')
    os.system(
        'PolTools multicoverage -t ' + str(threads) + ' five ' + ' '.join([tsr_picker_max_tss_file] + datasets) + ' > ' + tsr_quantification_file
    )

    quant_df = pd.read_csv(tsr_quantification_file, sep='\t')

    # Drop the chrom, left, right, and strand columns
    quant_df = quant_df.drop(["Chromosome", "Left", "Right"], axis=1)

    quant_df.columns = [str(col) + " maxTSS 5' Counts" if '.bed' in col else str(col) for col in quant_df.columns]

    df = df.merge(quant_df, on=['Name', 'Strand'])

    remove_files(tsr_quantification_file, datasets)

    return df, tsr_picker_max_tss_file


def get_sequences(max_tss_file, left, right):
    sequences_file = generate_random_filename('.sequences')

    os.system(
        'PolTools sequence_from_region_around_max_tss -u ' +
        ' '.join([max_tss_file, left, right]) + ' > ' + sequences_file
    )

    with open(sequences_file) as file:
        lines = [line.rstrip() for line in file.readlines()]

    remove_files(sequences_file)

    return lines


def add_sequences(df, tsr_picker_max_tss_file):
    seq_locations = [
        ['+25', '+50'],
        ['+5', '+35'],
        ['-100', '+100'],
        ['-5', '+5'],
        ['-25', '-1'],
        ['-36', '-19'],
    ]

    for left, right in seq_locations:
        column_name = left + ' to ' + right
        df[column_name] = get_sequences(tsr_picker_max_tss_file, left, right)

    return df


def main(args):
    tQ_file, all_dmso_file, threads = args[:3]
    quantifying_datasets = args[3:]

    threads = int(threads)

    blocklisted_all_dmso = blocklist_all_dmso_file(all_dmso_file)

    df, tsr_picker_output_file = get_tsrs(blocklisted_all_dmso)

    df = add_five_reads_in_tsr(df, blocklisted_all_dmso, tsr_picker_output_file)

    df = add_column_for_nearest_truQuant_gene(df, tQ_file)

    df = add_column_for_nearest_blocklisted_region(df)

    df, tsr_picker_max_tss_file = quantify_datasets(df, quantifying_datasets, tsr_picker_output_file, threads)

    df = add_sequences(df, tsr_picker_max_tss_file)

    remove_files(tsr_picker_output_file, blocklisted_all_dmso, tsr_picker_max_tss_file)

    # Write the table to a file
    df.to_csv('big_ass_table.csv', index=None)


if __name__ == '__main__':
    main(sys.argv[1:])
