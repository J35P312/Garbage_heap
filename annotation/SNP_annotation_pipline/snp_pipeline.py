import sys
import argparse
import subprocess
import os
import fnmatch

parser = argparse.ArgumentParser("""takes an indel vcf and a snp vcf as input, these files are merged and filtered using exac frequencies and cadd""")
parser.add_argument('--indels',type=str,required=True,help="the indel vcf")
parser.add_argument('--snps',type=str,required=True,help="The snp vcf")
parser.add_argument('--prefix',type=str,"output",help="output prefix")
parser.add_argument('--cadd',type=str,default=3000,help="path to cadd db")
parser.add_argument('--exac',type=str,default=3000,help="path to exac db")
args, unknown = parser.parse_known_args()

if not args.prefix:
    args.prefix=args.indels.split("/")[-1].split(".")[0]

os.system("vcf-concat {} {} > {}".format(args.snps,args.indels,args.prefix+"_concat.vcf"))

f= open(args.prefix+"_no_benign.vcf")
for line in open(args.prefix+"_concat.vcf"):
    
    if(line[0] == "#"):
        f.write( line.strip() + "\n" )
    else:
        try:
            VEP=line.split("CSQ=")[1];
        except:
            try:
                VEP=line.split("EFF=")[1];
            except:
                VEP=line.split("ANN=")[1];
        if "HIGH" in VEP or "MODERATE" in VEP or "splice" in VEP:
            content=line.split("\t")
            if content[6] == "PASS" or content[6] == "." or content[6] == "pass" or content[6] == "Pass":
                f.write( line.strip() + "\n" )
            
f.close()
os.system("python exac_annotation --vcf {} --exac {} > {}".format(args.prefix+"_no_benign.vcf", args.exac, args.prefix+".exac.vcf"))


f= open(args.prefix+".exac.filtered.vcf")
for line in open(args.prefix+".exac.vcf"):
    
    if(line[0] == "#"):
        f.write( line.strip() + "\n" )
    else:
        kg_frq=0
        exac_frq=0
        if ";1000GAF=" in line:
            content=line.split("\t")
            frq=content[7].split(";1000GAF=")[-1]
            kg_frq=frq.split(";")[0]
            
        if ";AF=" in line:
            content=line.split("\t")
            frq=content[7].split(";AF=")[-1]
            exac_frq=frq.split(";")[0]
        
        if float(exac_frq) <= 0.02 and float(kg_frq) <= 0.02:
            f.write( line.strip() + "\n" )
f.close()

