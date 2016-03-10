import sys
import argparse

parser = argparse.ArgumentParser("""Adds propfreq and/or CADD via annovar data to a vcf file""")
parser.add_argument('--vcf',type=str,required=True,help="the path to the vcf file")
parser.add_argument('--cadd',type=str,default=None,help="the path to the annovar cadd file")
parser.add_argument('--freq',type=str,default=None,help="the path to the annovar popfreqmax file(or any other frequency)")
args, unknown = parser.parse_known_args()

def annotate_vcf(variant,annovar_file):
    annotation=""
    #check if teh variant is present in the annovar file, then add the annotation to the vcf, ele add "" to the vcf
    variant_info=variant.split("\t");
    for line in open(annovar_file):
        content=line.split("\t")
        if content[2] == variant_info[0]:
            if content[3] == variant_info[1]:
                if content[6] == variant_info[4]:
                    annotation=content[1]
                    break
    if (annotation == ""):
        annotation="0"
    return(annotation)
    
    
CADD_HEADER="##INFO=<ID=CADD,Number=1,Type=Integer,Description=\"The CADD score of the variant\">"
FREQ_HEADER="##INFO=<ID=FRQ,Number=1,Type=Integer,Description=\"The frequency of the event in the database\">"



for line in open(args.vcf):
    content=line.split("\t")
    #print the header, then we are leaving the header, add CADD and FREQ tags to it
    if(line[0] == "#" and line[1] == "#"):
        print(line.strip())
    elif(line[0] == "#"):
        print(CADD_HEADER)
        print(FREQ_HEADER)
        print(line.strip())
    else:
        tag="";
    
        if args.cadd:
            tag +=";CADD="
            tag += annotate_vcf(line,args.cadd)
        if args.freq:
            tag += ";FRQ="
            tag +=annotate_vcf(line,args.freq)
        content[7]+=tag
        print("\t".join(content))
