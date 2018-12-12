#verifyfile.py

# add parametre for verifying all files or just db files
def verify_file_exists(dbfn): 
        try:
            file = os.readlink(dbfn)
            if file == '/dev/null' or \
              re.match(r'pipe:\[\d+\]',file) or \
              re.match(r'socket:\[\d+\]',file) or \ # check if file is open
	        re.match(r'.csv',file) or \ # check if file is extension FIX THIS -- CSV OR FEATHER?
	        dbfn in os.dir(inpath): 
                file = None
        except OSError as err:
            if err.errno == 2:     
                file = None
            else:
                raise(err) 
                
        yield (filename)
