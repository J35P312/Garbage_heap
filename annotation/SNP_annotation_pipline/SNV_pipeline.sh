exac_db="/proj/b2014152/private/exac/af_filter_data.tsv"
gene_list="/proj/b2014152/private/exac/GENELIST.txt"

#set the exac_db to the path of the exac tab file, set the gene list to your gene list
python exac_annotation.py --exac $exac_db --vcf $1 > $3.exac.vcf
python pop_freq_filter.py $3.exac.vcf > $3.exac_filtered.vcf
python print_variant.py  $3.exac_filtered.vcf $gene_list > $3.exac_filtered.snp.gene_list.vcf

python exac_annotation.py --exac $exac_db --vcf $2 > $3.exac.vcf
python pop_freq_filter.py $3.exac.vcf  > $3.exac_filtered..vcf
python print_variant.py  $3.exac_filtered.vcf $gene_list > $3.exac_filtered.indel.gene_list.vcf

vcf-concat $3.exac_filtered.indel.gene_list.vcf $3.exac_filtered.snp.gene_list.vcf > $3.exac_filtered.gene_list.vcf


