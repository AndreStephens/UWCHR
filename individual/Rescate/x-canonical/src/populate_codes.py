#populate_codes.py

import os
import pandas as pd
import feather as ft # IMPORT FEATHERIZE FUNCTION
import json
import re # CONDITIONAL

def populate(dbfn, ctinfofn):
    """
    Doc
    """
    inpath = '../../import/output/'
    outpath = '../../canonical/doc/' # CHANGE!!!!
    # !!! WANT TO CHECK IF FILE EXISTS THEN RUN SCRIPT TO GENERATE FILE IF NOT

    def verify_file_exists(dbfn): # DONT KNOW THAT WE NEED TO DO THIS!!
        try:
            file = os.readlink(dbfn)
            if file == '/dev/null' or \
              re.match(r'pipe:\[\d+\]',file) or \
              re.match(r'socket:\[\d+\]',file) or \ # check if file is open
	      re.match(r'.csv',file) or \ # check if file is extension FIX THIS -- CSV OR FEATHER?
	      dbfn in os.dir(inpath): # check if file is in directory -- FIX THIS // INVERT THESE STEPS
                file = None
        except OSError as err:
            if err.errno == 2:     
                file = None
            else:
                raise(err) # SHOULD IGNORE RATHER THAN ASSERT ERROR
                
        yield (filename)


    def join(*paths): # SEPARATE SCRIPT???
        full_path = os.path.join(*paths)
        return(full_path)
        
    ctdct_path = '../../codebook/doc/' # DECIDE IF THIS IS APPROPRIATE DIRECTORY
    ctdct_filename = os.path.join(ct_path, ctinfofn)
    
    with open(ctinfofn) as file:
        ctinfo_dcts = json.load(file)

    ctfn_lst = list() # To store names of constituent tables
    ctdf_lst = list() # To store constituent tables dataframes
    
    for ctinfo_dct in ctinfo_dcts:
        ctfn = os.path.join(ctinfo_dct['table_name'], '.csv') 
        ctfn_lst.append(ctfn) # DO YOU NEED THIS -ANDRE
        ct_infile = os.path.join(inpath, ctfn)
        ct_outfile = outpath + ctfn.strip(".csv") + ".fthr"
        ctdf = featherize(ct_infile, ct_outfile)
        ctdf_lst.append(ctdf) # list of constituent dataframes
	
    infile = join(inpath, dbfn)
    outfile = join(outpath, str(dbfn).replace('.csv', '.fthr')) # FIGURE OUT EXTENSION QUESTION
    dbdf = featherize(infile, outfile) # create feather file
    dbcn_lst = list(dbdf.columns) # get list of database columns
    dbnrow = dbdf.shape[0] # get row length for database
    
    # Check database column name against matching constituent table column...
    # ... then if positive match, store list of database and list of constituent table values
    for dbcn in dbcn_lst:
        for i, ctinfo_dct in enumerate(ctinfo_dcts):
            ctcn_ctinfo = ctinfo_dct['col_name'] # Matching columns may have different names in constituent table and database
            dbfn_ctinfo = join(ctinfo_dct['db_name'], ".csv")
            if dbfn_ctinfo != dbfn or / # match database file name with name in constituent tables info dictionary
                dbcn != ctcn_ctinfo: # match column names
                continue
            ctdf = ctdf_lst[i] # get relevant constituent table dataframe
            ctrefcol = ctdf[ctdf.columns[0]] # get reference values list from constituent table 
            ctfullcol = ctdf[ctdf.columns[1]] # this assumes 1st column is reference code and second is full value CHECK ASSUMPTION
            dbrefcol = dbdf[dbcn] # get database column with all values
            dbfullcol = [None]*dbnrow # create new empty list to store matched full values
            for j, dbrefval in enumerate(dbrefcol):
                if pd.isnull(dbrefval): # pd.isnull(obj) tests if value is either None or NaN
                    dbfullcol[j] == None # return empty cell in full column if reference column cell is empty (redundant)
                    continue
                for k, ctrefval in enumerate(ctrefcol):
                    if pd.isnull(ctrefval): 
                        continue # ignore empty cells in constituent table reference column 
                    if isinstance(ctrefval, float):
                        ctrefval = int(ctrefval) # values convert differently to string depending on whether float or integer
                    if isinstance(dbrefval, float):
                        dbrefval = int(dbrefval)
                    if str(dbrefval).lower() == str(ctrefval).lower(): # case insensitive
                        ctfullval = ctfullcol[k]
                        dbfullcol[j] = ctfullval
                errvars = (ctdf.columns[0], ctinfo_dct['table_name'] + ".csv", dbcn, dbfn)
                errmsg = "Did not find a reference-value match for %s>%s and %s>%s" % errvars
                rule = dbfullcol[j] is not None
                assert rule, errmsg
                
            dbrefcn = dbcn
            dbfullcn = dbrefcn + "_MATCHED"
            dbcn_lst = list(dbdf.columns) # The column index will get updated with each successful loop
            dbfullcn_index = dbcn_lst.index(dbcn) + 1 # Index number where matched column will be inserted
            dbdf.insert(dbfullcn_index, dbfullcn, dbfullcol)
            msgvars = (dbfullcn, dbfn, ctdf.columns[0], ctinfo_dct['table_name'] + ".csv", dbcn, dbfn)
            print("Inserted %s column in %s based on %s>%s and %s>%s match" % msgvars)
            
    return({'database': dbdf, 'db_name': dbfn}) # returns a dictionary with database dataframe and database name 
