import os
import sys

from PolTools.utils.bedtools_utils.run_bedtools_getfasta import run_getfasta
from PolTools.utils.make_random_filename import generate_random_filename
from PolTools.utils.remove_files import remove_files

from collections import defaultdict

gene_file = sys.argv[1]
tq_file = sys.argv[2]

motifs = defaultdict(lambda : {
    "motif": "",
    "region": [],
    "position": 0
})

gene_order_list = []

with open(gene_file) as file:
    for line in file:
        gene_name, _, motif, _ = line.split()

        motifs[gene_name]["motif"] = motif.upper()

regions_file = generate_random_filename()

os.system(
    "PolTools make_regions_file_centered_on_max_tss " + tq_file + " 80 > " + regions_file
)

# Get the regions in order of the genes
with open(regions_file) as file:
    for line in file:
        chrom, left, right, name, score, strand = line.split()

        if name in motifs:
            # Only add regions to the ones in the motifs
            motifs[name]["region"] = line.split()

# Make a good regions file
good_regions = generate_random_filename()

with open(good_regions, 'w') as file:
    for gene_name in motifs:
        chrom, left, right, name, score, strand = motifs[gene_name]["region"]

        file.write("\t".join(motifs[gene_name]["region"]) + "\n")
        gene_order_list.append(name)

fasta_file = run_getfasta(good_regions)

with open(fasta_file) as file:
    for i, line in enumerate(file):
        if i % 2 == 0:
            # This line has the > so skip
            continue
        else:
            sequence = line.rstrip().upper()

            curr_gene = gene_order_list[
                int(i / 2)
            ]

            motifs[curr_gene]["position"] = sequence.find(motifs[curr_gene]["motif"]) - 40


remove_files(good_regions, regions_file, fasta_file)

# Now make the output file
for gene_name in motifs:
    bed_formatted_gene_region = motifs[gene_name]["region"]

    # Replace the score with the position
    bed_formatted_gene_region[-2] = str(motifs[gene_name]["position"])

    print(
        "\t".join(bed_formatted_gene_region)
    )
