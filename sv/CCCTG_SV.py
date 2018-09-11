import sys
import argparse
from operator import itemgetter, attrgetter
import xlwt
import readVCF

def EFF(effects):
    snp_dictionary={}
    for effect in effects:
        if "HIGH" in effect or "MODERATE" in effect and "protein_coding" in effect:
            variant=effect.split("(")[0]
            if "[" in variant:
                variant=variant.split("[")[0]
            gene=effect.split("|")[5]
            feature=effect.split("|")[3]
            #for each snp, each unique effect of each gene shoudl only be reported once, ie not multiple intron variant GENEX for snp z
            if not gene in snp_dictionary:
                snp_dictionary[gene]={variant:feature}
            else:
                snp_dictionary[gene].update({variant:feature})
        #if sequence_feature is not the only entry of a gene, 
    return(snp_dictionary)
    
def ANN(effects):
    snp_dictionary={}
    for effect in effects:
        if "HIGH" in effect or "MODERATE" in effect or "MODIFIER":
            variant=effect.split("|")[1]
            if "[" in variant:
                variant=variant.split("[")[0]
            gene=effect.split("|")[3]
            feature=effect.split("|")[10]
            #for each snp, each unique effect of each gene shoudl only be reported once, ie not multiple intron variant GENEX for snp z
            if not gene in snp_dictionary:
                snp_dictionary[gene]={}
            snp_dictionary[gene][variant]=feature
            #if sequence_feature is not the only entry of a gene, 
    return(snp_dictionary)
    
parser = argparse.ArgumentParser("""turns a snpeff vcf into a csv file, output is printed to the stdout""")
parser.add_argument('--vcf',type=str,required=True,help="the path to the vcf file")
parser.add_argument('--frequency',type=float,default = 0.1,help="frequency threshold, more common variants are not printed")
parser.add_argument('--length',type=int,default = 10000,help="length threshold, smaller intergenic variants are not printed")

args, unknown = parser.parse_known_args()
variant_list=[]

output="\"{chrA}\",{chrB},\"{posA}\",\"{posB}\",\"{len}\",\"{var}\",\"{frequency}\",\"{genes}"

sample_ids = readVCF.get_sample_ids(args.vcf)
for line in open(args.vcf):
    if not "#" == line[0]:
        chrA, posA, chrB, posB,event_type,INFO,format = readVCF.readVCFLine(line)
#        print((chrA, posA, chrB, posB,event_type,INFO,format))
        content=line.strip().split("\t")

        #have a look in the snpeff field
        eff=True
        SNPEFF=""
        try:
            SNPEFF=content[7].split("EFF=")[1];
        except:
                if ";ANN=" in content[7]:
                    SNPEFF=content[7].split("ANN=")[1];
                elif ";CSQ=" in content[7]:
                    eff=False
                    SNPEFF=content[7].split("CSQ=")[1];
        effects=SNPEFF.split(",")
        #generate one netry per gene
        if eff:
            snp_dictionary=EFF(effects)
        else:
            snp_dictionary=ANN(effects)

        signalRD=""
        signalSR=""
        signalPE=""

        orientationA=""
        orientationB=""
        if "PE" in format:
            signalPE = "|".join(format["PE"])
        elif  "DV" in format:
            signalPE = "|".join(format["DV"])
            
        if "SR" in format:
            signalSR = "|".join(format["SR"])
        elif "RV" in format:
            signalSR = "|".join(format["RV"])
        if "natorRD" in INFO:
            signalRD = INFO["natorRD"]
            
        genes=[]
        for gene in snp_dictionary:
            genes.append(gene)
        length=float("inf")
        if chrA == chrB:
            length= int(posB)-int(posA)

        zygosity=""
        if "0/1" in content[-1]:
                zygosity="Het"
        elif "1/1" in content[-1]:
                zygosity="Hom"

        if ( len(genes) > 0 and not (len(genes) == 1 and genes[0] == "") ) or length > args.length:
            frq=0
            if "FRQ" in INFO:
                frq=float(INFO["FRQ"])
            if frq >= args.frequency: 
                continue
            
            variant_content = [chrA, chrB, posA, posB, length, event_type, frq]
            for gt in format["GT"]:
                if gt == "0/1":
                    variant_content.append("Het")
                elif gt == "1/1":
                    variant_content.append("Hom")
                # otherwise wild-type is assumed
                else:
                    variant_content.append("WT")
            variant_content.append(signalPE)
            variant_content.append(signalSR)
            variant_content.append(signalRD)
            if len(genes) < 200:
                variant_content.append("|".join(genes))
            else:
                variant_content.append("More than 200 genes!")
            variant_list.append(variant_content)

filename=args.vcf.replace(".vcf",".xls")

wb =  xlwt.Workbook()
ws0 = wb.add_sheet("sample",cell_overwrite_ok=True)
i=0;
header=["ChromosomeA","chromosomeB","PosA","PosB","Length","variant","frequency"]
for sample_id in sample_ids:
    header.append(sample_id)
header.append("signalPE")
header.append("signalSR")
header.append("signalRD")
header.append("Genes")
j=0
for item in header:
    ws0.write(i, j, item)
    j+=1
i=1
for entry in variant_list: 
    j=0;
    for item in entry:
        ws0.write(i, j, item)
        j+=1
    i+=1

wb.save(filename)
