#
# :date: 2016.09.15
# :author: AStephens
# :path: SV-history/individual/CDHES-LE/import/src/Makefile
#
#
# call it from the import/ directory with
# $ make -f src/Makefile
#

all: output/cdhes-le.csv.gz

output/cdhes-le.csv.gz: \
		src/merge.py \
		input/D1980.csv \
		input/D1981.csv \
		input/D1982.csv \
		input/D1983.csv \
		input/D1984.csv \
		input/D1985.csv \
		input/D1986.csv \
		input/D1987.csv \
		input/D1988.csv \
		input/D1989.csv \
		input/D1990.csv \
		input/D1991.csv \
		input/D1992.csv
	python $< \
		--d1980=input/D1980.csv \
		--d1981=input/D1981.csv \
		--d1982=input/D1982.csv \
		--d1983=input/D1983.csv \
		--d1984=input/D1984.csv \
		--d1985=input/D1985.csv \
		--d1986=input/D1986.csv \
		--d1987=input/D1987.csv \
		--d1988=input/D1988.csv \
		--d1989=input/D1989.csv \
		--d1990=input/D1990.csv \
		--d1991=input/D1991.csv \
		--d1992=input/D1992.csv \
		--output=$@



#all: output/cdhes-le.csv.gz
#
# RESCATE-perps.csv comes from AHG's original work
#
#output/cdhes-le.csv.gz: \
#		src/merge.py \
#		input/VMRGD.csv
#	python $< \
#		--vmrgd=input/VMRGD.csv \
#		--output=$@
#
# END.

