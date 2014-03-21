import os
from fnmatch import fnmatch

root = '/home/labadmin'
pattern = "*.txt"
a = []

for path, subdirs, files in os.walk(root):
    for name in files:
        if fnmatch(name, pattern):
            print os.path.join(path, name)
	    a.append(path)
	    
	    
for v in a:
	print " value: ", v
