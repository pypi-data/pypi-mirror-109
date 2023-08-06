import os
import argparse

from kocher_tools.plink2 import Plink2

def fstParser ():
	'''
	Argument parser for Fst calc

	Raises
	------
	IOError
		If the input, or other specified files do not exist
	'''

	def confirmFile ():
		'''Custom action to confirm file exists'''
		class customAction(argparse.Action):
			def __call__(self, parser, args, value, option_string=None):
				if not os.path.isfile(value):
					raise IOError('%s not found' % value)
				setattr(args, self.dest, value)
		return customAction

	def metavarList (var_list):
		'''Create a formmated metavar list for the help output'''
		return '{' + ', '.join(var_list) + '}'

	fst_parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)

	# Input arguments
	input_method = fst_parser.add_mutually_exclusive_group(required = True)
	input_method.add_argument('--vcf-filename', help = 'Filename of the VCF file', type = str, action = confirmFile())
	input_method.add_argument('--bed-prefix', help = 'Filename of the Binary-PED prefix', type = str)

	# Model input arguments
	fst_parser.add_argument('--model-file', help = 'Filename of the Model file', type = str, required = True, action = confirmFile())
	fst_parser.add_argument('--model', help = 'Model to use', type = str, required = True)

	# Fst arguments
	fst_methods = ['hudson', 'wc']
	fst_parser.add_argument('--fst-method', metavar = metavarList(fst_methods), help = 'Fst method to use', type = str, choices = fst_methods, default = 'wc')

	# Output arguments
	fst_parser.add_argument('--out-prefix', help = 'Output prefix for Fst files', type = str, default = 'out')
	fst_parser.add_argument('--out-dir', help = 'Output directory name', type = str, default = 'Fst_Output')

	# Other arguments
	fst_parser.add_argument('--overwrite', help = 'Overwrite previous output', action = 'store_true')

	return fst_parser.parse_args()

# Assign the arguments
fst_args = fstParser()

# Check for previous files, and overwrite if specified
if not fst_args.overwrite and os.path.isdir(fst_args.out_dir):
	raise Exception(f'Previous output found at: {fst_args.out_dir}. Please specify i) a different --out-dir or ii) use --overwrite')
elif fst_args.overwrite and os.path.isdir(fst_args.out_dir): 
	shutil.rmtree(fst_args.out_dir)

# Calculate Fst
fst_run = Plink2.usingModelFile(**vars(fst_args))
fst_run.calcFst(method = fst_args.fst_method)