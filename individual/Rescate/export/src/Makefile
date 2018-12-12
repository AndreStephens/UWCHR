#
# :date: 2016-12-09
# :author: AStephens
# :maintainer: AS
# :copyright: GPL v2 or later
#
# SV-history/individual/Rescate/export/src/Makefile
#

all: \
input/rescate.csv.gz \
output/rescate.csv.gz

input/rescate.csv.gz: \
		../canonicalize/output/rescate.csv.gz
	cd input && ln -sf ../$< .

output/rescate.csv.gz: \
		src/export.py \
		input/rescate.csv.gz
	python $< \
		--input=input/rescate.csv.gz \
		--output=$@

# END.
