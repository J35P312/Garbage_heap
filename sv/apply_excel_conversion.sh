#first argument - input directory
for file in $(ls $1)
do
    python CCCTG_SV.py --vcf $1/$file
done
