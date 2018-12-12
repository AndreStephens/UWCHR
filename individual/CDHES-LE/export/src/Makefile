#
# :date: 2016-10-04
# :author: AStephens
# :maintainer: AS
# :copyright: GPL v2 or later
#
# SV-history/individual/CDHES-LE/export/src/Makefile
#

all: output/cdhes-le.csv.gz

input/cdhes-le.csv.gz: \
		../canonicalize/output/cdhes-le.csv.gz
	cd input && ln -sf ../$< .

output/cdhes-le.csv.gz: \
		src/export.py \
		input/cdhes-le.csv.gz
	python $< \
		--input=input/cdhes-le.csv.gz \
		--output=$@

# END.
