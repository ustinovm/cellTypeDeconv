#!/bin/bash

mkdir kmc40
mkdir kmc40counts
mkdir kmc30
mkdir kmc30counts
mkdir kmc20
mkdir kmc20counts
mkdir kmc15
mkdir kmc15counts

for FILE in ./fastas/*; do
         /nfs/data/CellTypeDeconvRNA/tools/KMC3/kmc -k40 -fm -v -cs100000000 $FILE $FILE.res ./temp;
done;

mv ./fastas/*kmc* ./kmc40/

./kmcDumpWholeFolder.sh kmc40/

mv ./kmc40/*_counts* ./kmc40counts/

python matrixCreator.py ./kmc40counts/ marrow40

python normalizer.py marrow40.tsv marrowrun.readnums.txt


for FILE in ./fastas/*; do
         /nfs/data/CellTypeDeconvRNA/tools/KMC3/kmc -k30 -fm -v -cs100000000 $FILE $FILE.res ./temp;
done;

mv ./fastas/*kmc* ./kmc30/

./kmcDumpWholeFolder.sh kmc30/

mv ./kmc30/*_counts* ./kmc30counts/

python matrixCreator.py ./kmc30counts/ marrow30

python normalizer.py marrow30.tsv marrowrun.readnums.txt


for FILE in ./fastas/*; do
         /nfs/data/CellTypeDeconvRNA/tools/KMC3/kmc -k20 -fm -v -cs100000000 $FILE $FILE.res ./temp;
done;

mv ./fastas/*kmc* ./kmc20/

./kmcDumpWholeFolder.sh kmc20/

mv ./kmc20/*_counts* ./kmc20counts/

python matrixCreator.py ./kmc20counts/ marrow20

python normalizer.py marrow20.tsv marrowrun.readnums.txt


for FILE in ./fastas/*; do
         /nfs/data/CellTypeDeconvRNA/tools/KMC3/kmc -k15 -fm -v -cs100000000 $FILE $FILE.res ./temp;
done;

mv ./fastas/*kmc* ./kmc15/

./kmcDumpWholeFolder.sh kmc15/

mv ./kmc15/*_counts* ./kmc15counts/

python matrixCreator.py ./kmc15counts/ marrow15

python normalizer.py marrow15.tsv marrowrun.readnums.txt


