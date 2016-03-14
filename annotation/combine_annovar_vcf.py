import sys
import argparse

parser = argparse.ArgumentParser("""Adds propfreq and/or CADD via annovar data to a vcf file""")
parser.add_argument('--vcf',type=str,required=True,help="the path to the vcf file")
parser.add_argument('--cadd',type=str,default=None,help="the path to the annovar cadd file")
parser.add_argument('--freq',type=str,default=None,help="the path to the annovar popfreqmax file(or any other frequency)")
args, unknown = parser.parse_known_args()


#reads the annotation of the annovar file
def read_annovar_file(annovar_file):
    annovar_annotation={}
    for line in open(annovar_file):
        content=line.split("\t")
        if content[2] in annovar_file:
            if content[6] in annovar_file[content[2]]:
                annovar_annotation[content[2]][content[6]].append( [ content[3],content[1] ] )
            else:
                annovar_annotation[content[2]][content[6]]=[[ content[3],content[1] ]]
        else:
            annovar_annotation[content[2]] = { content[6]:[ [ content[3],content[1] ] ]}
    return(annovar_annotation)

def annotate_vcf(variant,annovar_file):
    annotation=""
    #check if teh variant is present in the annovar file, then add the annotation to the vcf, ele add "" to the vcf
    variant_info=variant.split("\t");
    if variant_info[0] in annovar_file:
        if variant_info[4] in annovar_file[variant_info[0]]:
            for line in annovar_file[variant_info[0]][variant_info[4]]:
                if content[0] == variant_info[1]:
                    return(content[1])
    return(0)
    
    
    
CADD_HEADER="##INFO=<ID=CADD,Number=1,Type=Integer,Description=\"The CADD relative score for this alternative.\">"
FREQ_HEADER="##INFO=<ID=1000GAF,Number=1,Type=Float,Description=\"Estimated allele frequency in the range (0,1) in the 1000G database.\">"

if args.cadd:
    CADD=read_annovar_file(args.cadd)
if args.freq:
    FRQ=read_annovar_file(args.freq)


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
            tag += annotate_vcf(line,CADD)
        if args.freq:
            tag += ";1000GAF="
            tag +=annotate_vcf(line,FRQ)
        content[7]+=tag
        print("\t".join(content))
