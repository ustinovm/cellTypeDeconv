#!/bin/bash
#
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=0-00:00:10
#SBATCH --output=/nfs/data/CellTypeDeconvRNA/data/pipelined/marrowrun/SLURMoutput.txt
#SBATCH --job-name=cellTypeDeconvMarrowRun
#SBATCH --mem-per-cpu=10000
srun python /nfs/data/CellTypeDeconvRNA/data/pipelined/marrowrun/matrixCreator.py /nfs/data/CellTypeDeconvRNA/data/pipelined/marrowrun/kmc15newcounts/ marrow15new
