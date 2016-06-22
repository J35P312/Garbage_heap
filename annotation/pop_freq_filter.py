import sys
import os
#accepts the path to a vep annotated vcf as the first command, prints all structural variatn that reside within a gene
inputFile=sys.argv[1];
for line in open(inputFile):
    
    if(line[0] == "#"):
        print(line.strip())
    else:
        content=line.split("\t")
        frq=content[7].split(";1000GAF=")[-1]
        frq=frq.split(";")[0]
        if float(frq) <= 0.05:
            print(line.strip())

