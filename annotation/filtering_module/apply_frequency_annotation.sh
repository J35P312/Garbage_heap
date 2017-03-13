#first argument - input directory
#second argument - output directory

exac_path=
kg_path=

for file in $(ls $1)
do

    filename=$(basename "$file")
    extension="${filename##*.}"
    filename="${filename%.*}"

    python exac_annotation_sqlite.py --vcf $1/$file --exac $exac_path --tag AF > $2/$filename.exac.vcf
    python exac_annotation_sqlite.py --vcf $2/$filename.exac.vcf --exac $kg_path --tag 1000GAF > $2/$filename.exac.kg.vcf

done
