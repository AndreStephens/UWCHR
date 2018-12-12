"""if all match, then open dbdf and add properly formatted column
else produce error report and spit out mssg"""

import os
import pandas as pd
import featherize 
import datecheck
import join 

inpath = '../../import/output' # Check
outpath = '../../clean/output'

def adddate(dbfn, report = True):
    infile = join(inpath, dbfn)
    dbdf = featherize(infile)
    for col in dbdf:
        dateformatted_col = list()
        inconsistent_msg = list()
        for row_i, val in enumerate(col):
            try:
                result = datecheck(val)
            except AssertionError: 
                continue # Ignore dateformat failed match
            matched_dateformat = result['dateformat']
            if len(matched_dateformat) > 1:
                errvars = (val, col, row_i, matched_dateformat)
                errmsg = 'Value %s in column %s row %d matches the following formats' % errvars
                print(errmsg)
            if row_i = 1:
                continue
            consistent_format_condition = matched_dateformat == last_dateformat
            constitent_format_msg = 'Warning: Inconsistent dateformat for row %d in column %s' % (row_i, col)
            try:
                assert consistent_format_condition, consistent_format_msg
            except AssertionError:
                inconsistent_msg.append(i_row)
            
 ## JUST DO TH COLUMNS
            
            last_dateformat = matched_dateformat
        
        if inconsistent, print #some matched others didn't, verify
    
for table in db_dict['database']:
    table_msg = "Checked " + table['table_name'] + "\n"
    print(table_msg)
    f.write(table_msg) # python will convert \n to os.linesep

    for column in table['table']:
        col_msg = "...Checking " + column['column_name'] + "\n"
        f.write(col_msg) # python will convert \n to os.linesep
        #print(col_msg)
        col_len = 0
        ymd_date_counter = 0
        ymd_false_val_list = list()
        ymd_true_val_list = list()
        #
        mdy_date_counter = 0
        mdy_false_val_list = list()
        mdy_true_val_list = list()
        #
        for value in column['values']:
            if value[0] == 'Non': #CHANGE
                continue
            else:
                col_len = col_len + 1
                
                if value[1]['ymd_check'][0] == True:
                    ymd_date_counter = ymd_date_counter + 1
                    ymd_true_val_list.append(value[0])
                else:
                    ymd_false_val_list.append(value[0])
                    
                if value[1]['mdy_check'][0] == True:
                    mdy_date_counter = mdy_date_counter + 1
                    mdy_true_val_list.append(value[0])
                else:
                    mdy_false_val_list.append(value[0])
                    
        ymd_percent_true = ymd_date_counter/col_len
        mdy_percent_true = mdy_date_counter/col_len
        
        if ymd_percent_true == 0:
            ymd_msg = "......Failed: No true YMD date format returned" + "\n"
        elif ymd_percent_true == 1:
            ymd_true_col_list.append(table['table_name'] + " >> " + column['column_name'])
            ymd_msg = "......Success: All true YMD date formats" + "\n"
        elif 0 < ymd_percent_true <= 0.5: 
            ymd_msg = "Inconsistent YMD: Values returned as False, EXCEPT: " + str(ymd_true_val_list) + "\n"
        else:
            ymd_msg = "Inconsistent YMD: Value returned as True, EXCEPT: " + str(ymd_false_val_list) + "\n"
            ymd_inconsistent_col_list.append(table['table_name'] + " >> " + column['column_name'])
        f.write(ymd_msg)
        
        if mdy_percent_true == 0:
            mdy_msg = "......Failed: No true MDY date format returned" + "\n"
        elif mdy_percent_true == 1:
            mdy_true_col_list.append(table['table_name'] + " >> " + column['column_name'])
            mdy_msg = "......Success: All true MDY date formats" + "\n"
        elif 0 < ymd_percent_true <= 0.5: 
            mdy_msg = "Inconsistent MDY: Values returned as False, EXCEPT: " + str(mdy_true_val_list) + "\n"
        else:
            mdy_msg = "Inconsistent MDY: Value returned as True, EXCEPT: " + str(mdy_false_val_list) + "\n"
            mdy_inconsistent_col_list.append(table['table_name'] + " >> " + column['column_name'])
        f.write(mdy_msg) 

sum_ymd_msg = "\nSUMMARY:\n" + "the following fields are TRUE dates in format... :\n" + str(ymd_true_col_list) + "\n" + "the following have either false positives or true negatives & need to be checked:\n" + str(ymd_inconsistent_col_list) + "\n"
f.write(sum_ymd_msg)

sum_mdy_msg = "\nSUMMARY:\n" + "the following fields are TRUE dates in format... :\n" + str(mdy_true_col_list) + "\n" + "the following have either false positives or true negatives & need to be checked:\n" + str(mdy_inconsistent_col_list) + "\n"
f.write(sum_mdy_msg)

f.close()