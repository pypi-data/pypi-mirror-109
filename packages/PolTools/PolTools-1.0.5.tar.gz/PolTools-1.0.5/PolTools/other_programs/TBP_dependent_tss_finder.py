import sys
import os
import multiprocessing
import pandas as pd

from collections import defaultdict

from PolTools.utils.make_random_filename import generate_random_filename
from PolTools.utils.remove_files import remove_files


def genomecov(strand, output_file, input_bed, chrom_sizes_file):
    os.system(
        "bedtools genomecov -i " + input_bed + " -g " + chrom_sizes_file + " -bg -strand " + strand + " -5 > " + output_file
    )

def get_genome_positions_file(all_dmso_data, chrom_sizes_file, min_counts):
    sorted_bed_file = generate_random_filename()

    os.system(
        "bedSort " + all_dmso_data + " " + sorted_bed_file
    )

    # Make the bedgraphs from the file
    fw_bedgraph = generate_random_filename("-FW.bedgraph")
    rv_bedgraph = generate_random_filename("-RV.bedgraph")

    args = [
        ("+", fw_bedgraph, sorted_bed_file, chrom_sizes_file),
        ("-", rv_bedgraph, sorted_bed_file, chrom_sizes_file)
    ]

    with multiprocessing.Pool() as pool:
        pool.starmap(genomecov, args)

    # Remove all the positions in the genome that are below the threshold value
    genome_positions_file = generate_random_filename(".bed")

    with open(genome_positions_file, 'w') as output_file:
        with open(fw_bedgraph) as file:
            for line in file:
                chrom, left, right, height = line.split()

                left, right, height = (int(left), int(right), int(height))

                if height > min_counts:
                    for position in range(left, right):
                        output_file.write(
                            '\t'.join(
                                [chrom, str(position), str(position + 1), "TSS", "0", "+"]
                            )  + "\n"
                        )

        with open(rv_bedgraph) as file:
            for line in file:
                chrom, left, right, height = line.split()

                left, right, height = (int(left), int(right), int(height))

                if height > min_counts:
                    for position in range(left, right):
                        output_file.write(
                            '\t'.join(
                                [chrom, str(position), str(position + 1), "TSS", "0", "-"]
                            )  + "\n"
                        )

    remove_files(sorted_bed_file, fw_bedgraph, rv_bedgraph)

    return genome_positions_file


def get_available_tss(tbp_dmso_rep_1, tbp_dmso_rep_2, tbp_vhl_rep1, tbp_vhl_rep2, genome_positions_file, tbp_subtraction_dependency_threshold):
    # Make a dictionary containing the 5' 4ounts for each of the files
    # Lets run PolTools multicoverage

    multicoverage_output_file = generate_random_filename(".txt")
    filenames = [tbp_dmso_rep_1, tbp_dmso_rep_2, tbp_vhl_rep1, tbp_vhl_rep2]

    print("PolTools multicoverage five " + " ".join([genome_positions_file] + filenames) + " > " + multicoverage_output_file)

    os.system(
        "PolTools multicoverage five " + " ".join([genome_positions_file] + filenames) + " > " + multicoverage_output_file
    )

    print("Past here")

    # Now read in the file to a pandas df
    df = pd.read_csv(multicoverage_output_file, sep='\t')

    # Make a column for the tbp dmso - tbp vhl
    dmso_cols = [col for col in df.columns if 'DMSO' in col]
    vhl_cols = [col for col in df.columns if 'VHL' in col]

    df['diff'] = df[dmso_cols].sum(axis=1) - df[vhl_cols].sum(axis=1)

    # Remove any TSSs that do not have at least tbp_subtraction_dependency_threshold reads
    df = df[df['diff'] >= tbp_subtraction_dependency_threshold]

    # Get the possible TSSs into a list
    possible_tss = defaultdict(
        lambda :
            {
                "+": [],
                "-": []
            }
    )

    print("Made df")

    for _, row in df.iterrows():
        chrom = row['Chromosome']
        left = int(row['Left'])
        right = int(row['Right'])
        strand = row['Strand']
        height = int(row['diff'])

        possible_tss[chrom][strand].append([chrom, left, right, "name", height, strand])

    print("Made dict")

    # For each chromsome and strand, sort the list by height
    for chrom in possible_tss:
        for strand in possible_tss[chrom]:
            possible_tss[chrom][strand].sort(key=lambda x: x[-2])

    return possible_tss


def find_tsrs(tss_heights):
    # Do the algorithm
    tsrs = []

    while tss_heights:
        # Choose the first one since it is the max
        curr_max_tss = tss_heights[0]
        chrom, left, right, name, height, strand = curr_max_tss

        new_tsr = [chrom, left - 5, right + 5, "TSS", height, strand]
        new_tsr_chrom, new_tsr_left, new_tsr_right, new_tsr_name, height , new_tsr_strand = new_tsr
        tsrs.append(new_tsr)

        # Eliminate overlapping TSSs
        non_overlapping_tss = []
        for tss in tss_heights:
            tss_chrom, tss_left, tss_right, tss_name, tss_score, tss_strand = tss

            if tss_left < new_tsr_left or tss_left >= new_tsr_right:
                # If there is no overlap between the newly defined TSR and this TSS, add it to the non overlapping
                non_overlapping_tss.append(tss)

        tss_heights = non_overlapping_tss

    return tsrs


def find_tsrs_per_chrom(possible_tss_dict):
    # Go through each chromosome and pick the largest. Go +- 5bp to make a region size of 11.
    # Remove any TSSs within that that region and then pick the next max
    identified_tsrs = []

    for chrom in possible_tss_dict:
        for strand in possible_tss_dict[chrom]:
            identified_tsrs.extend(
                find_tsrs(possible_tss_dict[chrom][strand])
            )

    return identified_tsrs


def main(args):
    all_dmso_data, tbp_dmso_rep_1, tbp_dmso_rep_2, tbp_vhl_rep1, tbp_vhl_rep2, tss_strength_threshold, \
    tbp_subtraction_dependency_threshold, chrom_sizes_file = args

    # Convert the thresholds to integers
    tss_strength_threshold = int(tss_strength_threshold)
    tbp_subtraction_dependency_threshold = int(tbp_subtraction_dependency_threshold)

    # Get all positions in the genome with at least tss_strength_threshold_counts in the all_dmso_data
    genome_positions_file = get_genome_positions_file(all_dmso_data, chrom_sizes_file, tss_strength_threshold)

    # Get the counts for each of those positions in each of the tbp datasets
    possible_tss_dict = get_available_tss(tbp_dmso_rep_1, tbp_dmso_rep_2, tbp_vhl_rep1, tbp_vhl_rep2, genome_positions_file, tbp_subtraction_dependency_threshold)

    # Go through each chromosome and find tsrs
    found_tsrs = find_tsrs_per_chrom(possible_tss_dict)

    # Write the TSRs to a file
    output_filename = "TBP_TSRs_TSS_Strength_min_" + str(tss_strength_threshold) + "_TBP_sub_dependency_" + \
                      str(tbp_subtraction_dependency_threshold) + ".bed"

    with open(output_filename, 'w') as file:
        for tsr in found_tsrs:
            file.write(
                "\t".join(
                    [str(val) for val in tsr]
                ) + "\n"
            )

if __name__ == '__main__':
    main(sys.argv[1:])