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

            for variant in SNV[chrom][snv]:
                snp_string += "|{}:{}->{}".format(snv,variant["ref"],variant["alt"])
    
    return(snp_string)

def main(args):
    SNV={}
    for line in open(args.SNVvcf):
        if line[0] == "#":
            continue
             
        content=line.split("\t")
        content[1] = int(content[1])
        if not content[0] in SNV:
            SNV[content[0]]={}
        if not content[1] in SNV[content[0]]:
            SNV[content[0]][content[1]]=[]
        SNV[content[0]][content[1]].append({"ref":content[3],"alt":content[4]})

    for line in open(args.SVvcf):
        if line[0] == "#" and line[1] == "#":
            print line.strip()
            continue
            
        elif line[0] == "#":
            print "##INFO=<ID=COMPOUND,Number=1,Type=String,Description=\"prints all snps and snvs found within the SV in the following format chr|pos:ref-alt|pos2:ref2->alt2..\">"
            print line.strip()
            continue
            
        content=line.strip().split("\t")
        snp_tag=";COMPOUND="
        
        chrA,posA,chrB,posB,event_type,INFO,FORMAT =readVCF.readVCFLine(line);
        if not chrA in SNV or not chrB in SNV:
            print line.strip()
            continue
        
        if chrA == chrB:
            snp_tag+=retrieve_snps(chrA,posA-args.padding,posB+args.padding,SNV)
        else:
            snp_tag+=retrieve_snps(chrA,posA-args.padding,posA+args.padding,SNV)
            snp_tag+= "|" + retrieve_snps(chrB,posB-args.padding,posB+args.padding,SNV)
            
        if not snp_tag == ";COMPOUND={}".format(chrA) and not snp_tag == ";COMPOUND={}|{}".format(chrA,chrB):
            content[7]+=snp_tag;

        print "\t".join(content)

parser = argparse.ArgumentParser("""this script adds a tag for each snp found within a structural variant""")
parser.add_argument('--SVvcf',type=str,required=True,help="A structural variant vcf")
parser.add_argument('--SNVvcf',type=str,required=True,help="The vcf containing snps and small indels")
parser.add_argument('--padding',type=int,default=3000,help="SNPS within this distance of the breakpoint/variant ends will be added to the tag")
args, unknown = parser.parse_known_args()

main(args)
