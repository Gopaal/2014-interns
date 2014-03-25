import os
import datetime
from fnmatch import fnmatch
import mimetypes
from visual.File_handler_module import Fill_DataBase


root = '/home/labadmin/.sugar/default/datastore'

path_list = []
filtered_path_list = []


for path, subdirs, files in os.walk(root):
    for name in files:
	if mimetypes.guess_type(name) == (None, None):  		#file filter by mime type i.e only plain/text files(None, none)
		
		if 'checksums' not in path+'/'+name:
	            if 'index' not in path+'/'+name:
	        	if 'index_updated' not in path+'/'+name:
		    	    if 'version' not in path+'/'+name:
			        path_list.append((path+'/'+name)[0:42])	




for path in path_list:
	if path not in filtered_path_list:
		filtered_path_list.append(path)
		
for path in filtered_path_list:
	print path
	Fill_DataBase(path)
	





				

