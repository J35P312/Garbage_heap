import sys
import os
#accepts the path to a vep annotated vcf as the first command, prints all structural variatn that reside within a gene
inputFile=sys.argv[1];
folder=inputFile.split("/");
folder=folder[:len(folder)-1]
name=inputFile.split("/");
name =name[-1];
name = name.split(".");
name = name[:len(name)-1]
name=".".join(name);

path="/".join(folder)


outputFile=os.path.join(path,name+".FILTERED.genes.csv")
bins={}
events=[];
Nevents=0;
first =1
for line in open(inputFile):
    
    if(line[0] == "#"):
        print(line.strip())
    else:
        VEP=line.split("CSQ=")[1];
        if "intergenic_variant" in VEP:
            print(line.strip())

