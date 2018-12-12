#
# :date: 2016-08-09
# :author: PB
# :maintainer: PB, AS
# :copyright: GPL v2 or later
#
# SV-history/individual/Rescate/canonicalize/src/Makefile
#

all: \
input/rescate.csv.gz \
input/vtypus.csv \
input/vtyp.csv \
hand/dept.csv \
hand/perps-canonical.csv \
hand/viols-canonical.csv \
output/rescate.csv.gz

input/rescate.csv.gz: \
		../clean/output/rescate.csv.gz
	cd input && ln -sf ../$< .

input/vtypus.csv: \
		../import/output/vtypus.csv
	cd input && ln -sf ../$< .

input/vtyp.csv: \
		../import/output/vtyp.csv
	cd input && ln -sf ../$< .

hand/dept.csv: \
		../../share/hand/dept.csv
	cd input && ln -sf ../$< .

hand/perps-canonical.csv: \
		../../share/hand/perps-canonical.csv
	cd input && ln -sf ../$< 

hand/viols-canonical.csv: \
		../../share/hand/viols-canonical.csv
	cd input && ln -sf ../$< .

output/rescate.csv.gz: \
		src/canonicalize.py \
		input/rescate.csv.gz 
	python $< \
		--input=input/rescate.csv.gz \
		--dept=hand/dept.csv \
		--vtype_eng=input/vtypus.csv \
		--vtype_esp=input/vtyp.csv \
		--viol_canon=hand/viols-canonical.csv \
		--perps=hand/perps-canonical.csv \
		--locations=hand/locations_lookup.csv \
		--output=$@

# end.
