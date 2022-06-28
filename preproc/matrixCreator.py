import os
import sys
import pandas as pd
from IPython.display import display
from functools import reduce

input_path = sys.argv[1]
outname = sys.argv[2]

if not os.path.isdir(input_path):
    print('The path specified does not exist')
    sys.exit()

df_files = []
for file in os.listdir(input_path):
    filename = input_path + os.sep + file
    if os.path.getsize(filename) > 0:
        #TODO: remove empty lines from final matrix
        print("trying to read" + filename)
        df = pd.read_csv(filename, header=None, index_col=0, sep='\t', low_memory=True, memory_map=True)
        if(len(df.index)>1):
        #df = df.set_index('0')  # set index
        #df.set_index(list(df.rows[0]))
            df = df[~df.index.duplicated(keep='first')]  # remove duplicates
            df.columns = [file[9:]]  # set column name to filename
            df_files.append(df)
            print("file " + filename + " appended to Matrix")
print("trying to concat")
df_combine = pd.concat(df_files, axis=1, sort=True).fillna(0)
#df_combine.sort_values(by=df_combine.columns[0])
df_combine.to_csv(outname+".tsv", sep="\t")
