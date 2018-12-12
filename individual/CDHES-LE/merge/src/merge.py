#
# :date: 2016-09-15
# :author: AStephens
# :maintainer: AStephens
# :copyright: GPL v2 or later
#
# SV-history/individual/CDHES-LE/merge-and-flatten/src/merge.py
#

import argparse
import sys
import pandas as pd
import re
import hashlib

if sys.version_info[0] != 3:
	raise "Oops! Must be using Python 3"

def get_digits(s):
	return re.findall(r'\d+', str(s))

def _get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("--d1980", required=True)
	parser.add_argument("--d1981", required=True)
	parser.add_argument("--d1982", required=True)
	parser.add_argument("--d1983", required=True)
	parser.add_argument("--d1984", required=True)
	parser.add_argument("--d1985", required=True)
	parser.add_argument("--d1986", required=True)
	parser.add_argument("--d1987", required=True)
	parser.add_argument("--d1988", required=True)
	parser.add_argument("--d1989", required=True)
	parser.add_argument("--d1990", required=True)
	parser.add_argument("--d1991", required=True)
	parser.add_argument("--d1992", required=True)
	parser.add_argument("--output", required=True)
	return parser.parse_args()

def make_hashid(row):
	try:
		s = ''.join([str(getattr(row, f)) for f in columns_canon])
	except:
		print(row)
		raise
	b = bytearray("cdhes-le{}".format(s), encoding='utf8')
	h = hashlib.sha1()
	h.update(b)
	return h.hexdigest()

if __name__ == "__main__":

	args = _get_args()
	print(args)

	d1980 = pd.read_csv(args.d1980, sep='|')
	d1981 = pd.read_csv(args.d1981, sep='|')
	d1982 = pd.read_csv(args.d1982, sep='|')
	d1983 = pd.read_csv(args.d1983, sep='|')
	d1984 = pd.read_csv(args.d1984, sep='|')
	d1985 = pd.read_csv(args.d1985, sep='|')
	d1986 = pd.read_csv(args.d1986, sep='|')
	d1987 = pd.read_csv(args.d1987, sep='|')
	d1988 = pd.read_csv(args.d1988, sep='|')
	d1989 = pd.read_csv(args.d1989, sep='|')
	d1990 = pd.read_csv(args.d1990, sep='|')
	d1991 = pd.read_csv(args.d1991, sep='|')
	d1992 = pd.read_csv(args.d1992, sep='|')

	dataframes = [d1980, d1981, d1982, d1983, d1984, d1985,	d1986, 
					d1987, d1988, d1989, d1990, d1991, d1992]
	cdhes_le = pd.concat(dataframes, ignore_index=True)

	# extract violation numbers into list
	# then arrange as stack
	vstack = cdhes_le['VLST'].apply(get_digits)
	vstack = vstack.apply(pd.Series, 1).stack()
	vstack.index = vstack.index.droplevel(-1)
	vstack.name = 'violation_number'

	cdhes_le = cdhes_le.join(vstack) # duplicates rows for each violation

	# Add hashid
	columns_canon = cdhes_le.columns
	cdhes_le['hashid'] = cdhes_le.apply(make_hashid, axis=1)
    
	#FIXME: Unsure why row lengths are different
	#assert len(stack) == len(cdhes_le)

	cdhes_le.to_csv(args.output, index=False, 
				sep="|", compression='gzip')

### END.