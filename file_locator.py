import os
from fnmatch import fnmatch
import mimetypes

root = '/home/labadmin/.sugar/default/datastore/43'
pattern = "*.txt"
a = []
b = []

for path, subdirs, files in os.walk(root):
    for name in files:
	if mimetypes.guess_type(name) == (None, None):
		a.append(path)
		b.append(name)
		print path, name
	"""
        if fnmatch(name, pattern):
            print os.path.join(path, name)
	    a.append(name)
	"""
	    
print "\n \n"
print a[3], b[3]
	    
#for v in a:
#	print " value: ", v

