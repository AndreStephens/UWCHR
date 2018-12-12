#datecheck.py

import os
import pandas as pd
from datetime import datetime
import json
import featherize # FIX
import join # FIX

inpath = '../../import/output'
outpath = '../clean/output'

# Create class to check dates

def checkdate(datestring):
"""
Boolean test if the object can be converted to Y/M/D or M/D/Y datetime format 
without raising a ValueError. Returns (True, date) tuple if true.
:param self: date string or integer in format YY(YY)MMDD. Also accepts 
'-' and '/' separators
"""

    dateformats = ['%Y-%m-%d', 
                    '%Y/%m/%d', 
                    '%Y%m%d', 
                    '%y-%m-%d', 
                    '%y/%m/%d',
					'%y%m%d',
					'%m-%d-%Y', 
                    '%m/%d/%Y', 
                    '%m%d%Y', 
                    '%m-%d-%y', 
                    '%m/%d/%y',
					'%m%d%y']
    
    start_range = datetime(1950, 1, 1)
    end_range = datetime(2000, 1, 1)

	result = dict(date = date, dateformat = list())
	
	for dateformat in dateformats:
		try:
			date = datetime.strptime(datestring, dateformat)
			range_test = DateCheck.start_range <= date <= DateCheck.end_range
			errmsg = 'Date string %s not in range Jan 1 1950 to Jan 1 2000 for dateformat %s'
			# print message if date format is outside of some range
			try:
        		assert range_test
			except AssertionError:
				print(errmsg % (date, dateformat))
        	result['dateformat'].append(dateformat)
    	except (ValueError, AssertionError):
    		continue
	
	return(result)