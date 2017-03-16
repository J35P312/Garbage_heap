#first argument - input directory
#second argument - output_directory

for file in $(ls $1)
do
    grep -E "HIGH|MODERATE" $1/$file > $2/$file
done
