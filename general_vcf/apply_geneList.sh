#first argument - input directory
#second argument - gene list file, a text file containing one gene symbol per line
#third argument - output directory
#WARNING: do not set input and output directory to the same directory!!!

for file in $(ls $1)
do
    python print_variant.py $1/$file $2 > $3/$file
done
