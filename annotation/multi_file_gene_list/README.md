Multi_file_gene_list
This is a collection of scripts used to apply a gene list filter on a large amount of files, using the least possible amount of arguments.
THe gene_list.py script accepts the path to one folder as an argument:

python gene_list.py /path/to/folder

This folder should contain vcf files and atleast one gene list. THese gene list files should either have csv, txt or tab prefix.
Th script creates one folder per gene list, and filters each vcf according to these gene lists, the filtered result is then added in the
generated for each gene list.
