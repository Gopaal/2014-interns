import os
import datetime
from fnmatch import fnmatch
import mimetypes



root = '/home/labadmin/.sugar/default/datastore/43'			
pattern = "*.txt"
a = []
b = []

for path, subdirs, files in os.walk(root):
    for name in files:
	if mimetypes.guess_type(name) == (None, None): 
		z = path+'/'+name 					
		a.append(z)
		b.append(name)
		
file2 = open('jason.txt', "a")
file2.write("\n")
file2.write("{")

for count in a:
	print count
	file = open(count,"r")
	if 'timestamp' in count:
		timestamp = (datetime.datetime.fromtimestamp(int(file.read())).strftime('%Y-%m-%d %H:%M:%S'))
		file2.write (timestamp)
		file2.write(", ")
	elif 'creation_time' in count:
		timestamp = (datetime.datetime.fromtimestamp(int(file.read())).strftime('%Y-%m-%d %H:%M:%S'))
		file2.write (timestamp)
		file2.write(", ")
	other_data = file.read()
	file2.write (other_data)
	file2.write(", ")
	file.close()
	
file2.write("}")	
file2.close()
	
	



#if 'timestamp' in b:
#	print (datetime.datetime.fromtimestamp(int(file.read())).strftime('%Y-%m-%d %H:%M:%S'))
					





		
		

