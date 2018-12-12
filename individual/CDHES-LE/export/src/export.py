#
# :date: 2016-09-28
# :author: AStephens
# :copyright: GPL v2 or later
#
# SV-history/individual/CDHES-LE/export/src/export.py
#

import argparse
import pandas as pd
import sys

if sys.version_info[0] < 3:
	raise "Must be using Python 3"

# Rename fields
columns = [
		('hashid',			None),
		('v_name',			'VCTNOM'),
		('v_age',			None),
		('v_sex',			None),
		('v_affiliation',	None),
		('n_type_raw',		'VIOL_NAME_ENG'),
		('n_type_en',		'n_canonical_en'),
		('n_type_es',		'n_canonical_es'),
		('n_lethal',		'n_lethal'),
		('n_year',			'year'),
		('n_month',			'month'),
		('n_day',			'day'),
		('n_date_raw',		'FSTR'),
		('n_municipality',	'municipality'),
		('n_department',	'department'),
		('n_geocode',		'geocode'),
		('n_location_raw',	'lugar_str'),
		('p_1_en',			'p_canonical_en'),
		('p_2_en',			None),
		('p_3_en',			None),
		('p_4_en',			None),
		('p_1_es',			'p_canonical_es'),
		('p_2_es',			None),
		('p_3_es',			None),
		('p_4_es',			None),
		('p_type_1_en',		'p_typ_en'),
		('p_type_2_en',		None),
		('p_type_3_en',		None),
		('p_type_4_en',		None),
		('p_type_1_es',	'p_typ_es'),
		('p_type_2_es',	None),
		('p_type_3_es',	None),
		('p_type_4_es',	None),
		('p_raw',			None),
		('s_source',		'EXPNUM'), 
		('s_name',			None)
	]

columns_canon = [x for x,y in columns]


def _get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("--input", required=True)
	parser.add_argument("--output", required=True)
	return parser.parse_args()


if __name__ == "__main__":
	args = _get_args()
	print(args)
	
	# Rename fields to canon
	cdhes_le = pd.read_csv(args.input, sep="|")
	columns_dict = {y:x for x,y in columns if y}
	cdhes_le.rename(columns=columns_dict, inplace=True)

	cdhes_le.reindex(columns=columns_canon)
    
	# Add null columns to match canon
	cdhes_le['v_age'] = None
	cdhes_le['v_sex'] = None
	cdhes_le['v_affiliation'] = None
	cdhes_le['p_2_en'] = None
	cdhes_le['p_3_en'] = None
	cdhes_le['p_4_en'] = None
	cdhes_le['p_2_es'] = None
	cdhes_le['p_3_es'] = None
	cdhes_le['p_4_es'] = None
	cdhes_le['p_type_2_en'] = None
	cdhes_le['p_type_3_en'] = None
	cdhes_le['p_type_4_en'] = None
	cdhes_le['p_type_2_es'] = None
	cdhes_le['p_type_3_es'] =	None
	cdhes_le['p_type_4_es'] =	None

	# Add reference for source
	cdhes_le['s_name'] = 'CDHES-LE'

	# Drop non-canonical columns
	cdhes_le = cdhes_le[columns_canon]

	print(cdhes_le.info())

	cdhes_le.to_csv(args.output, sep="|", 
			compression='gzip', index=False)

# END.

