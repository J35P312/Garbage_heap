import sys
import argparse
import subprocess
import os
import fnmatch

def main(vcf,humandb,output_folder):
    
    prefix=os.path.join(output_folder,vcf.split("\t")[-1])
    prefix=prefix.replace(".vcf","")
    
    
    #convert the vcf to annovar format
    convert2annovar="convert2annovar.pl -format vcf4 {input_vcf} > {prefix}.annovar"
    command=[convert2annovar.format(input_vcf=vcf,prefix=prefix)]
    tmp=subprocess.check_output(command, shell = True);
    
    popfreq="popfreq_max_20150413"
    cadd="cadd"
    annotate_varition="annotate_variation.pl -filter -out {prefix} -dbtype {db_type}  -build hg19 {prefix}.annovar {db_folder} "
    
    #popfreq annotation
    command=[annotate_varition.format(db_folder=humandb,db_type=popfreq,prefix=prefix)]
    tmp=subprocess.check_output(command, shell = True);
    
    #cadd annotation
    command=[annotate_varition.format(db_folder=humandb,db_type=cadd,prefix=prefix)]
    tmp=subprocess.check_output(command, shell = True);
    return(0);
        

parser = argparse.ArgumentParser("""this scripts annotates a SNP vcf using annovar, the humanDd folder is harcoded on line 20 of the script, the scrip""")
parser.add_argument('--vcf',type=str,help="the path to the vcf file")
parser.add_argument('--folder',type=str,help="used instead of vcf to annotate each vcf in a folder")
args, unknown = parser.parse_known_args()
humandb="/proj/b2015375/private/humandb/"

if args.vcf:
    main(args.vcf,humandb,"")
elif args.folder:
    for root, dirnames, filenames in os.walk(args.folder):
            for filename in fnmatch.filter(filenames, '*.vcf'):
                bam_file=os.path.join(root, filename)
                args.vcf=bam_file
                main(args.vcf,humandb,"")
else:
    print("|>L3453 5|>3(1/=Y --vcf || --folder")
