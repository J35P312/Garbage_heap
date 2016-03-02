import sys
import os
#accepts a vcf queried vs a frequency database, aswell as the highest allowed allele frequency. Prints all variants less common than the given threshold
inputFile=sys.argv[1];
limit=float(sys.argv[2]);
for line in open(inputFile):
    
    if(line[0] == "#"):
        print(line.strip())
    else:
        FRQ=line.split("FRQ=")[1];
        FRQ=FRQ.split(";")[0];
        FRQ=float(FRQ)
        if FRQ < limit:
            print(line.strip())

