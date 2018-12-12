#
# :date: 2016-12-09
# :author: AStephens
# :copyright: GPL v2 or later
#
# SV-history/individual/Rescate/export/src/export.py
#

import argparse
import pandas as pd
import sys

if sys.version_info[0] < 3:
	raise "Must be using Python 3"

# Rename fields
columns = [
		('v_name',			'fullname'),
		('v_age',			'AGE'),
		('v_sex',			'SEX'),
		('v_affiliation',	'AFFILIATIO'),
		('n_type_raw',		'n_str'),
		('n_type_en',		'n_canonical_en'),
		('n_type_es',		'n_canonical_es'),
		('n_lethal',		'n_lethal'),
		('n_year',			'year'),
		('n_month',			'month'),
		('n_day',			'day'),
		('n_date_raw',		'VIOLATION_'),
		('n_municipality',	'municipality'),
		('n_department',	'Deptname'),
		('n_geocode',		'geocode'),
		('n_location_raw',	'TOWN_CITY'),
		('p_1_en',			'p_canonical_en_1'),
		('p_1_es',			'p_canonical_es_1'),    
		('p_type_1_en',		'p_typ_en_1'),
		('p_type_1_es',		'p_typ_es_1'),
		('p_2_en',			'p_canonical_en_2'),
		('p_2_es',			'p_canonical_es_2'),
		('p_type_2_en',		'p_typ_en_2'),
		('p_type_2_es',		'p_typ_es_2'),
		('p_3_en',			'p_canonical_en_3'),
		('p_3_es',			'p_canonical_es_3'),
		('p_type_3_en',		'p_typ_en_3'),
		('p_type_3_es',		'p_typ_es_3'),
		('p_4_en',			'p_canonical_en_4'),
		('p_4_es',			'p_canonical_es_4'),
		('p_type_4_en',		'p_typ_en_4'),
		('p_type_4_es',		'p_typ_es_4'),
		('p_raw',			None),
		('s_source',		None),
		('s_name',			None),
		('hashid',			'hashid'),
	]

columns_canon = [x for x, y in columns]

## FUNCTIONS
def concat(strs):
	strs = [s for s in strs if s]
	if strs:
		return strs

def _get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("--input", required=True)
	parser.add_argument("--output", required=True)
	return parser.parse_args()

if __name__ == "__main__":
	args = _get_args()
	print(args)
	
	rescate = pd.read_csv(args.input, sep="|")

	columns_dict = {y:x for x,y in columns if y}
	rescate.rename(columns=columns_dict, inplace=True)

	# Add combined raw perps
	perps_raw = rescate[['p_raw_1',	'p_raw_2',
								'p_raw_3', 'p_raw_4']]
	perps_raw = perps_raw.fillna("")
	rescate['p_raw'] = perps_raw.apply(lambda r: concat(r), 
												axis=1)

	# Drop non-canonical columns 
	rescate = rescate[columns_canon]

	# Fix column index
	rescate.reindex(columns=columns_canon)

	print(rescate.info())
	rescate.to_csv(args.output, sep="|", 
			compression='gzip', index=False)

# END.