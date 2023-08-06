# Make a track for the input bed file but only show bases that have a minimum value
import sys
import os

from PolTools.utils.make_random_filename import generate_random_filename
from PolTools.utils.remove_files import remove_files

input_bed, chrom_sizes_file, min_value = sys.argv[1:]

min_value = int(min_value)




sorted_bed_file = generate_random_filename()

os.system(
    "bedSort " + input_bed + " " + sorted_bed_file
)


fw_bedgraph = generate_random_filename("-FW.bedgraph")
rv_bedgraph = generate_random_filename("-RV.bedgraph")

# Make the bedgraphs from the file
os.system(
    "bedtools genomecov -i " + sorted_bed_file + " -g " + chrom_sizes_file + " -bg -strand + -5 > " + fw_bedgraph
)

os.system(
    "bedtools genomecov -i " + sorted_bed_file + " -g " + chrom_sizes_file + " -bg -strand - -5 > " + rv_bedgraph
)

# Sort the files
os.system(
    "bedSort " + fw_bedgraph + " " + fw_bedgraph
)

os.system(
    "bedSort " + rv_bedgraph + " " + rv_bedgraph
)

fw_filt_bedgraph = generate_random_filename("-FW.bedgraph")
rv_filt_bedgraph = generate_random_filename("-RV.bedgraph")

# Remove all the positions in the genome that are below the threshold value
with open(fw_bedgraph) as file:
    with open(fw_filt_bedgraph, 'w') as outfile:
        for line in file:
            chrom, left, right, height = line.split()

            if int(height) > min_value:
                outfile.write(line)

with open(rv_bedgraph) as file:
    with open(rv_filt_bedgraph, 'w') as outfile:
        for line in file:
            chrom, left, right, height = line.split()

            if int(height) > min_value:
                outfile.write(line)


min_value = str(min_value)

# Now make the bigwigs
fw_bigwig = input_bed.replace(".bed", "_min" + min_value + "-FW.bw")
rv_bigwig = input_bed.replace(".bed", "_min" + min_value + "-RV.bw")

os.system(
    "bedGraphToBigWig " + fw_filt_bedgraph + " " + chrom_sizes_file + " " + fw_bigwig
)

os.system(
    "bedGraphToBigWig " + rv_filt_bedgraph + " " + chrom_sizes_file + " " + rv_bigwig
)

remove_files(sorted_bed_file, fw_bedgraph, rv_bedgraph, fw_filt_bedgraph, rv_filt_bedgraph)