Title: README.md  
Author: AS, PN  
Date:   2016.05.31  
Afflilation: UWCHR  

# ReadMe 

Scripts and their tasks in `Rescate/../src` and running log of issues.

## Scripts

### A. `read.py`, `csv2csv.py`, `dbf.py`
1. converts Xbase DBF files to csv

### B. `clean.py`
1. drop records without victim name
2. drop sensitive data
3. write report with descriptive stats of dropped records

### C. `merge.py`
1. join tables with information on violations, victim, incident, and perpetrator on unique key
2. TODO: explain pivot

### D. `canonicalize.py`
1. split violation date string by year, month, day in rescate df
2. merge violations column from `vtypes.csv` on `vytpcode`; merge canonical violations on local violations
3. add canonical columns for perp1... perp4
5. merge dept, municipality, geocode columns from locations_lookup.csv (See `canonical/note/canonicalize_locations.ipynb)
6. drop a number of unneeded fields

### E. `export.py`
* add source field to identify database
* concatenate raw perps column into single column string
* rename fields based on canonical names 
 - canonical fields are the common set of fields that will be used for joining all databases; they are outlined in listed in `individual/share/doc/canonical-fieldnames.md`
* create empty columns for canonical fields that not in this database 
* drop columns that are not canonical
* TODO: move hash id creation to earlier task

## Issues log

### Merging Rescate violations with military
Merging rescate violations with rescate military tables is something we should see about eventually. We would likely first want one merged file for military as we have for violations. The challenge here is that each record in rescate.csv (violations) is a victim-violation unit of analysis which has up to four perps. **To normalise both tables, we would need to either treat the victim-violation-perp as the unit or have repeated mililary columns corresponding to perp1 to perp4.**
