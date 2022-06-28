#!/bin/bash
dir=$1
for FILE in $dir*; do
filename=$FILE
       /nfs/data/CellTypeDeconvRNA/tools/KMC3/kmc_dump ${filename%.*} ${filename%%.*}_counts.tsv;
done;


