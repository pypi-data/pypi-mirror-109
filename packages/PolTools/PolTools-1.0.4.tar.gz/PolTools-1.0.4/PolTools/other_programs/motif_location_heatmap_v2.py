# Input: motifs from Juan, gene order sorted by TBP fold change
# Output: heatmap showing the location of the motif


import sys
import re
import os

from collections import defaultdict
from PolTools.utils.remove_files import remove_files
from PolTools.utils.make_random_filename import generate_random_filename
from PolTools.utils.heatmap_utils.generate_heatmap import generate_heatmap

args = sys.argv[1:]

if len(args) != 4:
    sys.stderr.write("Four arguments must be supplied: motif file, tbp_fold_change_file, output_filename (include .tiff), repeat amount\n")
    sys.exit(1)

juan_motif_file, tbp_fold_change_file, output_filename, repeat_amount = args


# Get all regions in the provided input file
regions = []
with open(juan_motif_file) as file:
    for line in file:
        #chrom, left, right, tsr_name, strand, motif, tbp_five_count_dependency, seq = line.split()
        regions.append(line.split())

# First get all the regions sorted by tsr fold change
regions.sort(key=lambda x:x[-2])

# Now need to sort by the motif distance by
regions.sort(key=lambda x: x[-1].split("_")[-1].find(x[-3]))





gamma = 2.2
repeat_amount = int(repeat_amount)

motifs_dict = defaultdict(
    lambda: {
        "Motif": [],
        "TSS_Locations": [],
    }
)

tss_to_gene_lookup_table = {}

tmp_juan_motif_file = generate_random_filename()

with open(juan_motif_file) as file:
    with open(tmp_juan_motif_file, 'w') as outfile:
        for line in file:
            chrom, left, right, tsr_name, strand, motif, tbp_five_count_dependency, seq = line.split()

            tss_left = int(left) + 5
            tss_right = int(right) - 5

            outfile.write(
                "\t".join([chrom, str(tss_left), str(tss_right), tsr_name, '0', strand]) + "\n"
            )

            motifs_dict[truQuant_gene_name]["Motif"].append(motif.upper())
            motifs_dict[truQuant_gene_name]["TSS_Locations"].append((tss_left, tss_right))
            motifs_dict[truQuant_gene_name]["Strand"] = strand

            tss_to_gene_lookup_table[tsr_name] = truQuant_gene_name


heatmap_width = -1
gene_order = []

with open(tbp_fold_change_file) as file:
    for line in file:
        chrom, left, right, name, score, strand = line.split()

        left, right = int(left), int(right)

        tss_loc_left = (left + right) / 2
        tss_loc_right = tss_loc_left + 1

        if strand == "-":
            tss_loc_left += 1
            tss_loc_right += 1

        motifs_dict[name]["truQuant_TSS_Location"] = (tss_loc_left, tss_loc_right)
        heatmap_width = right - left
        gene_order.append(name)


# Get the sequence from -36 to -19 for each of the regions
tmp_output_file = generate_random_filename(".sequences")
os.system(
    "PolTools sequence_from_region_around_max_tss -u " + tmp_juan_motif_file + " -36 -19 > " + tmp_output_file
)

heatmap_matrix = []
heatmap_data = {}

with open(tmp_output_file) as file:
    for line in file:
        curr_tsr, curr_seq = line.split("_")
        # Remove the > from the fasta file
        curr_tsr = curr_tsr[1:]
        curr_seq = curr_seq.rstrip().upper()

        curr_gene = tss_to_gene_lookup_table[curr_tsr]

        # Lets fix that now
        if "truQuant_TSS_Location" not in motifs_dict[curr_gene]:
            continue


        truQuant_location = motifs_dict[curr_gene]["truQuant_TSS_Location"]

        curr_row = [0] * heatmap_width

        # Find the location of the motif in the sequence
        for i, curr_motif in enumerate(motifs_dict[curr_gene]["Motif"]):
            regex_search_string = '(?=' + curr_motif + ')'

            regex_locations = [motif.start() for motif in re.finditer(regex_search_string, curr_seq)]

            # Convert the found motif locations to the relative position to the TSRs TSS
            motif_locations = [location - 36 for location in regex_locations]

            # Convert these to genomic positions
            genomic_motif_locations = []

            strand = motifs_dict[curr_gene]["Strand"]
            curr_tss_location = motifs_dict[curr_gene]["TSS_Locations"][i][0]

            for rel_location in motif_locations:
                if strand == "+":
                    curr_location = curr_tss_location + rel_location
                else:
                    curr_location = curr_tss_location - rel_location

                genomic_motif_locations.append((curr_location, curr_location + 1))

            # Convert the motif start locations to relative to truQuant locations
            relative_to_truQuant_locations = []
            for genomic_motif_location in genomic_motif_locations:
                motif_left, motif_right = genomic_motif_location
                tq_left, tq_right = truQuant_location

                if strand == "+":
                    relative_distance = motif_left - tq_left
                else:
                    relative_distance = tq_left - motif_left

                start_location = int(heatmap_width / 2) + relative_distance

                # Put ones in the locations
                for j in range(len(curr_motif)):
                    loc = int(start_location + j)
                    if loc < heatmap_width:
                        curr_row[loc] = 1

        if curr_gene not in heatmap_data:
            heatmap_data[curr_gene] = curr_row
        else:
            for j, val in enumerate(curr_row):
                heatmap_data[curr_gene][j] += val

# Convert the heatmap data to the heatmap matrix
for name in gene_order:
    if name in heatmap_data:
        heatmap_matrix.append(heatmap_data[name])
    else:
        heatmap_matrix.append([0] * heatmap_width)


remove_files(tmp_output_file, tmp_juan_motif_file)

# Write the heatmap matrix to a file
heatmap_matrix_file = generate_random_filename(".matrix")

with open(heatmap_matrix_file, 'w') as file:
    for line in heatmap_matrix:
        repeated_line = []
        for val in line:
            for _ in range(repeat_amount):
                repeated_line.append(val)

        file.write(
            "\t".join([str(val) for val in repeated_line]) + "\n"
        )

# Make the heatmap
generate_heatmap(heatmap_matrix_file, 'gray', output_filename, gamma=gamma, min_value=0, max_value=1)

remove_files(heatmap_matrix_file)
