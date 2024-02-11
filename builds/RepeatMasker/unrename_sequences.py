#!/usr/bin/env python3
DESCRIPTION = '''
Replace given short names of sequences in fasta/gff file using a provided from/to name file.

E.g.,
Seq000000000001    ==>    species_name_scaffold_000001_length100000_cov1.25155
Seq000000000002    ==>    species_name_scaffold_000002_length100_cov105.2611
...

This script was primairly developed to account for the ~50 character sequence header limit
imposed by some of the tools used by RepeatMasker.
This script was designed to give sequences in the fasta/gff file produced by RepeatMasker their
original/long names back (after being renamed by the rename_sequences.py script).

'''
import sys
import os
import argparse
import logging
import gzip

## Pass arguments.
def main():
	## Pass command line arguments. 
	parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=DESCRIPTION)
	parser.add_argument('-i', '--input', metavar='genome.fa', 
		required=False, default=sys.stdin, type=lambda x: File(x, 'r'), 
		help='Input [gzip] fasta file with sequence to rename (default: stdin)'
	)
	parser.add_argument('-o', '--output', metavar='genome.renamed.fa', 
		required=False, default=sys.stdout, type=lambda x: File(x, 'w'), 
		help='Output [gzip] fasta file with renamed sequences (default: stdout)'
	)
	parser.add_argument('-f', '--fromto', metavar='genome.fromto.txt', 
		required=True, type=argparse.FileType('r'), 
		help='Output file with from-to sequence names (default: %(default)s)'
	)
	parser.add_argument('-t', '--filetype', 
		required=False, default='fasta', type=str,
		choices=['fasta', 'gff'],
		help='Type of file being renamed (default: %(default)s)'
	)
	parser.add_argument('--debug', 
		required=False, action='store_true', 
		help='Print DEBUG info (default: %(default)s)'
	)
	args = parser.parse_args()
	
	## Set up basic debugger
	logFormat = "[%(levelname)s]: %(message)s"
	logging.basicConfig(format=logFormat, stream=sys.stderr, level=logging.INFO)
	if args.debug:
		logging.getLogger().setLevel(logging.DEBUG)
	
	logging.debug('%s', args) ## DEBUG
	
	file_type=args.filetype
	
	# Load old->new seq names
	fromtodict = {}
	with args.fromto as fromtofile:
		for line in fromtofile:
			line = line.strip('\n')
			# Ignore bank or comment lines
			if line.startswith('#') or not line:
				continue
			# Ignore lines without 2 columns
			line_split = line.split('\t')
			if len(line_split) == 2:
				fromtodict[line_split[1]] = line_split[0]
	
	# Loop over input file and rename depending on file type
	with args.input as infile, args.output as outfile:
		if file_type == 'fasta':
			for line in infile:
				line = line.strip('\n')
				if line.startswith('>'):
					new_seq_name = line.lstrip('>').split(' ')[0]
					try:
						old_seq_name = fromtodict[new_seq_name]
					except KeyError:
						logging.error('Sequence name "%s" not in from/to file!', new_seq_name)
						sys.exit(1)
					outfile.write('>'+old_seq_name+'\n')
				else:
					outfile.write(line+'\n')
		else: #gff
			for line in infile:
				line = line.strip('\n')
				# If line is not comment and not blank
				if not line.startswith('#') and line:
					line_split = line.split('\t')
					try:
						line_split[0] = fromtodict[line_split[0]]
					except KeyError:
						logging.error('Sequence name "%s" not in from/to file!', line_split[0])
						sys.exit(1)
					outfile.write('\t'.join(line_split)+'\n')
				else:
					outfile.write(line+'\n')


class File(object):
	'''
	Context Manager class for opening stdin/stdout/normal/gzip files.

	 - Will check that file exists if mode='r'
	 - Will open using either normal open() or gzip.open() if *.gz extension detected.
	 - Designed to be handled by a 'with' statement (other wise __enter__() method wont 
	    be run and the file handle wont be returned)
	
	NOTE:
		- Can't use .close() directly on this class unless you uncomment the close() method
		- Can't use this class with a 'for' loop unless you uncomment the __iter__() method
			- In this case you should also uncomment the close() method as a 'for'
			   loop does not automatically cloase files, so you will have to do this 
			   manually.
		- __iter__() and close() are commented out by default as it is better to use a 'with' 
		   statement instead as it will automatically close files when finished/an exception 
		   occures. 
		- Without __iter__() and close() this object will return an error when directly closed 
		   or you attempt to use it with a 'for' loop. This is to force the use of a 'with' 
		   statement instead. 
	
	Code based off of context manager tutorial from: https://book.pythontips.com/en/latest/context_managers.html
	'''
	def __init__(self, file_name, mode):
		## Upon initializing class open file (using gzip if needed)
		self.file_name = file_name
		self.mode = mode
		
		## Check file exists if mode='r'
		if not os.path.exists(self.file_name) and mode == 'r':
			raise argparse.ArgumentTypeError("The file %s does not exist!" % self.file_name)
	
		## Open with gzip if it has the *.gz extension, else open normally (including stdin)
		try:
			if self.file_name.endswith(".gz"):
				#print "Opening gzip compressed file (mode: %s): %s" % (self.mode, self.file_name) ## DEBUG
				self.file_obj = gzip.open(self.file_name, self.mode+'b')
			else:
				#print "Opening normal file (mode: %s): %s" % (self.mode, self.file_name) ## DEBUG
				self.file_obj = open(self.file_name, self.mode)
		except IOError as e:
			raise argparse.ArgumentTypeError('%s' % e)
	def __enter__(self):
		## Run When 'with' statement uses this class.
		#print "__enter__: %s" % (self.file_name) ## DEBUG
		return self.file_obj
	def __exit__(self, type, value, traceback):
		## Run when 'with' statement is done with object. Either because file has been exhausted, we are done writing, or an error has been encountered.
		#print "__exit__: %s" % (self.file_name) ## DEBUG
		self.file_obj.close()
#	def __iter__(self):
#		## iter method need for class to work with 'for' loops
#		#print "__iter__: %s" % (self.file_name) ## DEBUG
#		return self.file_obj
#	def close(self):
#		## method to call .close() directly on object.
#		#print "close: %s" % (self.file_name) ## DEBUG
#		self.file_obj.close()


if __name__ == '__main__':
	main()
