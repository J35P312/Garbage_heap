import sys
import argparse

parser = argparse.ArgumentParser("""removes all vcf entries that are not marked pass or .""")
parser.add_argument('--vcf',type=str,required=True,help="the path to the vcf file")
args, unknown = parser.parse_known_args()

for line in open(args.vcf):
    
    if(line[0] == "#"):
        print(line.strip())
    else:
        content=line.split("\t")
        end=content[7].split(";END=")[-1]
        end=end.split(";")[0]
        END=int(end)
        if(abs(END-int(content[1])) > 200):
            print(line.strip())
        else:
            print(abs(END-int(content[1])))
