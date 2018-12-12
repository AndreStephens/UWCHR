# :date: 2017-01-12
# :author: PN
# :path: SV-history/individual/rescate/clean/src/Makefile
#
# the following creates symlinks for files in ../../merge/output/
# to files in ../input/
# and runs script src/clean.py
#
# call it from the clean/ directory with
#   $ make -f src/Makefile
#
all: \
	input/rescate.csv.gz \
	output/rescate.csv.gz
    
input/rescate.csv.gz: \
		../merge/output/rescate.csv.gz
	cd input && ln -sf ../$< .

output/rescate.csv.gz: \
		src/clean.py \
		input/rescate.csv.gz
	python $< \
		--rescate=input/rescate.csv.gz \
		--output=$@