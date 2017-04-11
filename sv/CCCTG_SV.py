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
args, unknown = parser.parse_known_args()
variant_list=[]

output="\"{chrA}\",{chrB},\"{posA}\",\"{posB}\",\"{len}\",\"{var}\",\"{frequency}\",\"{genes}"
for line in open(args.vcf):
    if not "#" == line[0]:
        chrA, posA, chrB, posB,event_type,INFO,format = readVCF.readVCFLine(line)
        content=line.strip().split("\t")

        #have a look in the snpeff field
        eff=True
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
            signalPE =format["PE"][0]
            
        if "SR" in format:
            signalSR =format["SR"][0]      
        if "natorRD" in INFO:
            signalRD = INFO["natorRD"]


        if "PE" in format or "SR" in format:
            orientationA=line.split(";OA=")[-1].split(";")[0]
            orientationB=line.split(";OB=")[-1].split(";")[0]
            
        genes=[]
        for gene in snp_dictionary:
            genes.append(gene)
        length=float("inf")
        if chrA == chrB:
            length= int(posB)-int(posA)

        if len(genes) > 0 or length > 10000:
            if float(INFO["FRQ"]) < args.frequency: 
                if len(genes) < 200:
                    variant_list.append([chrA,chrB,posA,orientationA,posB,orientationB,length,event_type,INFO["FRQ"],signalPE,signalSR,signalRD,"|".join(genes)])
                else:
                    variant_list.append([chrA,chrB,posA,orientationA,posB,orientationB,length,event_type,INFO["FRQ"],signalPE,signalSR,signalRD,"More than 200 genes!"])
filename=args.vcf.replace(".vcf",".xls")

wb =  xlwt.Workbook()
ws0 = wb.add_sheet("sample",cell_overwrite_ok=True)
i=0;
header=["ChromosomeA","chromosomeB","PosA","orientationA","PosB","orientationB","Length","variant","frequency","signalPE","signalSR","signalRD","Genes"]
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
