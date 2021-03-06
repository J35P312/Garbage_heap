import sys
import argparse
import subprocess
import os
import fnmatch

parser = argparse.ArgumentParser("""takes an indel vcf and a snp vcf as input, these files are merged and filtered using exac frequencies and cadd""")
parser.add_argument('--indels',type=str,required=True,help="the indel vcf")
parser.add_argument('--snps',type=str,required=True,help="The snp vcf")
parser.add_argument('--prefix',type=str,help="output prefix")
parser.add_argument('--cadd',type=str,required=True,help="path to cadd db")
parser.add_argument('--exac',type=str,required=True,help="path to exac db")
parser.add_argument('--kg',type=str,required=True,help="path to thousand genome db")
args, unknown = parser.parse_known_args()

if not args.prefix:
    args.prefix=args.indels.split("/")[-1].split(".")[0]

os.system("vcf-concat {} {} > {}".format(args.snps,args.indels,args.prefix+"_concat.vcf"))

f= open(args.prefix+"_no_benign.vcf","w")
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
os.system("python exac_annotation_sqlite.py --vcf {} --tag EXACAF --exac {} > {}".format(args.prefix+"_no_benign.vcf", args.exac, args.prefix+".exac.vcf"))
os.system("python exac_annotation_sqlite.py --vcf {} --tag 1000GAF --exac {} > {}".format(args.prefix+".exac.vcf", args.kg, args.prefix+".exac.kg.vcf"))


f= open(args.prefix+".filtered.vcf","w")
for line in open(args.prefix+".exac.kg.vcf"):
    
    if(line[0] == "#"):
        f.write( line.strip() + "\n" )
    else:
        kg_frq=0
        exac_frq=0
        if ";1000GAF=" in line:
            content=line.split("\t")
            frq=content[7].split(";1000GAF=")[-1]
            kg_frq=frq.split(";")[0]
            
        if ";EXACAF=" in line:
            content=line.split("\t")
            frq=content[7].split(";EXACAF=")[-1]
            exac_frq=frq.split(";")[0]
        
        if float(exac_frq) <= 0.02 and float(kg_frq) <= 0.02:
            f.write( line.strip() + "\n" )
f.close()

