from os import listdir
import os
from os.path import isfile, join
import sys
import subprocess
import csv


filespath = sys.argv[1]
onlyfiles = [f for f in listdir(filespath) if isfile(join(filespath, f))]


for name in onlyfiles:
    oldname = os.path.join(filespath, name)
    if(name.__contains__("_2")):
        tosearch = (name.split("_")[0])
        #tosearch=str(tosearch)+".txt"
        tosearchfull=os.path.join(filespath,tosearch)
        if(onlyfiles.__contains__(tosearch)):
            print(name)
            os.system("cat " + oldname + " >> "+tosearchfull)
            #subprocess.check_call("cat " + oldname + " >> "+tosearchfull)
    #oldsra = name[0:-8]
    #print(oldsra)
    #if conversionlist.get(oldsra):
        #newname = os.path.join(filespath, conversionlist.get(oldsra))
        #os.rename(oldname,newname)
