import sys
import os
import pandas as pd
import numpy as np
import math
from collections import OrderedDict
from collections import Counter
from numpy import mean
from numpy import std
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline


matrix_path = sys.argv[1]
preproc = sys.argv[2]

# mat = mat.iloc[:, 1:]  # delete first column bc it was just numbers
# mat = mat.swapaxes(1, 0, False)
# mat = mat.set_axis(mat.iloc[0], axis=1, inplace=False)
# mat = mat.iloc[1:, :]
# mat = mat.rename(columns = lambda x: x.strip("smartseq_"))
# for column in mat:
#    if "AAAAAAAAAAAAA" in column:
#        del mat[column]
if preproc == "t":
    mat = pd.read_csv(matrix_path, sep="\t", low_memory=True, index_col=0)  # indexcol evtl entfenen für single matrices...
    mat = mat.swapaxes(1, 0, False)
    mat = mat.set_axis(mat.iloc[0], axis=1, inplace=False)
    mat = mat.iloc[1:, :]
    mat = mat.rename(index=lambda x: " ".join(x.split("_")[1:-2]))
if preproc == "f":
    mat = pd.read_csv(matrix_path, sep="\t", low_memory=True,
                      index_col=0)  # indexcol evtl entfenen für single matrices...
mat = mat[mat.columns.drop(list(mat.filter(regex='AAAAAAAAAAAA')))]

labels = mat.index.to_series()
'''
labelslist = labels.str.split("_").str[1:-2].str.join(" ")
labelslist = labelslist.tolist()
'''
labelslist = labels.tolist()
labelset = sorted(list(set(labelslist)))
# labelset.remove("leukocyte")
'''
mat = mat.rename(index=lambda x: " ".join(x.split("_")[1:-2]))
'''
coun = OrderedDict(sorted(Counter(mat.index.values).items()))
print(coun)

for key, val in coun.items():
    if val < 100:
        mat = mat.drop(index=key)
        labelset.remove(key)
'''
#this code snippet removes low variance features
summed = {}
for name in labelset:
    if name is not '':
        lilmat = mat.loc[name]
        colsum = lilmat.sum(axis=0)
        summed[name] = colsum/coun.get(name)
sumOfCols = pd.DataFrame(summed)
variance = sumOfCols.var(axis=1)
# highest = variance.nsmallest(int(math.sqrt(len(variance))))
smallestVars = variance.where(variance < 100)
smallestVars = smallestVars.dropna()
smallestVarsIndices = smallestVars.index.tolist()
print("number of features before filtering: ", len(variance))
print("number of features after filtering: ", len(variance) - len(smallestVarsIndices))

mat = mat.drop(columns=smallestVarsIndices)
#mat.to_csv(matrix_path[:-4] + "_filtered.tsv", sep="\t")
'''

#mat = mat.sort_index()  # .astype(np.uint8)
#mat = mat.groupby(by=mat.index, axis=0).groups

# i = 0
# for key, val in coun:
#    if (val < 50):
#        mat.drop(key)
#    else:
#        mat = mat.iloc[val - 50:val, :]
#        i= i + val - 50

majorities = {}
minorities = {}
coun = OrderedDict(sorted(Counter(mat.index.values).items()))

for key, val in coun.items():
    if (val < 200):
        minorities[key] = 300
    if val > 200:
        majorities[key] = 300

smote = SMOTE(sampling_strategy=minorities)
rus = RandomUnderSampler()
steps = [('o', smote), ('u', rus)]
pipeline = Pipeline(steps=steps)

#X_res, y_res = pipeline.fit_resample(mat, mat.index)
X_train, X_test, y_train, y_test = train_test_split(mat[mat.columns], mat.index, test_size=0.2, stratify=mat.index,
                                                    random_state=123555)
X_train, y_train = pipeline.fit_resample(X_train, y_train)
X_test, y_test = rus.fit_resample(X_test, y_test)

rf = RandomForestClassifier(n_estimators=100, oob_score=True, random_state=12553)
rf.fit(X_train, y_train)

predicted = rf.predict(X_test.values)
accuracy = accuracy_score(y_test, predicted)
print(f'Out-of-bag score estimate: {rf.oob_score_:.3}')
print(f'Mean accuracy score: {accuracy:.3}')
print('Number of features: ' + str(len(mat.columns)))
'''
# Feature importance:

# Get numerical feature importances
all_importants = list(rf.feature_importances_)
# List of tuples with variable and importance
feat_importances = [(feat, round(imp, 20)) for feat, imp in zip(mat.columns, all_importants)]
# Sort the feature importances by most important first
feat_importances = sorted(feat_importances, key=lambda x: x[1], reverse=True)

goodones = []
highest = max(rf.feature_importances_)
lowend = highest / 200
# summarize feature importance
# TODO: was mach ich mit den goodones ? alle anderen raus?
for entry in feat_importances:
    if entry[1] > lowend:
        goodones.append(entry[0])
#    print('Feature: %0d, Score: %.5f' % (i, v))
print(len(goodones))
print(len(feat_importances))
mat = mat[goodones]
print(len(mat.columns))
mat.to_csv(matrix_path[:-4] + "onlyMostImportant_div200.tsv", sep="\t")
# #plt = feat_importances.nlargest(15).plot(kind='barh')
# figure.savefig(matrix_path[0:-4] + "_features.png", bbox_inches="tight")
# plot feature importance
# plt.savefig(matrix_path[0:-4] + "_features.png", bbox_inches="tight")
# plt.close()

'''
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# print(Counter(X_test.index.values))
# conf_mat = confusion_matrix(y_test, predicted, labels=labelset, normalize='true')
conf_mat = confusion_matrix(y_test, predicted, labels=labelset)
cm = pd.DataFrame(conf_mat, index=labelset, columns=labelset)
# cm = cm * 100
cm.index.name = 'True Label'
cm.columns.name = 'Predicted Label'
print(conf_mat)

import seaborn

fig, ax = plt.subplots(figsize=(18, 16))
ax.tick_params(labelsize=15)
sett = list(set(labelslist))
# seaborn.set_context("poster")

seaborn.heatmap(cm
                # / np.sum(conf_mat)
                , fmt='.0f',
                ax=ax,
                annot=True,
                xticklabels=labelset, yticklabels=labelset, cmap="Blues",
                annot_kws={"size": 20}
                )
plt.xlabel(f'Predicted Label \n\nOut-of-bag score estimate:{rf.oob_score_:.3} \nNumber of features:{str(len(mat.columns))} \nNumber of input samples:{str(len(mat.index))}', fontsize=18)
plt.ylabel('True Label', fontsize=18)
# plt.tight_layout()
classrep = classification_report(y_test, predicted)#, output_dict=True)
#classrepdf = pd.DataFrame(classrep).transpose()
#classrepdf.to_csv(matrix_path[0:-4] + "classification_report_smote_rus.tsv",sep="\t")

with open(matrix_path[0:-4] + "_classification_report_smote_rus.txt", "w") as classrepfile:
    classrepfile.write(classrep)
    classrepfile.close()


plt.savefig(matrix_path[0:-4] + "_confmat_abs_tight_smote_rus.png", bbox_inches="tight")
plt.show()
plt.close()
