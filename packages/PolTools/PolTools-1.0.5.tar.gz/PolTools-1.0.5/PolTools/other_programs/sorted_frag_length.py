# Determines the lengths of fragments with a 5' end in regions

# Makes a table getting transcript lengths for each of the regions files -- regions are maxTSSs

import sys
import os

from PolTools.utils.make_transcripts_dict import build_transcripts_dict
from PolTools.utils.make_random_filename import generate_random_filename

from collections import defaultdict


sequencing_file = sys.argv[1]
regions_files = sys.argv[2:]

# Remove all reads that are unnecesary
cleaned_seq_file = generate_random_filename()

os.system(
    'bedtools intersect -wa -a ' + sequencing_file + ' -b ' + regions_files[0] + ' > ' + cleaned_seq_file
)

# Build the transcripts dict
transcript_dict = build_transcripts_dict(sequencing_file)

# Go through each of the regions and build the table dict which has keys of length and values of
# the regions filename and values of the number of transcripts with that length

table_dict = defaultdict(lambda: defaultdict(int))

for reg_file in regions_files:
    with open(reg_file) as file:
        for line in file:
            chrom, left, right, name, score, strand = line.split()

            five_prime_end = int(left)

            # Go through each transcript in the dataset that starts at this base
            if five_prime_end in transcript_dict[chrom][strand]:
                for three_prime_end in transcript_dict[chrom][strand][five_prime_end]:
                    length = abs(five_prime_end - three_prime_end) + 1

                    table_dict[length][reg_file] += 1

print(table_dict)

# Print out the table
with open("frag_length_table", 'w') as file:
    # Print the headers first
    file.write(
        "\t".join(
            ["Length"] + regions_files
        ) + "\n"
    )

    # Print the first 100 nt lengths
    for i in range(101):
        file.write(
            "\t".join(
                [str(i)] + [str(table_dict[i][reg_file]) for reg_file in regions_files]
            ) + "\n"
        )
