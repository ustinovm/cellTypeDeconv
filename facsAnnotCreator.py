import os
import sys
import random
import pandas as pd
import numpy as np

annotationfilepath = "C:\\Users\\Maxim\\PycharmProjects\\facsAnnotCreator\\annotations_facs.csv"
cellIdTable = "C:\\Users\\Maxim\\PycharmProjects\\facsAnnotCreator\\SRAtoCellIDTable.txt"

cols = ["cell", "cell_ontology_class", "cell_ontology_id", "plate.barcode", "tissue"]
annot = pd.read_csv(annotationfilepath, low_memory=False, usecols=cols)
annot.set_index("cell", inplace=True)
annot[cols[4]] = annot["tissue"].replace('_', '', regex=True).replace('-', '', regex=True)
cellids = pd.read_csv(cellIdTable, low_memory=False, sep="\t", header=None, usecols=[1, 2])
cellids = cellids.rename(columns={1: "SRA", 2: "cell"})
cellids["cell"] = cellids["cell"].str.slice(0, -12)
cellids = cellids[cellids["cell"].str.contains("_C1") == False]
cellids["cell"] = cellids["cell"].str.slice(0, -3)
cellids.set_index("cell", inplace=True)
# todo: "smartseq2_bladder_tissue_ID_B_cell"
annot["cell_id"] = annot.index
fulllist = annot.join(cellids, how="left")

fulllist.set_index("SRA", inplace=True)
fulllist.replace('\s+', '_', regex=True, inplace=True)
fulllist["newname"] = "smartseq_" + fulllist["tissue"] + "Tissue_" + \
                      fulllist["cell_ontology_class"]
fulllist = fulllist.reset_index()
fulllist['tmp'] = np.arange(len(fulllist))
fulllist["newname"] = (fulllist["newname"].map(str) + "_" + fulllist["tmp"].map(str)).astype(str)
i = 0
"""for row in fulllist.values:
    print(cellids.loc[row[5]])
    print(annot.loc[row[5]])
    print(row)"""

outputlist = fulllist[["SRA", "newname"]]

outputlist.to_csv("ConversionListC2.csv", sep="\t")
