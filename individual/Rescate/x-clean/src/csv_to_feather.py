#csv_to_feather.py

import os
import sys
import pandas as pd
import feather as fthr
import join_pathstrings.py # CHECK

def featherize(dbfn, inpath, outpath, sep="|", encoding ="latin-1"):
    """
    Reads a csv file into a Pandas DataFrame and returns a feather-formatted file.
    :param dbfn: name of .csv file (will also be name of .fthr file when created)
    :type dbfn: str
    :param infile: directory where csv file is located
    :type infile: str
    :param outpath: target directory for feather file
    :type outfile: str
    :param sep: delimiter/separator of csv file columns (defaults to '/')
    :type sep: str
    :param encoding: character encoding type (defaults to 'latin-1')
    :type encoding: str
    """
    
    infile = join(inpath, dbfn)
    outfile = join(outpath, dbfn)
    # read csv as pandas dataframe
    dataframe_pd = pd.read_csv(infile, sep, encoding)
    
    # MAKE THIS OPTIONAL
    # write as feather-formatted file 
    #fthr.write_dataframe(dataframe_pd, outfile)
    #return fthr.read_dataframe(outfile)


if __name__ == '__main__':
    'Usage: python <dbfn> <inpath> <outpath> <sep> <encoding>'
    dbfn = sys.argv[1]
    inpath = sys.argv[2]
    outpath = sys.argv[3]
    
    if len(sys.argv) == 4:
        featherize(dbfn, inpath, outpath)
    elif len(sys.argv) == 5:
        sep = sys.argv[4]
        featherize(dbfn, inpath, outpath, sep)
    else:
        sep = sys.argv[4]
        encoding = sys.argv[5]
        featherize(dbfn, inpath, outpath, sep, encoding)