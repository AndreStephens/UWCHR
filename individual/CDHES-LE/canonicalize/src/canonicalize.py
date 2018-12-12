#
# :date: 2016-09-28
# :author: AStephens
# :copyright: GPL v2 or later
#
# SV-history/individual/CDHES-LE/canonical/src/canonicalize.py
#
# See `hand` and `note` for explanation of how fields were 
# canonicalised and important assumptions made while doing so.

import argparse
import pandas as pd
import sys

if sys.version_info[0] < 3:
	raise "Must be using Python 3"

def _get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("--input", required=True)
	parser.add_argument("--perp_canon", required=True)
	parser.add_argument("--date_canon", required=True)
	parser.add_argument("--location_canon", required=True)
	parser.add_argument("--viol_local", required=True)
	parser.add_argument("--viol_canon", required=True)
	parser.add_argument("--output", required=True)
	return parser.parse_args()

if __name__ == "__main__":
	args = _get_args()
	print(args)
	
	cdhes_le = pd.read_csv(args.input, sep="|")
	pre_nrows = len(cdhes_le)

	date_canon = pd.read_csv(args.date_canon, sep="|")

	viol_local = pd.read_csv(args.viol_local, sep="|")
	viol_canon = pd.read_csv(args.viol_canon, sep="|")
	viol_canon = viol_canon[viol_canon.dataset=='cdhes-le']

	location_canon = pd.read_csv(args.location_canon, sep="|")

	perp_canon = pd.read_csv(args.perp_canon, sep="|")
	perp_canon = perp_canon[perp_canon.dataset=='cdhes-le']


	## ADD PERPS
	cdhes_le = pd.merge(cdhes_le, perp_canon, how='left', 
			left_on='HSTR', right_on='p_raw')

	## DATES
	# See details in `note\canonicalize_dates.ipynb`.
	date_canon = date_canon.drop_duplicates('FSTR')
	cdhes_le = pd.merge(cdhes_le, date_canon, how='left',
				left_on='FSTR', right_on='FSTR')

	#Fix bad year    
	cdhes_le[cdhes_le.year > 1992] = None

	## VIOLATIONS
	# lookup local violations
	viol_local.VIOL_NUM = viol_local.VIOL_NUM.apply(float)
	cdhes_le = pd.merge(cdhes_le, viol_local, how='left',
				left_on='violation_number', right_on='VIOL_NUM')
	# canonicalize violations
	cdhes_le = pd.merge(cdhes_le, viol_canon, how='left',
				left_on='VIOL_NAME_ENG', right_on='n_str')
	del cdhes_le['n_str']

	## LOCATIONS
	# See details in `note\canonicalize_locations.ipynb`
	location_canon.geocode = location_canon.geocode.map(
		lambda x: '{}00'.format(str(int(x))) if int(x) else x) 
	cdhes_le = pd.merge(cdhes_le, location_canon, how='left',
				left_on='LUGAR', right_on='lugar_str')

	post_nrows = len(cdhes_le)
	assert pre_nrows == post_nrows, "Oops! Script changed row length. Check merges."

	cdhes_le = cdhes_le.dropna(axis=0, how='all')
    
	print(cdhes_le.info())
	## OUTPUT
	cdhes_le.to_csv(args.output, sep="|", 
				compression='gzip', index=False)

# END.