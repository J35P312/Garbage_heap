import sys
import os
import re
#accepts the path to a vep annotated vcf as the first command, prints all structural variatn that reside within a gene
inputFile=sys.argv[1];
hist={}
for line in open(inputFile):
    
    if(line[0] == "#"):
        pass
    else:
        lte=line.split(";LTE=")[-1]
        lte=lte.split(";")[0]
        if not lte in hist:
            hist[lte] = 0;
        hist[lte] += 1

for val in sorted(hist):
    print("{}\t{}".format(val,hist[val]))
