#first argument - input directory

for file in $(ls $1)
do
    python CCCTG.py --vcf $file
done
