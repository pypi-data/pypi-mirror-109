import sys

from PolTools.utils.build_counts_dict import build_counts_dict

# Goal is to make a regions file that has all the positions which have at least 10 5' counts in the dataset

# First get the dataset
seq_file = sys.argv[1]
chrom_sizes_file = sys.argv[2]

sizes_dict = {}
with open(chrom_sizes_file) as file:
    for line in file:
        chrom, size = line.split()
        sizes_dict[chrom] = int(size)

min_value = 0
five_dict = build_counts_dict(seq_file, 'five')

# Now we just need to go through each position and print it out
count = 0
for chromosome in five_dict:
    if 'chr' not in chromosome:
        continue

    for strand in five_dict[chromosome]:
        for position in five_dict[chromosome][strand]:
            if five_dict[chromosome][strand][position] > min_value:


                if position >= 0 and position <= sizes_dict[chromosome]:
                    tss_name = "TSS" + str(count)
                    print(
                        "\t".join(
                            [chromosome, str(position), str(int(position) + 1), tss_name , '0', strand]
                        )
                    )

                    count += 1