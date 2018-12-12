# Project Description

The project cleans, standardizes and combines historical 
databases on human rights violationsin El Salvador 
between 1975 and 1993. 

The following databases were used:

- **Rescate**: Based on Tutela Legal denuncias, independent work
- **CDHES-LE**: contains Individual victim depositions
- **United Nations**: Comision de la Verdad (direct sources)
- **United Nations**: Comision de la Verdad (indirect sources)
- **SJC**:
<br><br>

*This project is a collaboration of the University of Washington 
Center for Human Rights (UWCHR) and the 
Human Rights Data Analysis Group (HRDAG).*
<br><br><br>

# Project Artitecture and Workflow

## Project Directories
These are relative to `SV-history/`

* `individual/`: contains the individual databases
* `multiple/`: contains databases that have been merged for analysis (naming convention db1+db2.ext); PB comment: this category level is **unnecessary**. To concat all the files together, use `compare/CDHES-le+Rescate+UN+UN-indirect/import`
* `match/`: to deduplicate all the violations
* `compare/`: to compare (usually for descriptive purposes) raw datasets to each other: how many detentions does CDHES-le contain vs how many in Rescate?
* `analyse/`: contains analyses and results for various models
* `write/`: contains files used for writing reports, papers, etc. (usually in LaTeX)

## Database Directories
* `{database_name}/`: directory for a given database
* `share/`: files that are commonly used across databases

## Task Directories
These are a good typical list but vary by category. Each task is explained in a README file.

* `import/`: convert database file format to csv
* `merge/`: link tables together using matching unique keys
* `clean/`: fix systematic and ideosyncratic value errors
* `canonicalize/`: recode values in a column to some standard set for consistency within and across databases, particularly for dates, locations, violations and perpetrators
* `export/`: write versions of database, renaming columns for consistency across databases and dropping unnessary columns, based on specific needs

## Taskflow Directories
* `input/`: contains raw import files or symlinks of file outputs from a previous task directory
* `src/`: contains scripts and Makefile
* `output/`: contains output files generated from `src/`
* `hand/`: contains files or symlinks with data created by hand or using notebooks, typically csv tables that pair raw values and corresponding canonical values for dates, locations, violations and perpetrators
* `note/`: contains Jupyter notebooks that test code, help generate files for hand or explain the logic of complex cleaning tasks
* `frozen/`: contains input files that have been modified by hand to correct issues that are not fixed with code; where they exist, they should be used in place of files in `input/`
* `doc/`: contains documentation

