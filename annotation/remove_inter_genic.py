import sys
import os
#accepts the path to a vep annotated vcf as the first command, prints all structural variatn that reside within a gene
inputFile=sys.argv[1];
for line in open(inputFile):
    
    if(line[0] == "#"):
        print(line.strip())
    else:
        try:
            VEP=line.split("CSQ=")[1];
        except:
            VEP=line.split("EFF=")[1];
        if not "intergenic_variant" in VEP and not "intergenic_region" in VEP:
            print(line.strip())

