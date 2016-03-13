import sys
import argparse
import subprocess
import os
import fnmatch

def main(args):

    for line in open(args.vcf):

        if line[0] == "#" and line[1] == "#":
           print line.strip()
        elif line[0] == "#":
           print "##INFO=<ID=CADD,Number=1,Type=Float,Description=\"The phredd CADD score of the variant\">"
           print "##INFO=<ID=FRQ,Number=1,Type=Float,Description=\"The frequency of the event in the database\">"
           print line.strip()
        else:
           CADD=0
           FRQ=0
           annotation=";CADD={};FRQ={}"
           content=line.split("\t")

           chromosome=content[0]
           position=int(content[1])
           end=position+1
           alt=content[4]
    	   #cadd annotation
           command=["tabix {} {}:{}-{}".format(args.cadd,chromosome,position,end)]
           tmp=subprocess.check_output(command, shell = True);
           output=tmp.split("\n")
           for entry in output:
               db_content=entry.split("\t")
               if db_content[4] == alt:
                  CADD=db_content[6]
                  break
           content[7] += annotation.format(CADD,FRQ)
           print("\t".join(content))
	   #popfreq
        

parser = argparse.ArgumentParser("""this scripts annotates a SNP using CADD and popfreq, the popfreq and CADD file must be tabix indexed and tabbix must be installed""")
parser.add_argument('--vcf',type=str,required=True,help="the path to the vcf file")
parser.add_argument('--folder',type=str,help="used instead of vcf to annotate each vcf in a folder")
parser.add_argument('-—cadd',type=str,help="The path to the CADD DB")
parser.add_argument('--popfreq',type=str,help="the path to the popfreq DB")
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
