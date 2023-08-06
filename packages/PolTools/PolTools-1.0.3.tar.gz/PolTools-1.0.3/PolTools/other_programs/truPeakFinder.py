import scipy
import numpy as np
from scipy.optimize import leastsq  # Levenberg-Marquandt: leastsq
import sys
import os
import warnings

from collections import defaultdict

from PolTools.utils.remove_files import remove_files
from PolTools.utils.make_random_filename import generate_random_filename


def get_pileups_dict(input_file, chrom_size_file):
	pileup_dict = defaultdict(lambda: defaultdict(int))

	bedgraph_file = generate_random_filename('.bedGraph')

	os.system(
		'bedtools genomecov -i ' + input_file + ' -g ' + chrom_size_file + ' -bg > ' + bedgraph_file
	)

	with open(bedgraph_file) as file:
		for line in file:
			chrom, left, right, height = line.split()

			left = int(left)
			right = int(right)
			height = int(height)

			for position in range(left, right):
				pileup_dict[chrom][position] = height

	return pileup_dict, bedgraph_file


def make_fragment_file(input_file, min_fragment_length, max_fragment_length):
	fragment_file = generate_random_filename()

	with open(fragment_file, 'w') as outfile:
		with open(input_file) as file:
			for line in file:
				chrom, left, right, name, score, strand = line.split()

				left = int(left)
				right = int(right)

				fragment_length = right - left

				if fragment_length >= min_fragment_length and fragment_length <= max_fragment_length:
					outfile.write(line)

	return fragment_file


def get_chrom_sizes_dict(chrom_size_file):
	chrom_sizes_dict = defaultdict(int)

	with open(chrom_size_file) as file:
		for line in file:
			chromosome, size = line.split()
			size = int(size)

			chrom_sizes_dict[chromosome] = size

	return chrom_sizes_dict


# Returns (height, center_x, width_x), the gaussian parameters of distribution found by a fit
def fit_gaussian(array):
	# The array input has two columns. The first is the genomic position and the second is the height at that position.
	position = array[:, 0]
	height = array[:, 1]

	max_height = height.max()

	# This is the weighted average of the peak
	mean = sum(position * height) / sum(height)

	standard_deviation = np.sqrt(abs(sum((position - mean) ** 2 * height) / sum(height)))

	p0 = np.c_[max_height, mean, standard_deviation]

	# TODO: Errors out when the last value in p0 is less than one
	# The leastsq function is used to minimize the sum of squares of the error function with an estimate of the max height.
	# This is only possible when the standard deviation is greater than 1 (because if it is 0 then it must only be that peak)

	if standard_deviation > 1:
		with warnings.catch_warnings():
			warnings.simplefilter("ignore")
			p1, success = scipy.optimize.leastsq(error_function, p0.copy()[0], args=(position, height), maxfev=0)

		# Only return the position if it is within the possible positions
		if p1[0] < 2 * max_height and p1[1] > position.min() and p1[1] < position.max():
			return p1

		else:
			return np.array([0, 0, 0])

	return np.array([0, 0, 0])


# define a gaussian fitting function where
# p[0] = amplitude/height, p[1] = mean, p[2] = sigma
def fitfunc(p, x):
	amplitude, mean, sigma = p
	if sigma != 0:
		return amplitude * np.exp(-0.5 * (((x - mean) / sigma) ** 2))
	else:
		return 0


def error_function(p, x, y):
	return fitfunc(p, x) - y


def remove_peaks_close_together_helper(min_distance_between_peaks, overlapping_peaks, chrom_data):
	# Finds the max peak and keeps it. Removes all peaks within min_distance_between_peaks. Repeats until no peaks remain.
	data = {peak: chrom_data[peak] for peak in overlapping_peaks}

	kept_peaks = []

	while data:
		# Get the current max
		curr_max_peak_position = max(data, key=data.get)

		# Add the max to the kept peaks
		kept_peaks.append(curr_max_peak_position)

		# Remove all peaks within min_distance_between_peaks
		data = {k: v for k, v in data.items() if abs(curr_max_peak_position - k) > min_distance_between_peaks}

	# The peaks are not sorted like they need to be, so we fix that quick
	return sorted(kept_peaks)


def remove_peaks_close_together(min_distance_between_peaks, peaks, chrom_data):
	filtered_peaks = []

	overlapping_peaks = []
	currently_overlapping = False

	for i, peak in enumerate(peaks[:-1]):
		# Each peak just has the location
		next_peak = peaks[i + 1]

		distance_between_peaks = next_peak - peak

		if distance_between_peaks < min_distance_between_peaks:
			# Add to the currently overlapping and continue until they don't overlap
			currently_overlapping = True
			overlapping_peaks.append(peak)

		else:
			if currently_overlapping:
				# The current peak does not overlap with the previous ones, so we find peaks in the previously overlapping
				currently_overlapping = False

				# The current peak is overlapping with the previous one, so don't forget to add it
				overlapping_peaks.append(peak)

				f = remove_peaks_close_together_helper(min_distance_between_peaks, overlapping_peaks, chrom_data)
				filtered_peaks.extend(f)
				overlapping_peaks = []

			else:
				filtered_peaks.append(peak)

	return filtered_peaks


def find_peaks_in_chromosome(chrom_data, threshold, window_radius, chrom_size, min_distance_between_peaks):
	# extract peaks from enriched regions

	inflection_points = []
	for position in range(chrom_size + 1):
		curr_slope = chrom_data[position + 1] - chrom_data[position]
		next_slope = chrom_data[position + 2] - chrom_data[position + 1]

		if curr_slope > 0 and next_slope <= 0:
			inflection_points.append(position)

	peaks = []

	# Go through each inflection point and determine if it is a peak
	for infl_point in inflection_points:
		# An inflection point is a peak if dip is above the threshold in the window size
		left_region_boundary = infl_point - window_radius
		right_region_boundary = infl_point + window_radius

		# Make sure the boundaries are possible
		if left_region_boundary < 0:
			left_region_boundary = 0
		if right_region_boundary > chrom_size:
			right_region_boundary = chrom_size

		region_dict = {k: chrom_data[k] for k in range(left_region_boundary, right_region_boundary + 1)}

		max_height_location = max(region_dict, key=region_dict.get)
		max_height = region_dict[max_height_location]
		min_height = max(region_dict.values())

		dip = min_height / max_height

		if dip > threshold:
			# We know this is a peak
			peaks.append(max_height_location)

	filtered_peaks = remove_peaks_close_together(min_distance_between_peaks, peaks, chrom_data)

	return filtered_peaks


def find_peaks(threshold, pileup_dict, window_size, chrom_sizes_dict, min_distance_between_peaks):
	peaklist = defaultdict(list)

	for chrom in pileup_dict:
		# Set chrom_data to the current chromosome's data
		chrom_data = pileup_dict[chrom]

		chrom_size = chrom_sizes_dict[chrom]

		peaks = find_peaks_in_chromosome(chrom_data, threshold, window_size, chrom_size, min_distance_between_peaks)

		for x in range(len(peaks) - 1):
			curr_peak = peaks[x]
			next_peak = peaks[x + 1]

			# Make an array w with values of the position and the height
			# This is going through each position between peaks and making an array with the positions and heights
			w = np.array([[position, chrom_data[position]] for position in range(curr_peak, next_peak)])

			# Fit the peak array (position and heights array) to a gaussian distribution
			p1 = fit_gaussian(w)

			if not np.array_equal(p1, [0, 0, 0]):
				height, center_x, center_y = p1
				center_x = int(center_x)

				peaklist[chrom].append(
					[chrom, center_x, center_x + 1, fitfunc(p1, center_x)]
				)

	return peaklist


def make_bigwig_files(peaklist, chrom_size_file, input_file, fragment_bedgraph_file):
	bedgraph_output_file = 'output_file.bedGraph'

	with open(bedgraph_output_file, 'w') as file:
		for chrom in peaklist:
			for peak in peaklist[chrom]:
				file.write(
					"\t".join(str(val) for val in peak) + "\n"
				)

	# Convert the peaks to bigwig
	os.system(
		"bedGraphToBigWig " + bedgraph_output_file + " " + chrom_size_file + " output_file.bw"
	)

	# Convert the original file to a bigwig
	tmp_file = generate_random_filename('.tmp')
	os.system(
		'bedtools genomecov -i ' + input_file + ' -g ' + chrom_size_file + ' -bg > ' + tmp_file
	)

	os.system(
		"bedGraphToBigWig " + tmp_file + " " + chrom_size_file + " input_file.bw"
	)

	# Convert the fragments file to a bigwig
	os.system(
		"bedGraphToBigWig " + fragment_bedgraph_file + " " + chrom_size_file + " fragments.bw"
	)

	remove_files(tmp_file, bedgraph_output_file)


def run_truPeak_finder():
	input_file, chrom_size_file, min_fragment_length, max_fragment_length = sys.argv[1:]

	min_fragment_length = int(min_fragment_length)
	max_fragment_length = int(max_fragment_length)

	threshold = 0.6
	window_size = 100
	min_distance_between_peaks = 50

	print("Removing fragments shorter than " + str(min_fragment_length) + " bp or longer than " +
		  str(max_fragment_length) + " bp ...")
	fragment_file = make_fragment_file(input_file, min_fragment_length, max_fragment_length)

	print('Importing Alignment File ...')
	pileup_dict, fragment_bedgraph_file = get_pileups_dict(fragment_file, chrom_size_file)

	chrom_sizes_dict = get_chrom_sizes_dict(chrom_size_file)

	print('Finding Peaks ...')
	peaks_dict = find_peaks(threshold, pileup_dict, window_size, chrom_sizes_dict,
							min_distance_between_peaks)

	number_peaks_found = sum([len(peaks_list) for peaks_list in peaks_dict.values()])
	print(str(number_peaks_found) + " peaks were found.")

	print("Making bigwig files ...")
	make_bigwig_files(peaks_dict, chrom_size_file, input_file, fragment_bedgraph_file)

	remove_files(fragment_file, fragment_bedgraph_file)


if __name__ == '__main__':
	run_truPeak_finder()
