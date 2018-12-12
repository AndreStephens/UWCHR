
Date: 2016-09-28
Author: AStephens
Maintainers: AStephens, PNeff  

`SV-history/individual/CDHES-LE/README.md`

# Read Me 

## Scripts

Scripts and their tasks in `CDHES-LE/../src` and running log of issues.

### A. `merge.py`
* combines tables from D1980.csv to D1992.csv
* splits single record with list of n violations int n records with single violation; this changes the data level from victim to victim-violation
* TODO: add hash id


### B. `clean.py`
* drop sensitive data
* write report with descriptive stats of dropped records

### C. `canonicalize.py`
* merges canonical perps on perp column 
 - **Assumption**: `HSTR` is perp column
* merges canonical dates table in `hand/` on `FSTR` 
 - **Assumption**: `FSTR` is violation date (see `canonical/note/canonicalize_dates.ipynb` for details on cleaning and cannibalization of dates)
* merges violations name on violations code
 - **Assumption**: We assume violation codes 1-15 match list order in PBall's publication. PBall is confident that this is correct.
* merges canonical violation name on local violation name
* merges locations on `LUGAR`
 - See `note\canonicalize_locations.ipynb` for details on canonicalization


### D. `export.py`
* add source field to identify database
* rename fields based on canonical names 
 - canonical fields are the common set of fields that will be used for joining all databases; they are outlined in listed in `individual/share/doc/canonical-fieldnames.md`
* create empty columns for canonical fields that not in this database 
* drop columns that are not canonical
* TODO: move hash id creation to merge task

## Issues/Bugs

*None flagged.*