"""
PyPheWAS Core version 2 (main PyPheWAS code)
Developed by:
    Shikha Chaganti, PhD
    Cailey Kerley

MASI Lab
Department of Electrical Engineering and Computer Science
Vanderbilt University
"""

from collections import Counter
import getopt
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import os
import pandas as pd
import scipy.stats
import statsmodels.discrete.discrete_model as sm
import statsmodels.formula.api as smf
import matplotlib.lines as mlines
from tqdm import tqdm
import time
from collections import OrderedDict


def get_codes():  # same
	"""
	Gets the PheWAS codes from a local csv file and load it into a pandas DataFrame.

	:returns: All of the codes from the resource file.
	:rtype: pandas DataFrame

	"""
	path = os.path.dirname(os.path.abspath(__file__))
	filename = os.sep.join([path, 'resources', 'codes.csv'])
	return pd.read_csv(filename)


def get_group_file(path, filename):  # same
	"""
	Read all of the genotype data from the given file and load it into a pandas DataFrame.

	:param path: The path to the file that contains the phenotype data
	:param filename: The name of the file that contains the phenotype data.
	:type path: string
	:type filename: string

	:returns: The data from the genotype file.
	:rtype: pandas DataFrame
	"""
	wholefname = path + filename
	genotypes_df = pd.read_csv(wholefname)
	genotypes_df = genotypes_df.dropna(subset=['id'])
	genotypes_df.sort_values(by='id', inplace=True)
	return genotypes_df


def get_input(path, filename, reg_type):  # diff -done - add duration
	"""
	Read all of the phenotype data from the given file and load it into a pandas DataFrame.

	:param path: The path to the file that contains the phenotype data
	:param filename: The name of the file that contains the phenotype data.
	:type path: string
	:type filename: string

	:returns: The data from the phenotype file.
	:rtype: pandas DataFrame
	"""
	wholefname = path + filename
	icdfile = pd.read_csv(wholefname)
	icdfile['icd9'] = icdfile['icd9'].str.strip()
	print("...")
	if reg_type == 0:
		phenotypes = pd.merge(icdfile, codes, on='icd9')
		print("...")
		phenotypes['MaxAgeAtICD'] = 0
		phenotypes['MaxAgeAtICD'] = phenotypes.groupby(['id', 'phewas_code'])['AgeAtICD'].transform('max')
		print("...")
		phenotypes.sort_values(by='id', inplace=True)
		print("...")
	else:
		"""
		This needs to be changed, need to adjust for a variety of different naming conventions
		in the phenotype file, not simply 'AgeAtICD', 'id', 'icd9', etc.
		Either we need to adjust for different names in the code, or state explicitly in the
		documentation that we cannot do things like this.
		"""
		phenotypes = pd.merge(icdfile, codes, on='icd9')
		phenotypes['count'] = 0
		phenotypes['count'] = phenotypes.groupby(['id', 'phewas_code'])['count'].transform('count')
		phenotypes['duration'] = phenotypes.groupby(['id', 'phewas_code'])['AgeAtICD'].transform('max') - \
								 phenotypes.groupby(['id', 'phewas_code'])['AgeAtICD'].transform('min') + 1
		phenotypes['MaxAgeAtICD'] = 0
		phenotypes['MaxAgeAtICD'] = phenotypes.groupby(['id', 'phewas_code'])['AgeAtICD'].transform('max')
	return phenotypes


def generate_feature_matrix(genotypes_df, icds, reg_type, phewas_cov=''):
	"""
	Generates the feature matrix that will be used to run the regressions.

	:param genotypes:
	:param icds:
	:type genotypes:
	:type icds:

	:returns:
	:rtype:

	"""

	feature_matrix = np.zeros((3, genotypes_df.shape[0], phewas_codes.shape[0]), dtype=float)

	# make genotype a dictionary for faster access time
	genotypes = genotypes_df.set_index('id').to_dict('index')

	# use phewascodes to make a dictionary of indices in the np array
	empty_phewas_df = phewas_codes.set_index('phewas_code')
	empty_phewas_df.sort_index(inplace=True)
	empty_phewas_df['np_index'] = range(0,empty_phewas_df.shape[0])
	np_index = empty_phewas_df['np_index'].to_dict()

	exclude = []  # list of ids to exclude (in icd list but not in genotype list)
	last_id = ''  # track last id seen in icd list
	count = -1

	for index, data in tqdm(icds.iterrows(), desc="Processing ICDs", total=icds.shape[0]):
		if reg_type == 0:
			curr_id = data['id']
			if not curr_id in genotypes:
				if not curr_id in exclude:
					print('%s has records in icd file but is not in group file - excluding from study' % (curr_id))
					exclude.append(curr_id)
				continue
			# check id to see if a new subject has been found
			if last_id != curr_id:
				count += 1
				last_id = curr_id  # reset last_id
				feature_matrix[1][count] = genotypes[curr_id]['MaxAgeAtVisit']

			# add data to feature matrices
			phecode_ix = np_index[data['phewas_code']]
			feature_matrix[0][count][phecode_ix] = 1
			feature_matrix[1][count][phecode_ix] = data['MaxAgeAtICD']
			if phewas_cov:
				# TODO: add phewas_cov
				continue

		elif reg_type == 1:
			# TODO: add linear regression
			print("linear (count) regression is not currently supported")
			return -1
		else:
			# TODO: add duration regression
			print("duration regression is not currently supported")
			return -1

	return feature_matrix



"""

Statistical Modeling

"""


def get_phewas_info(p_index):  # same
	"""
	Returns all of the info of the phewas code at the given index.

	:param p_index: The index of the desired phewas code
	:type p_index: int

	:returns: A list including the code, the name, and the rollup of the phewas code. The rollup is a list of all of the ICD-9 codes that are grouped into this phewas code.
	:rtype: list of strings
	"""
	p_code = phewas_codes.loc[p_index].phewas_code
	corresponding = codes[codes.phewas_code == p_code]

	p_name = corresponding.iloc[0].phewas_string
	p_rollup = ','.join(codes[codes.phewas_code == p_code].icd9.tolist())
	return [p_code, p_name, p_rollup]


def calculate_odds_ratio(genotypes, phen_vector1, phen_vector2, reg_type, covariates, lr=0, response='',
						 phen_vector3=''):  # diff - done
	"""
	Runs the regression for a specific phenotype vector relative to the genotype data and covariates.

	:param genotypes: a DataFrame containing the genotype information
	:param phen_vector: a array containing the phenotype vector
	:param covariates: a string containing all desired covariates
	:type genotypes: pandas DataFrame
	:type phen_vector: numpy array
	:type covariates: string

	.. note::
		The covariates must be a string that is delimited by '+', not a list.
		If you are using a list of covariates and would like to convert it to the pyPhewas format, use the following::

			l = ['genotype', 'age'] # a list of your covariates
			covariates = '+'.join(l) # pyPhewas format

		The covariates that are listed here *must* be headers to your genotype CSV file.
	"""

	data = genotypes
	data['y'] = phen_vector1
	data['MaxAgeAtICD'] = phen_vector2
	# f='y~'+covariates
	if response:
		f = response + '~ y + genotype +' + covariates
		if phen_vector3.any():
			data['phe'] = phen_vector3
			f = response + '~ y + phe + genotype' + covariates
	else:
		f = 'genotype ~ y +' + covariates
		if phen_vector3.any():
			data['phe'] = phen_vector3
			f = 'genotype ~ y + phe +' + covariates
	try:
		if lr == 0:
			logreg = smf.logit(f, data).fit(disp=False)
			p = logreg.pvalues.y
			odds = 0  #
			conf = logreg.conf_int()
			od = [-math.log10(p), p, logreg.params.y, '[%s,%s]' % (conf[0]['y'], conf[1]['y'])]
		elif lr == 1:
			f1 = f.split(' ~ ')
			f1[1] = f1[1].replace(" ", "")
			logit = sm.Logit(data[f1[0].strip()], data[f1[1].split('+')])
			lf = logit.fit_regularized(method='l1', alpha=0.1, disp=0, trim_mode='size', qc_verbose=0)
			p = lf.pvalues.y
			odds = 0
			conf = lf.conf_int()
			od = [-math.log10(p), p, lf.params.y, '[%s,%s]' % (conf[0]['y'], conf[1]['y'])]
		else:
			linreg = smf.logit(f, data).fit(method='bfgs', disp=False)
			p = linreg.pvalues.y
			odds = 0
			conf = linreg.conf_int()
			od = [-math.log10(p), p, linreg.params.y, '[%s,%s]' % (conf[0]['y'], conf[1]['y'])]
	except:
		odds = 0
		p = np.nan
		od = [np.nan, np.nan, np.nan, np.nan]
	return (odds, p, od)


def run_phewas(fm, genotypes, covariates, reg_type, response='', phewas_cov=''):  # same
	"""
	For each phewas code in the feature matrix, run the specified type of regression and save all of the resulting p-values.

	:param fm: The phewas feature matrix.
	:param genotypes: A pandas DataFrame of the genotype file.
	:param covariates: The covariates that the function is to be run on.

	:returns: A tuple containing indices, p-values, and all the regression data.
	"""
	m = len(fm[0, 0])
	p_values = np.zeros(m, dtype=float)
	icodes = []
	# store all of the pertinent data from the regressions
	regressions = pd.DataFrame(columns=output_columns)
	control = fm[0][genotypes.genotype == 0, :]
	disease = fm[0][genotypes.genotype == 1, :]
	inds = np.where((control.any(axis=0) & ~disease.any(axis=0)) | (~control.any(axis=0) & disease.any(axis=0)))[0]
	for index in tqdm(range(m), desc='Running Regressions'):
		phen_vector1 = fm[0][:, index]
		phen_vector2 = fm[1][:, index]
		phen_vector3 = fm[2][:, index]
		if np.where(phen_vector1 > 0)[0].shape[0] > 5:
			if index in inds:
				# print get_phewas_info(index)
				res = calculate_odds_ratio(genotypes, phen_vector1, phen_vector2, reg_type, covariates, lr=1,
										   response=response,
										   phen_vector3=phen_vector3)
			else:
				res = calculate_odds_ratio(genotypes, phen_vector1, phen_vector2, reg_type, covariates, lr=0,
										   response=response,
										   phen_vector3=phen_vector3)
		else:
			odds = 0
			p = 1
			od = [-0.0, 1.0, 0.0, np.nan]
			res = (odds, p, od)

		# save all of the regression data

		phewas_info = get_phewas_info(index)
		stat_info = res[2]
		info = phewas_info[0:2] + stat_info + [phewas_info[2]]

		regressions.loc[index] = info

		p_values[index] = res[1]
	return regressions


def get_bon_thresh(normalized, power):  # same
	"""
	Calculate the bonferroni correction threshold.

	Divide the power by the sum of all finite values (all non-nan values).

	:param normalized: an array of all normalized p-values. Normalized p-values are -log10(p) where p is the p-value.
	:param power: the threshold power being used (usually 0.05)
	:type normalized: numpy array
	:type power: float

	:returns: The bonferroni correction
	:rtype: float

	"""
	return power / sum(np.isfinite(normalized))


def get_fdr_thresh(p_values, power):
	"""
	Calculate the false discovery rate threshold.

	:param p_values: a list of p-values obtained by executing the regression
	:param power: the thershold power being used (usually 0.05)
	:type p_values: numpy array
	:type power: float

	:returns: the false discovery rate
	:rtype: float
	"""
	sn = np.sort(p_values)
	sn = sn[np.isfinite(sn)]
	sn = sn[::-1]
	for i in range(len(sn)):
		thresh = power * i / len(sn)
		if sn[i] <= thresh:
			break
	return sn[i]


def get_bhy_thresh(p_values, power):
	"""
	Calculate the false discovery rate threshold.

	:param p_values: a list of p-values obtained by executing the regression
	:param power: the thershold power being used (usually 0.05)
	:type p_values: numpy array
	:type power: float

	:returns: the false discovery rate
	:rtype: float
	"""
	sn = np.sort(p_values)
	sn = sn[np.isfinite(sn)]
	sn = sn[::-1]
	for i in range(len(sn)):
		thresh = power * i / (8.1 * len(sn))
		if sn[i] <= thresh:
			break
	return sn[i]


def get_imbalances(regressions):
	"""
	Generates a numpy array of the imbalances.

	For a value *x* where *x* is the beta of a regression:

	========= ====== =======================================================
	*x* < 0   **-1** The regression had a negative beta value
	*x* = nan **0**  The regression had a nan beta value (and a nan p-value)
	*x* > 0   **+1** The regression had a positive beta value
	========= ====== =======================================================

	These values are then used to get the correct colors using the imbalance_colors.

	:param regressions: DataFrame containing a variety of different output values from the regression performed. The only one used for this function are the 'beta' values.
	:type regressions: pandas DataFrame

	:returns: A list that is the length of the number of regressions performed. Each element in the list is either a -1, 0, or +1. These are used as explained above.
	:rtype: numpy array
	"""

	imbalance = np.array(regressions['beta'])
	imbalance[np.isnan(imbalance)] = 0
	imbalance[imbalance > 0] = 1
	imbalance[imbalance < 0] = -1
	return imbalance


def get_x_label_positions(categories, lines=True):  # same
	"""
	This method is used get the position of the x-labels and the lines between the columns

	:param categories: list of the categories
	:param lines: a boolean which determines the locations returned (either the center of each category or the end)
	:type categories:
	:type lines: bool

	:returns: A list of positions
	:rtype: list of ints

	"""
	tt = Counter(categories)
	s = 0
	label_positions = []
	for _, v in tt.items():
		if lines:
			inc = v // 2
		else:
			inc = v
		label_positions.append(s + inc)
		s += v
	return label_positions


def plot_data_points(y, thresh, save='', imbalances=np.array([])):  # same
	"""
	Plots the data with a variety of different options.

	This function is the primary plotting function for pyPhewas.

	:param x: an array of indices
	:param y: an array of p-values
	:param thresh: the threshold power
	:param save: the output file to save to (if empty, display the plot)
	:param imbalances: a list of imbalances
	:type x: numpy array
	:type y: numpy array
	:type thresh: float
	:type save: str
	:type imbalances: numpy array

	"""

	# Determine whether or not to show the imbalance.
	fig = plt.figure()
	ax = plt.subplot(111)
	show_imbalance = imbalances.size != 0

	# Sort the phewas codes by category.
	c = codes.loc[phewas_codes['index']]
	c = c.reset_index()
	idx = c.sort_values(by='category').index

	# Get the position of the lines and of the labels
	# linepos = get_x_label_positions(c['category'].tolist(), False)
	# x_label_positions = get_x_label_positions(c['category'].tolist(), True)
	# x_labels = c.sort_values('category').category_string.drop_duplicates().tolist()

	# Plot each of the points, if necessary, label the points.
	e = 1
	artists = []
	frame1 = plt.gca()
	# ax.axhline(y=-math.log10(0.05), color='yellow', ls='dotted')
	ax.axhline(y=thresh, color='red', ls='dotted')
	# ax.axhline(y=thresh1, color='yellow', ls='dotted')
	# ax.axhline(y=thresh, color='orange', ls='dotted')
	# ax.xticks(x_label_positions, x_labels, rotation=70, fontsize=10)
	# ax.xlim(xmin=0, xmax=len(c))
	plt.ylabel('-log10(p)')
	# if thresh_type == 0:
	#     thresh = thresh0
	# elif thresh_type == 1:
	#     thresh = thresh1
	# else:
	#     thresh = thresh2

	# y_label_positions = [thresh]#[thresh0, thresh1,thresh2]

	# plt.yticks(y_label_positions, ['Bonf p = ' + '{:.2e}'.format(np.power(10, -thresh0)),
	#                               'Benj-Hoch p = ' + str(round(np.power(10, -thresh1), 3)),
	#                            'Benj-Hoch-Yek p = ' + str(round(np.power(10, -thresh2), 3))], rotation=10, fontsize=10)
	for i in idx:
		if y[i] > thresh:
			e += 15
			if show_imbalance:  # and imbalances[i]>0:
				# if imbalances[i]>0:
				artists.append(ax.text(e, y[i], c['phewas_string'][i], rotation=89, va='bottom', fontsize=8))
			# else:
			#	artists.append(ax.text(e, -y[i], c['phewas_string'][i], rotation=271, va='top',fontsize=8))
			elif not show_imbalance:
				artists.append(ax.text(e, y[i], c['phewas_string'][i], rotation=89, va='bottom'))
		else:
			e += 0

		if show_imbalance:
			if y[i] > thresh:
				if imbalances[i] > 0:
					ax.plot(e, y[i], '+', color=plot_colors[c[i:i + 1].category_string.values[0]], fillstyle='full',
							markeredgewidth=1.5)

				else:
					# ax.plot(e,y[i],'o', color=plot_colors[c[i:i+1].category_string.values[0]], fillstyle='full', markeredgewidth=0.0)
					ax.plot(e, y[i], '_', color=plot_colors[c[i:i + 1].category_string.values[0]], fillstyle='full',
							markeredgewidth=1.5)
		else:
			ax.plot(e, y[i], 'o', color=plot_colors[c[i:i + 1].category_string.values[0]], fillstyle='full',
					markeredgewidth=0.0)
	line1 = []
	box = ax.get_position()
	ax.set_position([box.x0, box.y0 + box.height * 0.05, box.width, box.height * 0.95])
	for lab in plot_colors.keys():
		line1.append(
			mlines.Line2D(range(1), range(1), color="white", marker='o', markerfacecolor=plot_colors[lab], label=lab))
	artists.append(
		ax.legend(handles=line1, bbox_to_anchor=(0.5, 0), loc='upper center', fancybox=True, ncol=4, prop={'size': 6}))
	ax.axhline(y=0, color='black')
	frame1.axes.get_xaxis().set_visible(False)

	# If the imbalance is to be shown, draw lines to show the categories.
	# if show_imbalance:
	# 	for pos in linepos:
	# 		ax.axvline(x=pos, color='black', ls='dotted')
	# Determine the type of output desired (saved to a plot or displayed on the screen)
	if save:
		pdf = PdfPages(save)
		pdf.savefig(bbox_extra_artists=artists, bbox_inches='tight')
		pdf.close()
	else:
		ax.subplots_adjust(left=0.05, right=0.85)
		ax.show()

	# Clear the plot in case another plot is to be made.
	plt.clf()


def plot_odds_ratio(y, p, thresh, save='', imbalances=np.array([])):  # same
	"""
	Plots the data with a variety of different options.

	This function is the primary plotting function for pyPhewas.

	:param x: an array of indices
	:param y: an array of p-values
	:param thresh: the threshold power
	:param save: the output file to save to (if empty, display the plot)
	:param imbalances: a list of imbalances
	:type x: numpy array
	:type y: numpy array
	:type thresh: float
	:type save: str
	:type imbalances: numpy array

	"""

	# Determine whether or not to show the imbalance.
	fig = plt.figure()
	ax = plt.subplot(111)
	show_imbalance = imbalances.size != 0

	# Sort the phewas codes by category.
	c = codes.loc[phewas_codes['index']]
	c = c.reset_index()
	idx = c.sort_values(by='category').index

	# Get the position of the lines and of the labels
	# linepos = get_x_label_positions(c['category'].tolist(), False)
	# x_label_positions = get_x_label_positions(c['category'].tolist(), True)
	# x_labels = c.sort_values('category').category_string.drop_duplicates().tolist()

	# Plot each of the points, if necessary, label the points.
	e = 1
	artists = []
	frame1 = plt.gca()
	# ax.xticks(x_label_positions, x_labels, rotation=70, fontsize=10)
	plt.xlabel('Log odds ratio')

	# if thresh_type == 0:
	#     thresh = thresh0
	# elif thresh_type == 1:
	#     thresh = thresh1
	# else:
	#     thresh = thresh2

	# plt.xlim(xmin=min(y[p>thresh,1]), xmax=max(y[p>thresh,2]))

	for i in idx:
		if p[i] > thresh:
			e += 15
			if show_imbalance:  # and imbalances[i]>0:
				if imbalances[i] > 0:
					artists.append(ax.text(y[i][0], e, c['phewas_string'][i], rotation=0, ha='left', fontsize=6))
				else:
					artists.append(ax.text(y[i][0], e, c['phewas_string'][i], rotation=0, ha='right', fontsize=6))
			elif not show_imbalance:
				artists.append(ax.text(e, y[i][0], c['phewas_string'][i], rotation=40, va='bottom'))
		else:
			e += 0

		if show_imbalance:
			if p[i] > thresh:
				ax.plot(y[i][0], e, 'o', color=plot_colors[c[i:i + 1].category_string.values[0]], fillstyle='full',
						markeredgewidth=0.0)
				ax.plot([y[i, 1], y[i, 2]], [e, e], color=plot_colors[c[i:i + 1].category_string.values[0]])
		# else:
		# ax.plot(e,y[i],'o', color=plot_colors[c[i:i+1].category_string.values[0]], fillstyle='full', markeredgewidth=0.0)
		#	ax.plot(e,-y[i],'o', color=plot_colors[c[i:i+1].category_string.values[0]], fillstyle='full', markeredgewidth=0.0)
		else:
			ax.plot(e, y[i], 'o', color=plot_colors[c[i:i + 1].category_string.values[0]], fillstyle='full',
					markeredgewidth=0.0)
	line1 = []
	box = ax.get_position()
	ax.set_position([box.x0, box.y0 + box.height * 0.05, box.width, box.height * 0.95])
	for lab in plot_colors.keys():
		line1.append(
			mlines.Line2D(range(1), range(1), color="white", marker='o', markerfacecolor=plot_colors[lab], label=lab))
	artists.append(ax.legend(handles=line1, bbox_to_anchor=(0.5, -0.15), loc='upper center', fancybox=True, ncol=4,
							 prop={'size': 6}))
	ax.axvline(x=0, color='black')
	frame1.axes.get_yaxis().set_visible(False)

	# If the imbalance is to be shown, draw lines to show the categories.
	# if show_imbalance:
	# 	for pos in linepos:
	# 		ax.axvline(x=pos, color='black', ls='dotted')
	# Determine the type of output desired (saved to a plot or displayed on the screen)
	if save:
		pdf = PdfPages(save)
		pdf.savefig(bbox_extra_artists=artists, bbox_inches='tight')
		pdf.close()
	else:
		ax.subplots_adjust(left=0.05, right=0.85)
		ax.show()

	# Clear the plot in case another plot is to be made.
	plt.clf()


def process_args(kwargs, optargs, *args):
	clean = np.vectorize(lambda x: x[x.rfind('-') + 1:] + '=')
	searchfor = clean(list(optargs.keys()))
	opts, rem = getopt.getopt(args, '', searchfor)
	assert len(rem) == 0, 'Unknown arguments included %s' % (str(rem))
	for option in opts:
		k, v = option
		kwargs[optargs[k]] = v

	return kwargs


def display_kwargs(kwargs):
	print("Arguments: ")
	for k, v in kwargs.items():
		left = str(k).ljust(30, '.')
		right = str(v).rjust(50, '.')
		print(left + right)


output_columns = ['PheWAS Code',
				  'PheWAS Name',
				  '\"-log(p)\"',
				  'p-val',
				  'beta',
				  'Conf-interval beta',
				  'ICD-9']

plot_colors = {'-': 'gold',
			   'circulatory system': 'red',
			   'congenital anomalies': 'mediumspringgreen',
			   'dermatologic': 'maroon',
			   'digestive': 'green',
			   'endocrine/metabolic': 'darkred',
			   'genitourinary': 'black',
			   'hematopoietic': 'orange',
			   'infectious diseases': 'blue',
			   'injuries & poisonings': 'slategray',
			   'mental disorders': 'fuchsia',
			   'musculoskeletal': 'darkgreen',
			   'neoplasms': 'teal',
			   'neurological': 'midnightblue',
			   'pregnancy complications': 'gold',
			   'respiratory': 'brown',
			   'sense organs': 'darkviolet',
			   'symptoms': 'darkviolet'}
imbalance_colors = {
	0: 'white',
	1: 'deepskyblue',
	-1: 'red'
}
regression_map = {
	'log': 0,
	'lin': 1,
	'lind': 2
}
threshold_map = {
	'bon': 0,
	'fdr': 1
}

codes = get_codes()
phewas_codes = pd.DataFrame(codes['phewas_code'].drop_duplicates());
phewas_codes.sort_values(by=['phewas_code'], inplace=True)
phewas_codes.reset_index(inplace=True)
