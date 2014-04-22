import subprocess

cmd='python filter.py'

p1=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
w = open('fill.csv',"w+")

for line in iter(p1.stdout.readline,b''):
    w.write(line)



