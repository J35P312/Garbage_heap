The_annotator
This script accepts a folder containing files with ending txt,tab or bed. These files contain one gene per line, as well as a key for that gene.
THe script also accepts a vcf file, annotaed by vep or snpeff. THe script will add the key of each gene within the txt,tab or bed files to variatns containing the gene of any key.

python The_annotator.py /path/to/folder vcf_file.vcf
