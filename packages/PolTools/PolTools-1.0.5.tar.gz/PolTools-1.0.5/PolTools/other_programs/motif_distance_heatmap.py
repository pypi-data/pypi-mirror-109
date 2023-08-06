# Input: motifs from Juan, gene order sorted by TBP fold change
# Output: heatmap showing the location of the motif


import sys
import random

from PolTools.utils.make_random_filename import generate_random_filename

args = sys.argv[1:]

juan_motif_file, output_filename = args
width = 50

# Get all regions in the provided input file
regions = []
with open(juan_motif_file) as file:
    for line in file:
        regions.append(line.split())

# First get all the regions sorted by tsr fold change
#regions.sort(key=lambda x: float(x[-2]), reverse=True)

# Randomize the sort first
random.shuffle(regions)


# Now need to sort by the motif distance
regions.sort(key=lambda x: x[-1].split("_")[-1].find(x[-3]))


# Expand the regions and write them to a file
with open(output_filename, 'w') as file:
    for region in regions:
        chrom, left, right, tsr_name, strand, motif, tbp_five_count_dependency, seq = region

        max_tss_left = int(left) + 5
        max_tss_right = int(right) - 5

        left = str(max_tss_left - width)
        right = str(max_tss_right + width - 1)

        if strand == '-':
            left = str(int(left) + 1)
            right = str(int(right) + 1)

        file.write(
            "\t".join(
                [chrom, left, right, tsr_name, '0', strand]
            ) + "\n"
        )
