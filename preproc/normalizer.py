import os
import sys
import pandas as pd

matrix_path = sys.argv[1]
lineNum_path = sys.argv[2]

d = {}
with open(lineNum_path) as f:
    for line in f:
        (num, file) = line.split(" ")
        d[file[18:-7].strip()] = (int(num) / 4) #fastq with every fourth line containing 100BP
        print(file[18:-7])
f.close()

mat = pd.read_csv(matrix_path, sep="\t")
print("matrix has been read")
for (colname, coldata) in mat.iteritems():
    realname = colname[0:-11]
    print(realname)
    if d.get(realname) and realname != "":
        print("normalizing: " + realname)
        readnumber = d.get(realname)
        mat[colname] = (mat[colname] / readnumber)*1000000

mat.to_csv(matrix_path[0:-4]+"_reallynormalized.tsv", sep="\t")
