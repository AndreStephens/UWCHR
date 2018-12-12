output/rescate-canonical.csv: \
		src/Rescate-canonical.R \
		src/canonicalization-functions.R \
		input/rescate-merged.csv \
		input/dept.csv \
		input/vtypus.csv \
		input/el-salvador-geocodes-cleaned.csv
	Rscript $< \
		--functions=src/canonicalization-functions.R \
		--rescate=input/rescate-merged.csv \
		--dept=input/dept.csv \
		--vtypus=input/vtypus.csv \
		--geocodes=input/el-salvador-geocodes-cleaned.csv \
		--output=output/rescate-canonical.csv

all: output/rescate-canonical.csv
