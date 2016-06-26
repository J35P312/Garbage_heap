#!/bin/bash -l
 
#SBATCH -A b2014152
#SBATCH -p core
#SBATCH -n 1
#SBATCH -t 24:00:00
#SBATCH -J zip

module load bioinfo-tools
module load tabix

#argument 1 is the vcf file
bgzip $1
