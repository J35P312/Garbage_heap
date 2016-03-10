import sys
import argparse

parser = argparse.ArgumentParser("""turns a snpeff vcf into a csv file, output is printed to the stdout""")
parser.add_argument('--vcf',type=str,required=True,help="the path to the vcf file")
args, unknown = parser.parse_known_args()

print("Chromosome,Position,Ref,Alt,feature,effect,Gene,zygosity,CADD,popfreq")
output="{chromosome},{pos},{ref},{alt},{feature},{effect},{gene},{zygosity},{CADD},{popfreq}"
for line in open(args.vcf):
    if not "#" == line[0]:
        content=line.strip().split("\t")
        try:
            SNPEFF=line.split("EFF=")[1];
        except:
                SNPEFF=line.split("ANN=")[1];
