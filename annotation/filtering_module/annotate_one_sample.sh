#!/bin/bash -l
 
#SBATCH -A b2016296
#SBATCH -p core
#SBATCH -n 1
#SBATCH -t 24:00:00
#SBATCH -J TIDDIT

./snpPipe.sh $1 $2 $3
