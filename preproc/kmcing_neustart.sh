#!/bin/bash
for FILE in ./fastasCont/*; do
         /nfs/data/CellTypeDeconvRNA/tools/KMC3/kmc -k15 -ci100 -fm -v $FILE $FILE.res ./temp;
done;

