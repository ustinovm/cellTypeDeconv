import numpy as np
import pandas as pd
import sys
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

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
rndperm = np.random.permutation(mat.shape[0])

pca = PCA(n_components=4)
pca_result = pca.fit_transform(mat)

mat['pca-one'] = pca_result[:, 0]
mat['pca-two'] = pca_result[:, 1]
mat['pca-three'] = pca_result[:, 2]
mat['pca-four'] = pca_result[:, 3]
print('Explained variation per principal component: {}'.format(pca.explained_variance_ratio_))

plt.figure(figsize=(16, 10))
sns.scatterplot(
    x="pca-two", y="pca-three",
    palette=sns.color_palette("hls", len(set(labelslist))),
    data=mat,
    legend="full",
    hue=labelslist
)
plt.show()
