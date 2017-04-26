import sys
import argparse
import subprocess
import os
import fnmatch

parser = argparse.ArgumentParser("""annotate vcf""")
parser.add_argument('--vcf',type=str,required=True,help="The input vcf")
parser.add_argument('--cadd',type=str,help="path to cadd db")
parser.add_argument('--exac',type=str,help="path to exac db")
parser.add_argument('--kg',type=str,help="path to thousand genome db")
parser.add_argument('--sweref',type=str,help="path to sweref db")
args, unknown = parser.parse_known_args()

args.prefix=args.vcf.replace(".vcf"."")

if args.exac:
    args,prefix += ".exac"
    os.system("python exac_annotation_sqlite.py --vcf {} --tag EXAC --db {} > {}".format(args.vcf   , args.exac, args.prefix+".vcf") )
    args.vcf = args.prefix+".vcf"

if args.kg:
    args,prefix += ".kg"
    os.system("python exac_annotation_sqlite.py --vcf {} --tag 1000GAF --db {} > {}".format(args.vcf , args.kg,  args.prefix+".vcf") )
    args.vcf = args.prefix+".vcf"

if args.swefreq:
    args,prefix += ".sweref"
    os.system("python exac_annotation_sqlite.py --vcf {} --tag SWEREF --db {} > {}".format(args.vcf , args.sweref,  args.prefix+".vcf") )
    args.vcf = args.prefix+".vcf"


if args.cadd  
    args,prefix += ".cadd"  
    os.system("python exac_annotation_sqlite.py --vcf {} --tag CADD --db {} > {}".format(args.vcf , args.cadd,  args.prefix+".vcf") )
    args.vcf = args.prefix+".vcf"
