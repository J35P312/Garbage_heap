import sys
import os
import re
#accepts the path to a vep annotated vcf as the first command, prints all structural variatn that reside within a gene
inputFile=sys.argv[1];
for line in open(inputFile):
    
    if(line[0] == "#"):
        print(line.strip())
    else:
        front=line.split(";OCC=")[0]
        back=line.split(";FRQ=")[-1]
        back=back.split(";")[1:]
        if len(back) > 1:
            back=";".join(back);
        if not back == "":
            print(front + ";" + back.strip())
        else:
            print(front.strip)

