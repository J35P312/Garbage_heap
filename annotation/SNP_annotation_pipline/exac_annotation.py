import sys
import argparse
import subprocess
import os
import fnmatch

def main(args):
    exac_db={}
    for line in open(args.exac):
        if line[0] == "#":
            continue
        content=line.strip().split()
        if not content[0] in exac_db:
            exac_db[content[0]] = {}
        if not content[1] in exac_db[content[0]]:
            exac_db[content[0]][content[1]] = {}  
        exac_db[content[0]][content[1]][content[3]] = content[4]
    for line in open(args.vcf):
        if line[0] == "#" and line[1] == "#":
            print line.strip()
        elif line[0] == "#":
            print "##INFO=<ID=AF,Number=A,Type=Float,Description=\"Estimated allele frequency in the range (0,1) in the 1000G database.\">"
            print line.strip()
        else:
            FRQ=0
            annotation=";AF={}"
            content=line.split("\t")

            chromosome=content[0]
            position=content[1]
            end=position
            alt=content[4]
            #cadd annotation
            if args.exac:
                if chromosome in exac_db:
                    if position in exac_db[chromosome]:
                  	    if alt in exac_db[chromosome][position]:
                  	        FRQ=exac_db[chromosome][position][alt]

            content[7] += annotation.format(FRQ)
            print("\t".join(content).strip())
	   		#popfreq
        

parser = argparse.ArgumentParser("""this scripts annotates a SNP using CADD and popfreq, the popfreq and CADD file must be tabix indexed and tabbix must be installed""")
parser.add_argument('--vcf',type=str,required=True,help="the path to the vcf file")
parser.add_argument('--folder',type=str,help="used instead of vcf to annotate each vcf in a folder")
parser.add_argument('--exac',type=str,help="the path to the exac DB")
args, unknown = parser.parse_known_args()

if args.vcf:
    main(args)
elif args.folder:
    for root, dirnames, filenames in os.walk(args.folder):
            for filename in fnmatch.filter(filenames, '*.vcf'):
                bam_file=os.path.join(root, filename)
                args.vcf=bam_file
                main(args)
else:
    print("|>L3453 5|>3(1/=Y --vcf || --folder")
