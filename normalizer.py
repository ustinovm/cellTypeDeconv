import os
import sys
import pandas as pd

matrix_path = sys.argv[1]
lineNum_path = sys.argv[2]

d = {}
with open(lineNum_path) as f:
    for line in f:
        (num, file) = line.split(" ")
        d[file[9:-7]] = int(num) / 2
f.close()

mat = pd.read_csv(matrix_path, sep="\t")
for (colname, coldata) in mat.iteritems():
    realname = colname[0:-11]
    if d.get(realname) and realname != "":
        readnumber = d.get(realname)
        mat[colname] = (mat[colname] / readnumber)*1000000

mat.to_csv("10X_P7_11_normalized.tsv", sep="\t")
