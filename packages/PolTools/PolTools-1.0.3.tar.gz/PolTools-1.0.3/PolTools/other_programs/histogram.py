import sys

from collections import defaultdict

from PolTools.utils.build_counts_dict import build_counts_dict

bed_file = sys.argv[1]

five_counts_dict = build_counts_dict(bed_file, 'five')

# Now make the histogram
histogram_dict = defaultdict(int)

max_position = ()
max_counts = -1

for chrom in five_counts_dict:
    for strand in five_counts_dict[chrom]:
        for position, counts in five_counts_dict[chrom][strand].items():
            histogram_dict[counts] += 1

            if counts > max_counts:
                max_position = (chrom, strand, position)
                max_counts = counts

print("Max position has " + str(max_counts) + " counts and is located at " + str(max_position))

# Print out the histogram_dict
for counts in sorted(histogram_dict.keys()):
    print("\t".join([str(counts), str(histogram_dict[counts])]))
