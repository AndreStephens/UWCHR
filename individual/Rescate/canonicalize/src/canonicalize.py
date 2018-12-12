#
# :date: 2016-08-09
# :author: PB
# :maintainer: PB, AS
# :copyright: GPL v2 or later
#
# SV-history/individual/Rescate/canonical/src/canonicalize.py
#
#
import argparse
import pandas as pd
import sys

if sys.version_info[0] < 3:
	raise "Must be using Python 3"


def _get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("--input", required=True)
	parser.add_argument("--dept", required=True)
	parser.add_argument("--locations", required=True)
	parser.add_argument("--vtype_eng", required=True)
	parser.add_argument("--vtype_esp", required=True)
	parser.add_argument("--viol_canon", required=True)
	parser.add_argument("--perps", required=True)
	parser.add_argument("--output", required=True)
	return parser.parse_args()


if __name__ == "__main__":

	args = _get_args()
	print(args)

	# GET DATAFRAME OBJECTS
	rescate = pd.read_csv(args.input, sep="|")
	pre_nrows = len(rescate) # to check later if merge done properly

 	# See `canonical/note/canonicalize_locations.ipynb
 	# for explanation about how locations csv was made.
	locations = pd.read_csv(args.locations, sep='|')

	vtype_eng = pd.read_csv(args.vtype_eng, sep="|")
	vtype_esp = pd.read_csv(args.vtype_esp, sep="|")

	viol_canon = pd.read_csv(args.viol_canon, sep="|")
	viol_canon = viol_canon[viol_canon.dataset=="rescate"]

	perps = pd.read_csv(args.perps, sep="|")
	perps = perps[perps.dataset=='rescate']

    # stdize violations to the names rather than codes
	## VIOLATIONS
	# combine local viols in spanish and english and merge onto rescate
	vtypes = pd.merge(vtype_eng, vtype_esp, on='Vtypcode,A,2')
	vtypes = vtypes[['Vtypcode,A,2', 'Name,A,40_x', 'Name,A,40_y']]
	rescate = pd.merge(rescate, vtypes, how='left',
				       left_on='VTYPCODE', right_on='Vtypcode,A,2')
	rescate.rename(columns={'Name,A,40_x': 'violation_eng',
							'Name,A,40_y': 'violation_esp',}, 
							inplace=True)
	rescate.drop(['Vtypcode,A,2'], axis=1, inplace=True)
 
 	# add canonical violations from `share/hand`
	rescate = pd.merge(rescate, viol_canon, how='left',
						left_on='violation_esp', right_on='n_str')

 	## LOCATIONS
    # Need to clear 'NAN' outputs for municipality
	locations['municipality'] = locations.muni.map(lambda x: str(x).upper())
	# pad geocodes with trailing zeros to follow canon
	locations['geocode'] = locations.geo.map(
		lambda x: '{}00'.format(str(int(x)) if pd.notnull(x) else x))
	locations.drop(['dept2', 'muni', 'geo'], axis=1, inplace=True)
	# merge with canonicalized locations in `hand`
	rescate = pd.merge(rescate, locations, on=['DEPTCODE', 'TOWN_CITY'], how='left')

	## PERPS
	# canoncalise perps
	perps1 = perps.copy()
	perps2 = perps.copy()
	perps3 = perps.copy()
	perps4 = perps.copy()

	perps1.columns = ['{}_1'.format(col) for col in perps.columns]
	perps2.columns = ['{}_2'.format(col) for col in perps.columns]
	perps3.columns = ['{}_3'.format(col) for col in perps.columns]
	perps4.columns = ['{}_4'.format(col) for col in perps.columns]

	rescate = pd.merge(rescate, perps1, left_on='perp1', right_on='p_raw_1', 
		how='left')
	rescate = pd.merge(rescate, perps2, left_on='perp2', right_on='p_raw_2', 
		how='left')
	rescate = pd.merge(rescate, perps3, left_on='perp3', right_on='p_raw_3', 
		how='left')
	rescate = pd.merge(rescate, perps4, left_on='perp4', right_on='p_raw_4', 
		how='left')

	# NAMES
	rescate.rename(columns={'VICTIM_NAM': 'fullname'}, inplace=True)

	drop_fields = ['INCDCODE', 'VIOLCODE', 'VICTCODE', 'SITE', 'JURISDICTI',
			   	'VICTIM_COU', 'KILLED_COU', 'WOUNDED_CO', 'IS_PROPERT', 'DETAINED',
			  	'POSITION', 'AGRPCODE', 'KW', 'SGRPCODE', 'SGRP_DESCR', 'key',
       			'COLLCODE', 'OPERCODE', 'ENTRY_DATE', 'CHANGE_DAT', 'CHANGE_TIM',
				'INCIDENT_D', 'INCDDATEEX', 'BOOKCODE', 'PAGE_REFER', 'TESTIMONY',
       			'IS_CITE', 'IS_INCD', 'IS_PROB', 'BOOK_NAME', 'PUBLCODE']
	rescate.drop(drop_fields, axis=1, inplace=True)

	post_nrows = len(rescate)
	assert pre_nrows == post_nrows, "Oops! Script changed row length. Check merges."

	print(rescate.info())
	rescate.to_csv(args.output, sep="|", compression='gzip', index=False)

# end.
