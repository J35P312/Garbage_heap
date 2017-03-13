#first argument - input directory
#second argument - gene list
#third argument - output directory

mkdir $3
mkdir $3/gene_list
mkdir $3/frequency_filter
mkdir $3/effect_filter

./apply_geneList.sh $1 $2 $3/gene_list
./apply_frequency_annotation.sh $3/gene_list $3/frequency_filter
./apply_effect_filter.sh $3/frequency_filter $3/effect_filter

./excel_2_vcf.sh $3/frequency_filter
./excel_2_vcf.sh $3/effect_filter
