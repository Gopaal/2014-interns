import os
import datetime
from fnmatch import fnmatch
import mimetypes
import re
import os

RE_WORD = re.compile(r'\b[a-zA-Z]+\b')
keywords = frozenset(['data', 'preview'])



def is_empty(fpath):  
    return True if os.path.isfile(fpath) and os.path.getsize(fpath) > 0 else False
	    
class Fill_DataBase():

    def __init__(self, root):
        Path_holder = []
	for path, subdirs, files in os.walk(root):
    	    for name in files:
	        if mimetypes.guess_type(name) == (None, None):
		    Path_holder.append( path+'/'+name)
		    
	for count in Path_holder:	   
	    for word in RE_WORD.findall(count):
                if word in keywords:
                    Path_holder.remove(count)
                    continue
					
	WriteFile = open('datastore.txt',"a")
	WriteFile.write("\n")
	WriteFile.write("{")
 	for count in Path_holder:
	    print count
		
	    Read_File = open(count,"r")
	    if 'timestamp' in count:
		timestamp = (datetime.datetime.fromtimestamp(int(Read_File.read())).strftime('%Y-%m-%d %H:%M:%S'))
		WriteFile.write(count[89:120])
		WriteFile.write(":")
		WriteFile.write (timestamp)
		WriteFile.write(", ")
	    elif 'creation_time' in count:
		timestamp = (datetime.datetime.fromtimestamp(int(Read_File.read())).strftime('%Y-%m-%d %H:%M:%S'))
		WriteFile.write(count[89:120])
		WriteFile.write(":")
		WriteFile.write (timestamp)
		WriteFile.write(", ")
	    else:
		if(not(is_empty(count))):
		   WriteFile.write(count[89:120])
		   WriteFile.write(": null, ")
		else:
		   other_data = Read_File.read()
		   WriteFile.write(count[89:120])
		   WriteFile.write(":")
		   WriteFile.write (other_data)
		   WriteFile.write(", ")
		   Read_File.close()
	
	WriteFile.write("}")
	WriteFile.close()
        
	

