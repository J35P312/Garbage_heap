import sys
import os
import fnmatch
import subprocess
import glob
#this script applies gene list filters on any number of vcf files. Read the README.md file for more info on how to run the script.



def detect_files(path,extensions):
    files={}
    for extension in extensions:
        for file in glob.glob(os.path.join(path,"*.{}".format(extension) ) ):
            name=file.split("/")[-1].split(".{}".format(extension))[0]
            print name
            files[name]=[file,path]
                        
    return(files)

def apply_gene_list(input_vcf,output_vcf,gene_list):
    genes=[]
    for line in open(gene_list):
        genes.append("|"+line.strip()+"|");

    f = open(output_vcf,'w')
    for line in open(input_vcf):
        if line[0] == "#":
            f.write(line)
        else:
            printed=False;
            for gene in genes:
                if not printed and gene in line:
                    printed = True;
                    
                    
                    if "FRQ" in line:
                        frequency=line.split("\t")[7]
                        frequency=frequency.split("FRQ=")[-1]
                        frequency=frequency.split(";")[0]
                        if float(frequency) < 0.075:
                            f.write(line)
                    
                    else:
                        f.write(line)
                
    f.close()
    
try:
    path=sys.argv[1]
except:
    print "Error: no input path!"
    print "exmple python gene_list.py /path/to/the/files"

gene_lists=detect_files(path,["txt","csv"])
vcf_files=detect_files(path,["vcf"])

for gene_list in gene_lists:
    if not os.path.exists( os.path.join(gene_lists[gene_list][1],gene_list) ):
        os.makedirs( os.path.join(gene_lists[gene_list][1],gene_list) )
    for vcf in vcf_files:
        genes=gene_lists[gene_list][0]
        input_vcf=vcf_files[vcf][0]
        output_vcf= os.path.join(gene_lists[gene_list][1],gene_list,vcf+"_"+gene_list+".vcf")
        apply_gene_list(input_vcf,output_vcf,genes)
        
