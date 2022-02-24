import sys
import os
import pandas as pd
import numpy as np
from collections import OrderedDict
from numpy import mean
from numpy import std
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import RandomOverSampler

from collections import Counter

matrix_path = sys.argv[1]

mat = pd.read_csv(matrix_path, sep="\t")#, index_col="0")  # indexcol evtl entfenen für single matrices...
mat = mat.iloc[:, 1:]  # delete first column bc it was just numbers
mat = mat.swapaxes(1, 0, False)
mat = mat.set_axis(mat.iloc[0], axis=1, inplace=False)
mat = mat.iloc[1:, :]

# for column in mat:
#    if "AAAAAAAAAAAAA" in column:
#        del mat[column]

mat = mat[mat.columns.drop(list(mat.filter(regex='AAAAAAAAAAAAA')))]

labels = mat.index.to_series()
labelslist = labels.str.split("_").str[4:-1].str.join(" ")
labelslist = labelslist.tolist()
labelset = sorted(list(set(labelslist)))
labelset.remove("leukocyte")
mat = mat.rename(index=lambda x: " ".join(x.split("_")[4:-1]))
coun = OrderedDict(sorted(Counter(mat.index.values).items()))


mat = mat.drop(index="leukocyte")


mat = mat.sort_index()
matt = mat.groupby(by=mat.index, axis=0).groups

# i = 0
# for key, val in coun:
#    if (val < 50):
#        mat.drop(key)
#    else:
#        mat = mat.iloc[val - 50:val, :]
#        i= i + val - 50
rus = RandomOverSampler(random_state=432)
X_res, y_res = rus.fit_resample(mat, mat.index)
X_train, X_test, y_train, y_test = train_test_split(mat[mat.columns], mat.index, test_size=0.5, stratify=mat.index,
                                                    random_state=123456)
X_train, y_train = rus.fit_resample(X_train, y_train)
X_test, y_test = rus.fit_resample(X_test, y_test)

rf = RandomForestClassifier(n_estimators=100, oob_score=True, random_state=123456)
rf.fit(X_train, y_train)

predicted = rf.predict(X_test.values)
accuracy = accuracy_score(y_test, predicted)
print(f'Out-of-bag score estimate: {rf.oob_score_:.3}')
print(f'Mean accuracy score: {accuracy:.3}')

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# print(Counter(X_test.index.values))
conf_mat = confusion_matrix(y_test, predicted, labels=labelset, normalize='true')
cm = pd.DataFrame(conf_mat, index=labelset, columns=labelset)
# cm = cm * 100
cm.index.name = 'True Label'
cm.columns.name = 'Predicted Label'
print(conf_mat)

import seaborn

fig, ax = plt.subplots(figsize=(18,10))
ax.tick_params(labelsize=15)
sett = list(set(labelslist))
seaborn.set_context("poster")

seaborn.heatmap(cm
                # / np.sum(conf_mat)
                , fmt='.1%', ax=ax, annot=True, xticklabels=labelset, yticklabels=labelset, cmap="Blues",annot_kws={"size": 20}
                )
plt.xlabel('Predicted Label', fontsize=18)
plt.ylabel('True Label', fontsize=18)
plt.tight_layout()

plt.savefig("10X_P7_8_labeled_confmat_test.png")
plt.show()

