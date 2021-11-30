import os
import sys
import pandas as pd
from IPython.display import display
from functools import reduce

input_path = sys.argv[1]

if not os.path.isdir(input_path):
    print('The path specified does not exist')
    sys.exit()

df_files = []
for file in os.listdir(input_path):
    filename = input_path + "\\" + file
    df = pd.read_csv(filename, header=None, index_col=0, sep='\t')
    #df = df.set_index('0')  # set index
    #df.set_index(list(df.rows[0]))
    df = df[~df.index.duplicated(keep='first')]  # remove duplicates
    df.columns = [file[9:]]  # set column name to filename
    df_files.append(df)
df_combine = pd.concat(df_files, axis=1).fillna(0)
#df_combine.sort_values(by=df_combine.columns[0])
df_combine.to_csv("testoutfile.tsv", sep="\t")
