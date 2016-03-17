import argparse

parser = argparse.ArgumentParser("""this scripts prints every variant present on a chosen chromosome""")
parser.add_argument('--vcf',type=str,required=True,help="the path to the vcf file")
parser.add_argument('--chr',type=str,,required=True,help="the chromosome")
args, unknown = parser.parse_known_args()

for line in open(args.vcf):
    if line[0] == "#":
        print line.strip()
    else:
        content=line.split("\t")
        if content[0] == args.chr:
            print line.strip()
