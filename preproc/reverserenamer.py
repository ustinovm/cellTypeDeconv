from os import listdir
import os
from os.path import isfile, join
import sys
import csv

filespath = sys.argv[1]
indexpath = sys.argv[2]
onlyfiles = [f for f in listdir(filespath) if isfile(join(filespath, f))]

conversionlist = {}
with open(indexpath) as file:
    indexfile = csv.reader(file, delimiter="\t")
    for line in indexfile:
        if line[0] == "":
            continue
        conversionlist[line[2]] = line[1]

for name in onlyfiles:
    oldname = os.path.join(filespath, name)
    oldsra = name[0:-6]
    print(oldsra)
    print(conversionlist.get(oldsra))
    if conversionlist.get(oldsra):
        newname = os.path.join(filespath, conversionlist.get(oldsra))
        os.rename(oldname,newname)
