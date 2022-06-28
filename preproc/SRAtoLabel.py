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
        conversionlist[line[1]] = line[2]

for name in onlyfiles:
    if(name.__contains__("_2"))or name=="SRR_Acc_List.txt":
        continue
    oldname = os.path.join(filespath, name)
    #oldsra = name[0:-8]
    if conversionlist.get(name):
        newname = os.path.join(filespath, conversionlist.get(name)) #+ ".fastq")
        os.rename(oldname,newname)
