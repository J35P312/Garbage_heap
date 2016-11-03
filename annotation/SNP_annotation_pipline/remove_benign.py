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
            try:
                VEP=line.split("EFF=")[1];
            except:
                VEP=line.split("ANN=")[1];
        if "HIGH" in VEP or "MODERATE" in VEP or "splice" in VEP:
            print(line.strip())

