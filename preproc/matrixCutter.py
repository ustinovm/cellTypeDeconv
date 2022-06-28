import os
import sys
import pandas as pd
import numpy as np
from collections import OrderedDict
from collections import Counter

matrix_path = sys.argv[1]
lineNum_path = sys.argv[2]

d = {}
with open(lineNum_path) as f:
    for line in f:
        (num, file) = line.split(" ")
        d[file[18:].strip()] = (int(num) / 4) *100
f.close()
print("trying to read matrix")
mat = pd.read_csv(matrix_path, sep="\t", index_col=0)
print("matrix has been read, commencing normalization")
for colname in mat:
    realname = colname[0:-11]
    if d.get(realname) and realname != "":
        readnumber = d.get(realname)
        mat[colname] = (mat[colname] / readnumber) * 1000000
print("matrix has been normalized")
mat = mat.swapaxes(1, 0, False)
mat = mat.rename(index=lambda x: " ".join(x.split("_")[1:-1]))
labels = mat.index.to_series()
labelslist = labels.str.split(" ").str[:-1].str.join(" ")
labelslist = labelslist.tolist()
labelset = sorted(list(set(labelslist)))
coun = Counter(labelslist)
print(coun)

for key, val in coun.items():
    if val < 100:
        mat = mat[~mat.index.str.contains("^" + key + "\s\d", regex=True)]
print("matrix has been cut")
labels = mat.index.to_series()
labelslist = labels.str.split(" ").str[:-1].str.join(" ")
labelslist = labelslist.tolist()
labelset = sorted(list(set(labelslist)))
coun = Counter(labelslist)
print(coun)

summed = {}
# meanOfCols = pd.DataFrame({}, columns=labelset)
# standardDev = pd.DataFrame({}, columns=labelset)  # spaget
meanOfCols = {}
standardDev = {}
for name in labelset:
    if name is not '':
        lilmat = mat[mat.index.str.contains("^" + name + "\s\d", regex=True)]
        colsum = lilmat.sum(axis=0)
        standardDev[name] = lilmat.std(ddof=0)
        meanOfCols[name] = colsum / coun[name]
        standardDev[name] = standardDev[name] / meanOfCols[name] * 100
meanOfCols = pd.DataFrame(meanOfCols, columns = labelset)
standardDev = pd.DataFrame(standardDev, columns=labelset)
avCoefOfVariation = standardDev.sum(axis=1) / len(labelset)
# highest = variance.nsmallest(int(math.sqrt(len(variance))))
smallestVars = avCoefOfVariation.where(avCoefOfVariation < 90)
smallestVars = smallestVars.dropna()
smallestVarsIndices = smallestVars.index.tolist()
print("number of features before filtering: ")
print("number of features to drop: ", len(smallestVarsIndices))

mat = mat.drop(columns=smallestVarsIndices)

mat.to_csv(matrix_path[0:-4] + "_cut_normalized.tsv", sep="\t")
