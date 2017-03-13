#first argument - input directory
#second argument - output_directory

for file in $(ls $1)
do
    grep -E "HIGH|MODERATE" $file > $2/$file
done
