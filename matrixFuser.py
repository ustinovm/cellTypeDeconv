import os
import sys
import pandas as pd

input_path = sys.argv[1]
df_files = []

for file in os.listdir(input_path):
    filename= input_path + os.sep + file
    df = pd.read_csv(filename, sep="\t", index_col="0")
    del df["Unnamed: 0"]
    df_files.append(df)
df_combine = pd.concat(df_files, axis=1).fillna(0)
df_combine.to_csv("testoutt.tsv", sep="\t")
