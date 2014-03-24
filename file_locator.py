import os
import datetime
from fnmatch import fnmatch
import mimetypes


	    




def file_all(root):

				
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
	



root = '/home/labadmin/.sugar/default/datastore'			#path to folders to search for files
pattern = "*.txt"
a = []
b = []
c = []
d = []

for path, subdirs, files in os.walk(root):
    for name in files:
	if mimetypes.guess_type(name) == (None, None):  		#file filter by mime type i.e only plain/text files(None, none)
		Actual_path = path+'/'+name
		a.append(Actual_path)

		

		

		
for count in a:
	if 'checksums' not in count:
	    if 'index' not in count:
	        if 'index_updated' not in count:
		    if 'version' not in count:
			b.append(count)		
compare_count = len(b)
print len(b)


for x in b:
	c.append(x[0:42])
	

for r in c:
	if r not in d:
		d.append(r)
		
for z in d:
	print z
	file_all(z)
	

i = 0	
for count in a:
	if "title" in count:
		i+=1
i/=2
print i
