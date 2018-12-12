#
# :date: 2016-09-28
# :author: AStephens
# :maintainer: AS
# :copyright: GPL v2 or later
#
# SV-history/individual/CDHES-LE/canonical/src/Makefile
#

all: \
input/cdhes-le.csv.gz \
output/cdhes-le.csv.gz

input/cdhes-le.csv.gz: \
		../clean/output/cdhes-le.csv.gz
	cd input && ln -sf ../$< .

output/cdhes-le.csv.gz: \
		src/canonicalize.py \
		input/cdhes-le.csv.gz
	python $< \
		--input=input/cdhes-le.csv.gz \
		--perp_canon=hand/perps-canonical.csv \
		--date_canon=hand/dates_lookup.csv \
		--location_canon=hand/locations_lookup.csv \
		--viol_local=hand/violations_lookup.csv \
		--viol_canon=hand/viols-canonical.csv \
		--output=$@

# END.
