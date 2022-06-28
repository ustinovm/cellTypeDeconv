#!/bin/bash
dirpath=$1
indexpath=$2
runname=$3

for f in x*;
do
	cat $f | xargs /nfs/data/CellTypeDeconvRNA/tools/sratoolkit.2.11.1-ubuntu64/bin/fasterq-dump
done

python SRAtoLabel.py $1 $2

mkdir fastas
mkdir fastasUnused
mkdir kmcfiles
mkdir counts
mkdir temp

mv ./smartseq* ./fastas
mv ./*_2.fastq ./fastasUnused
wc -l `find ./fastas/ -type f` | tee readnumsNew.txt
cat readnumsNew.txt | sed 's/^[ \t]*//' > $runname.readnums.txt

for FILE in ./fastas/*; do
         /nfs/data/CellTypeDeconvRNA/tools/KMC3/kmc -fm -v -cs100000000 $FILE $FILE.res ./temp;
done;

mv ./fastas/*kmc* ./kmcfiles/

./kmcDumpWholeFolder.sh kmcfiles/

mv ./kmcfiles/*_counts* ./counts/

python matrixCreator.py ./counts/ $3

