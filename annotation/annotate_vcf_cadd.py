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
           		print "##INFO=<ID=CADD,Number=1,Type=Integer,Description=\"The CADD relative score for this alternative.\">"
           		print "##INFO=<ID=1000GAF,Number=A,Type=Float,Description=\"Estimated allele frequency in the range (0,1) in the 1000G database.\">"
           		print line.strip()
        	else:
           		CADD=100
           		FRQ=0
           		annotation=";CADD={};1000GAF={}"
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
               			if len(db_content) > 3:
               				if db_content[3] == alt and str(position) == db_content[1]:
                  				CADD=db_content[5]
                  				break
                  	#popfreq annotation
           		command=["tabix {} {}:{}-{}".format(args.popfreq,chromosome,position,end)]
           		tmp=subprocess.check_output(command, shell = True);
           		output=tmp.split("\n")
           		for entry in output:
               			db_content=entry.split("\t")
               			if len(db_content) > 3:
               				if db_content[4] == alt and str(position) == db_content[1]:
                  				FRQ=db_content[5]
                  				break
                  			
        		content[7] += annotation.format(CADD,FRQ)
           		print("\t".join(content).strip())
	   		#popfreq
        

parser = argparse.ArgumentParser("""this scripts annotates a SNP using CADD and popfreq, the popfreq and CADD file must be tabix indexed and tabbix must be installed""")
parser.add_argument('--vcf',type=str,required=True,help="the path to the vcf file")
parser.add_argument('--folder',type=str,help="used instead of vcf to annotate each vcf in a folder")
parser.add_argument('--cadd',type=str,help="The path to the CADD DB")
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
