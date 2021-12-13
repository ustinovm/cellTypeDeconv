import sys
import os
import pandas as pd
import numpy as np
from numpy import mean
from numpy import std
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
matrix_path = sys.argv[1]

mat = pd.read_csv(matrix_path, sep="\t")
mat = mat.iloc[:, 1:]  # delete first column bc it was just numbers
mat = mat.swapaxes(1, 0, False)
mat = mat.set_axis(mat.iloc[0], axis=1, inplace=False)
mat = mat.iloc[1:, :]


for column in mat:
    if "AAAAAAAAAAAAA" in column:
        del mat[column]

labels = mat.index.to_series()
labelslist = labels.str.split("_").str[4:-1].str.join(" ")
labelslist = labelslist.tolist()
mat = mat.rename(index=lambda x: " ".join(x.split("_")[4:-1]))
X_train, X_test, y_train, y_test = train_test_split(mat[mat.columns], mat.index, test_size=0.5, stratify=mat.index, random_state=123456)

rf = RandomForestClassifier(n_estimators=100, oob_score=True, random_state=123456)
rf.fit(X_train, y_train)

predicted = rf.predict(X_test)
accuracy = accuracy_score(y_test, predicted)
print(f'Out-of-bag score estimate: {rf.oob_score_:.3}')
print(f'Mean accuracy score: {accuracy:.3}')