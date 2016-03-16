import sys
import os
#accepts the path to a vep annotated vcf as the first command, prints all structural variatn that reside within a gene
inputFile=sys.argv[1];
for line in open(inputFile):
    
    if(line[0] == "#"):
        print(line.strip())
    else:
        content=line.split("\t")
        frq=content[7].split(";1000GAF=")
        frq=frq.split(";")[-1]
        if float(frq) <= 0.01:
            print(line.strip())

