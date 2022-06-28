import os
import sys
import pandas as pd
import numpy as np
from collections import OrderedDict

bigmatrix_path = sys.argv[1]
smallmatrix_path = sys.argv[2]

bigmat = pd.read_csv(bigmatrix_path, sep="\t", index_col=0)
smallmat = pd.read_csv(smallmatrix_path, sep="\t", index_col=0)

featToKeep = list(smallmat.columns.values)

bigmat = bigmat[bigmat.index.isin(featToKeep)]

bigmat.to_csv(bigmatrix_path[0:-4] + "_unnor_importantFeat.tsv", sep="\t")