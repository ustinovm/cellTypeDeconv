import numpy as np
import pandas as pd
import sys
import os
from collections import OrderedDict
from collections import Counter
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns


print(np.__version__)
print(os.environ)


matrix_path = sys.argv[1]

dirpath = "./" + matrix_path[:-4] + "_figures"
try:
    os.mkdir(dirpath)
except OSError as error:
    print(error)

mat = pd.read_csv(matrix_path, sep="\t", index_col=0,low_memory=True)  # indexcol evtl entfenen für single matrices...
# mat = mat.iloc[:, 1:]  # delete first column bc it was just numbers
mat = mat.swapaxes(1, 0, False)
mat = mat.set_axis(mat.iloc[0], axis=1, inplace=False)
mat = mat.iloc[1:, :]

# mat = mat.rename(index=lambda x: " ".join(x.split("_")[1:-2]))

# mat = mat[mat.columns.drop(list(mat.filter(regex='AAAAAAAAAAAAA')))]
mat = mat.rename(index=lambda x: " ".join(x.split("_")[1:-2]))
labels = mat.index.to_series()
# labelslist = labels.str.split("_").str[4:-1].str.join(" ")
labelslist = labels.tolist()
labelset = sorted(list(set(labelslist)))
#rndperm = np.random.permutation(mat.shape[0])

coun = OrderedDict(sorted(Counter(mat.index.values).items()))
print(coun)

for key, val in coun.items():
    if val < 100:
        mat = mat.drop(index=key)
        labelset.remove(key)

labels = mat.index.to_series()
# labelslist = labels.str.split("_").str[4:-1].str.join(" ")
labelslist = labels.tolist()


pca = PCA(n_components=7)
pca_result = pca.fit_transform(mat)

mat['pca-one'] = pca_result[:, 0]
mat['pca-two'] = pca_result[:, 1]
mat['pca-three'] = pca_result[:, 2]
mat['pca-four'] = pca_result[:, 3]
mat['pca-five'] = pca_result[:, 4]
mat['pca-six'] = pca_result[:, 5]
mat['pca-seven'] = pca_result[:, 6]

print('Explained variation per principal component: {}'.format(pca.explained_variance_ratio_))
pcax = ''
pcay = ''
for i in range(1, 7):
    if i == 1:
        pcax = 'pca-one'
    elif i == 2:
        pcax = 'pca-two'
    elif i == 3:
        pcax = 'pca-three'
    elif i == 4:
        pcax = 'pca-four'
    elif i == 5:
        pcax = 'pca-five'
    elif i == 6:
        pcax = 'pca-six'
    elif i == 7:
        pcax = 'pca-seven'
    for j in range(2, 7):
        if j == 2:
            pcay = 'pca-two'
        elif j == 3:
            pcay = 'pca-three'
        elif j == 4:
            pcay = 'pca-four'
        elif j == 5:
            pcay = 'pca-five'
        elif j == 6:
            pcay = 'pca-six'
        elif j == 7:
            pcay = 'pca-seven'
        if pcax != pcay:
            plt.figure(figsize=(26, 10))
            sns.set_context("poster")
            b = sns.scatterplot(
                x=pcax, y=pcay,
                palette=sns.color_palette("hls", len(labelset)),
                data=mat,
                #legend="full",
                hue=labelslist,
            )
            b.set_xlabel(pcax+": "+str(round(pca.explained_variance_ratio_[i],8))+" of variance")
            b.set_ylabel(pcay+": "+str(round(pca.explained_variance_ratio_[j],8))+" of variance")
            b.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
            plt.savefig(dirpath + "/" + matrix_path[0:-4] + pcax + pcay + ".png", bbox_inches="tight")

            plt.show()
            plt.close()
