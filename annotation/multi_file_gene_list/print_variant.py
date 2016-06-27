import sys
import os
#accepts the path to a gene list as the first argument, each gene is given as a separate line, the second argument is the vcf file. Prints a new vcf file containing genes found in teh gene list
inputFile=sys.argv[1];

variants=sys.argv[2:]
genes=[]
for line in open(sys.argv[2]):
    genes.append("|"+line.strip()+"|");

for line in open(inputFile):
    if line[0] == "#":
        print(line.strip())
    else:
        printed=False;
        for gene in genes:
            if not printed and gene in line:
                printed = True;
                print(line.strip())

