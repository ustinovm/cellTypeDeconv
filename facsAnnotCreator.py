import os
import sys
import random
import pandas as pd

annotationfilepath = "C:\\Users\\Maxim\\Desktop\\Bachelorarbeit\\Data\\TabulaMuris\\facs\\annotations_facs.csv"
cellIdTable = "C:\\Users\\Maxim\\Desktop\\Bachelorarbeit\\Data\\TabulaMuris\\facs\\SRAtoCellIDTable.tsv"

cols = ["cell", "cell_ontology_class", "cell_ontology_id", "plate.barcode", "tissue"]
annot = pd.read_csv(annotationfilepath, low_memory=False, usecols=cols)
annot.set_index("cell", inplace=True)
cellids = pd.read_csv(cellIdTable, low_memory=False, sep="\t", header=None, usecols=[1, 2])
cellids = cellids.rename(columns={1: "SRA", 2: "cell"})
cellids["cell"] = cellids["cell"].str.slice(0, -15)
cellids.set_index("cell", inplace=True)
# todo: create renaming name for each sra and save table

fulllist = annot.join(cellids, how="left")
fulllist.set_index("SRA", inplace=True)
fulllist["newname"] = "smartseq_" + fulllist["tissue"] + "_" + fulllist["cell_ontology_class"]
fulllist = fulllist.reset_index()
i = 0
for row in fulllist.values:
    print(row)
    i += 1
#todo: add i to every row fml and saving
print("hola")
