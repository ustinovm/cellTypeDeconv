import sys
import pandas as pd
from collections import OrderedDict


from collections import Counter

matrix_path = sys.argv[1]

mat = pd.read_csv(matrix_path, sep="\t")  # , index_col="0")  # indexcol evtl entfenen für single matrices...
mat = mat.swapaxes(1, 0, False)
mat = mat.set_axis(mat.iloc[0], axis=1, inplace=False)
mat = mat.iloc[1:, :]
# mat = mat.rename(columns = lambda x: x.strip("smartseq_"))


# mat = mat[mat.columns.drop(list(mat.filter(regex='AAAAAAAAAAAA')))]

labels = mat.index.to_series()
labelslist = labels.str.split("_").str[1:-2].str.join(" ")
labelslist = labelslist.tolist()
labelset = sorted(list(set(labelslist)))
mat = mat.rename(index=lambda x: " ".join(x.split("_")[1:-1]))
indexdict = {}
coun = OrderedDict(sorted(Counter(mat.index.values).items()))
print(coun)
for key,val in coun.items():
    val = key.split(" ")[0:-1]
    indexdict[key] = ' '.join(key.split(" ")[0:-1])

indicesdf=pd.DataFrame([indexdict])
indicesdf.to_csv(matrix_path[:-4]+'_indexed.tsv',sep="\t")
occurences = dict(Counter(indexdict.values()))
todrop = []
for key,val in occurences.items():
    if key!="":
        if val<100:
            todrop.append(key)
            mat = mat[~mat.index.str.startswith(key)]

''''
#mat= mat[~mat.index.str.startswith(todrop)]
for key, val in coun.items():
    if val < 100:
        if(key!=""):
            #mat = mat.drop(index=key)
            mat = mat.loc[:,~mat.columns.str.startswith(key)]
            if(labelset.__contains__(key.split(" ")[0:-1])):
                labelset.remove(key.split(" ")[0:-1])
'''
summed = {}
for name in labelset:
    if (name is not '') and not todrop.__contains__(name):
        #lilmat = mat.loc[name]
        lilmat = mat[mat.index.str.startswith(name)]
        colsum = lilmat.sum(axis=0)
        summed[name] = colsum
sumOfCols = pd.DataFrame(summed)
variance = sumOfCols.var(axis=1)
smallestVars = variance.where(variance < 10)
smallestVars = smallestVars.dropna()
smallestVarsIndices = smallestVars.index.tolist()
print("number of features before filtering: ", len(variance))
print("number of features after filtering: " , len(smallestVarsIndices))

mat = mat.drop(columns=smallestVarsIndices)
mat.to_csv(matrix_path[:-4] + "_filteredNames.tsv", sep="\t")
