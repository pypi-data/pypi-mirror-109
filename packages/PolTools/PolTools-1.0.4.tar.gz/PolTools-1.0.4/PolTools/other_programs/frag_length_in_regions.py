# Determines the lengths of fragments with a 5' end in regions

import sys


from multiprocessing import Pool


from PolTools.utils.make_transcripts_dict import build_transcripts_dict
from collections import defaultdict


regions_file = sys.argv[1]
output_file = sys.argv[2]
sequencing_files = sys.argv[3:]

regions = []

with open(regions_file) as file:
    for line in file:
        if line.split():
            regions.append(line.split())

with Pool() as pool:
    dicts = pool.map(build_transcripts_dict, sequencing_files)

transcripts_dicts = {seq_file: dicts[i] for i, seq_file in enumerate(sequencing_files)}

# Keys of the length and values of a dictionary with the keys of filenames and values of the number of fragments
frag_lengths = defaultdict(lambda: defaultdict(int))

# Loop through each base in the regions
for region in regions:
    chrom, left, right, name, score, strand = region

    for base in range(int(left), int(right)):
        for seq_file in sequencing_files:
            if base in transcripts_dicts[seq_file][chrom][strand]:
                for three_prime_position in transcripts_dicts[seq_file][chrom][strand][base]:

                    curr_length = three_prime_position - base + 1
                    frag_lengths[curr_length][seq_file] += 1

# Output the data for fragments up to 100 bp
with open(output_file, 'w') as file:
    # Print the header first
    file.write(
        "\t".join(
            ["Length"] + [seq_file.split("/")[-1] for seq_file in sequencing_files]
        ) + "\n"
    )

    for i in range(101):
        file.write(
            "\t".join(
                [str(i)] + [str(frag_lengths[i][seq_file]) for seq_file in sequencing_files]
            ) + "\n"
        )