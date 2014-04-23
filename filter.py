import os
import datetime
from fnmatch import fnmatch
import mimetypes
import re
import subprocess


RE_WORD = re.compile(r'\b[a-zA-Z]+\b')
keywords = frozenset(['data', 'preview'])

column_holder = []
Path_holder = []
title_list = []


def is_empty(fpath):  
    return True if os.path.isfile(fpath) and os.path.getsize(fpath) > 0 else False
	    

def Get_titles_list(root):
        
	for path, subdirs, files in os.walk(root):
    	    for name in files:
	        if mimetypes.guess_type(name) == (None, None):
		    Path_holder.append( path+'/'+name)
		    
		    
	for count in Path_holder:	   
	    for word in RE_WORD.findall(count):
                if word in keywords:
                    Path_holder.remove(count)
                    continue
		    
		    
		    
	WriteFile = open('datastore.txt',"w+")
	#WriteFile.write("\n")
	#WriteFile.write("{")
 	for count in Path_holder:
	    #print count
		
	    Read_File = open(count,"r")
	    if 'title_set_by_user' in count:
		continue
	    elif "title" in count:
	        file_data = Read_File.read()
		title_list.append(file_data)
		if file_data not in column_holder:
		    column_holder.append(file_data)
	    else:
	        continue
	    Read_File.close()
        WriteFile.close()
	#Activity_count()
	return column_holder
	
def Activity_count():
	write1=open('filteredtext.txt',"w+")
	for x in column_holder:
	    print x  +','+ str(title_list.count(x))
	    #write1.write( x  +','+ str(title_list.count(x)))
    
    
    
j =Get_titles_list('/home/labadmin/.sugar/default/datastore')


