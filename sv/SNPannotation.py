import sys
import argparse
import subprocess
import os
import fnmatch
import readVCF

def retrieve_snps(chrom,start,end,SNV):
    snp_string=chrom
    for snv in SNV[chrom]:
        if snv >= start and snv <= end:
            snp_string += "|{}:{}->{}".format(snv,SNV[chrom][snv]["ref"],SNV[chrom][snv]["alt"])
    
    return(snp_string)

def main(args):
    SNV={}
    for line in open(args.SNVvcf): 
        content=line.split("\t")
        content[1] = int(content[1])
        if not content[0] in SNV:
            SNV[content[0]]={}
        if not content[1] in SNV[content[0]]:
            SNV[content[0]][content[1]]=[]
        SNV[content[1]].append({"ref":content[3],"alt":content[4]})

    for line in open(args.SVvcf):
        if line[0] == "#" and line[1] == "#":
            print line.strip()
        elif line[0] == "#":
            print "##INFO=<ID=COMPOUND,Number=1,Type=String,Description=\"prints all snps and snvs found within the SV in the following format chr|pos:ref-alt|pos2:ref2->alt2..\">"
            print line.strip()
        content=line.strip().split("\t")
        snp_tag="COMPOUND=;"
        
        chrA,posA,chrB,posB,event_type,INFO,FORMAT =readVCF.readVCFLine(line);
        if chrA == chrB:
            snp_tag+=retrieve_snps(chrA,posA-args.padding,posB+args.padding)
        else:
            snp_tag+=retrieve_snps(chrA,posA-args.padding,posA+args.padding)
            snp_tag+= "|" + retrieve_snps(chrB,posB-args.padding,posB+args.padding)
        content[7]+=snp_tag;
        "\t".join(content)

parser = argparse.ArgumentParser("""this script adds a tag for each snp found within a structural variant""")
parser.add_argument('--SVvcf',type=str,required=True,help="A structural variant vcf")
parser.add_argument('--SNVvcf',type=str,required=True,help="The vcf containing snps and small indels")
parser.add_argument('--padding',type=int,default=3000,help="SNPS within this distance of the breakpoint/variant ends will be added to the tag")
args, unknown = parser.parse_known_args()

if args.vcf:
    main(args)
else:
    print("|>L3453 5|>3(1/=Y --vcf")
