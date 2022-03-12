import numpy as np
import pandas as pd
import sys
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

matrix_path = sys.argv[1]

mat = pd.read_csv(matrix_path, sep="\t")  # , index_col="0")  # indexcol evtl entfenen für single matrices...
mat = mat.iloc[:, 1:]  # delete first column bc it was just numbers
mat = mat.swapaxes(1, 0, False)
mat = mat.set_axis(mat.iloc[0], axis=1, inplace=False)
mat = mat.iloc[1:, :]

mat = mat.rename(index=lambda x: " ".join(x.split("_")[1:-2]))

# mat = mat.drop(index="leukocyte")
# mat = mat.drop(index="promonocyte")
# mat = mat.drop(index="granulocyte")
# mat = mat.drop(index="proerythroblast")
# mat = mat.drop(index="Fraction A pre-pro B cell")
# mat = mat.drop(index="hematopoietic precursor cell")
# mat = mat.drop(index="erythroblast")
# mat = mat.drop(index="late pro-B cell")
# mat = mat.drop(index="basophil")
# mat = mat.drop(index="alveolar macrophage")
# mat = mat.drop(index="early pro-B cell")
# mat = mat.drop(index="lung endothelial cell")
# mat = mat.drop(index="type II pneumocyte")
# mat = mat.drop(index="mast cell")
# mat = mat.drop(index="stromal cell")
# mat = mat.drop(index="myeloid cell")
# mat = mat.drop(index="granulocytopoietic cell")
# mat = mat.drop(index="ciliated columnar cell of tracheobronchial tree")

#for column in mat:
#   if "AAAAAAAAAAAAA" in column:
#        del mat[column]

mat = mat[mat.columns.drop(list(mat.filter(regex='AAAAAAAAAAAAA')))]

labels = mat.index.to_series()
# labelslist = labels.str.split("_").str[4:-1].str.join(" ")
labelslist = labels.tolist()
rndperm = np.random.permutation(mat.shape[0])

pca = PCA(n_components=4)
pca_result = pca.fit_transform(mat)

mat['pca-one'] = pca_result[:, 0]
mat['pca-two'] = pca_result[:, 1]
mat['pca-three'] = pca_result[:, 2]
mat['pca-four'] = pca_result[:, 3]
print('Explained variation per principal component: {}'.format(pca.explained_variance_ratio_))

plt.figure(figsize=(17, 10))
sns.set_context("poster")
b = sns.scatterplot(
    x="pca-four", y="pca-three",
    palette=sns.color_palette("hls", len(set(labelslist))),
    data=mat,
    #legend="full",
    hue=labelslist,
)
#b.set_xlabel("pca-three: 8.77% of variance")
#b.set_ylabel("pca-two: 12.86% of variance")

plt.show()
