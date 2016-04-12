import sys
import argparse
import subprocess
import os
import fnmatch

def main(args):
    for line in open(args.vcf):
        if line[0] == "#":
            print line.strip()
        elif(";natorP1=" in line):
            pval=line.split(";natorP1=")[-1]
            pval=pval.split(";")[0]

            pval3=line.split(";natorP3=")[-1]
            pval3=pval3.split(";")[0]

            if float(pval) <= args.pval1 and float(pval3) <= args.pval3:
                print line.strip()
            #else:
            #    print pval
            #    print line.strip()
        else:
            print line.strip()

parser = argparse.ArgumentParser("""this scripts removes low quality cnvnator calls based on the natorP1 and natorP3 tags""")
parser.add_argument('--vcf',type=str,required=True,help="the path to the vcf file")
parser.add_argument('--pval1',type=float,default=0.05,help="threshold P value of natorP1, default =0.05")
parser.add_argument('--pval3',type=float,default=0.05,help="threshold P value of natorP3, default =0.05")
args, unknown = parser.parse_known_args()

if args.vcf:
    main(args)
else:
    print("|>L3453 5|>3(1/=Y --vcf")
