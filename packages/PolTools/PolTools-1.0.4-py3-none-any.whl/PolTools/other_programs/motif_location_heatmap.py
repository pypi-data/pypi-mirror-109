# The goal is to


# Input: motifs from Juan, gene order sorted by TBP fold change
# Output: heatmap showing the location of the motif



import sys
import re

from collections import defaultdict
from PolTools.utils.bedtools_utils.run_bedtools_getfasta import run_getfasta
from PolTools.utils.remove_files import remove_files
from PolTools.utils.make_random_filename import generate_random_filename
from PolTools.utils.heatmap_utils.generate_heatmap import generate_heatmap

juan_motif_file, tbp_fold_change_file, output_filename, gamma, repeat_amount = sys.argv[1:]
gamma = float(gamma)
repeat_amount = int(repeat_amount)

motifs_dict = defaultdict(
    lambda: {
        "Motif": [],
        "Sequence": ""
    }
)

with open(juan_motif_file) as file:
    for line in file:
        chrom, left, right, tsr_name, gene_name, motif = line.split()

        motifs_dict[gene_name]["Motif"].append(motif.upper())

gene_order = []
with open(tbp_fold_change_file) as file:
    for line in file:
        chrom, left, right, name, score, strand = line.split()

        gene_order.append(name)

# Get the sequences for each gene
fasta_file = run_getfasta(tbp_fold_change_file)

with open(fasta_file) as file:
    for i, line in enumerate(file):
        if i % 2 == 0:
            # This line has the > so go to the next line
            pass
        else:
            sequence = line.rstrip().upper()

            curr_gene_name = gene_order[int(i / 2)]
            motifs_dict[curr_gene_name]["Sequence"] = sequence

remove_files(fasta_file)

# Find the locations and then make the heatmap
# Based regex code from https://stackoverflow.com/questions/4664850/how-to-find-all-occurrences-of-a-substring

heatmap_matrix = []

for gene_name in gene_order:
    motifs = motifs_dict[gene_name]["Motif"]
    curr_seq = motifs_dict[gene_name]["Sequence"]

    # Now lets make the binary list associated with this gene
    bin_list = [0] * len(curr_seq)

    for curr_motif in motifs:
        regex_search_string = '(?=' + curr_motif + ')'

        motif_start_locations = [motif.start() for motif in re.finditer(regex_search_string, curr_seq)]

        # Set all locations of the motif to 1's
        for start_location in motif_start_locations:
            for i in range(len(curr_motif)):
                bin_list[start_location + i] = 1

    heatmap_matrix.append(bin_list)

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
