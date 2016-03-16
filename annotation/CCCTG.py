import sys
import argparse

parser = argparse.ArgumentParser("""turns a snpeff vcf into a csv file, output is printed to the stdout""")
parser.add_argument('--vcf',type=str,required=True,help="the path to the vcf file")
args, unknown = parser.parse_known_args()

print("\"Chromosome\",\"Position\",\"ID\",\"Ref\",\"Alt\",\"feature\",\"effect\",\"Gene\",\"zygosity\",\"CADD\",\"popfreq\"")
output="\"{chromosome}\",{pos},\"{id}\",\"{ref}\",\"{alt}\",\"{feature}\",\"{effect}\",\"{gene}\",\"{zygosity}\",{CADD},{popfreq}"
for line in open(args.vcf):
    if not "#" == line[0]:
        content=line.strip().split("\t")
        zygosity = "";
        #check the zygozity of the variant, using the GT field
        if len(content) >= 10:
            format_=content[8].split(":")
            if "GT" in format_:
                sample=content[9].split(":")
                pos=format_.index("GT")
                if( sample[pos] == "1/0" or sample[pos] == "0/1"):
                    zygosity="het"
                elif(sample[pos] == "1/1"):
                    zygosity="hom"
        #grab all information from the different fields
        chrom=content[0]
        pos=content[1]
        id_=content[2]
        if id_ ==0:
            id= "."
        ref=content[3]
        alt=content[4]
        cadd=""
        txt=content[7].split(";CADD=")
        if len(txt) == 2:
            txt=txt[-1]
            cadd=txt.split(";")[0]
        popfreq=""
        txt=content[7].split(";1000GAF=")
        if len(txt) == 2:
            txt=txt[-1]
            popfreq=txt.split(";")[0]
        #have a look in the snpeff field
        try:
            SNPEFF=content[7].split("EFF=")[1];
        except:
                SNPEFF=content[7].split("ANN=")[1];
        effects=SNPEFF.split(",")
        #generate one netry per gene
        snp_dictionary={}
        for effect in effects:
            variant=effect.split("(")[0]
            if "[" in variant:
                variant=variant.split("[")[0]
            gene=effect.split("|")[5]
            feature=effect.split("|")[6]
            #for each snp, each unique effect of each gene shoudl only be reported once, ie not multiple intron variant GENEX for snp z
            if not gene in snp_dictionary:
                snp_dictionary[gene]={variant:feature}
            else:
                snp_dictionary[gene].update({variant:feature})
        #if sequence_feature is not the only entry of a gene, then remove it
        for gene in snp_dictionary:
            if len(snp_dictionary[gene]) > 1 and "sequence_feature" in snp_dictionary[gene]:
                del snp_dictionary[gene]["sequence_feature"]
        for gene in snp_dictionary:
            for variant in snp_dictionary[gene]:
                feature=snp_dictionary[gene][variant]
                print(output.format(chromosome=chrom, pos=pos, id=id_, ref=ref, alt=alt,feature = feature ,effect=variant,gene=gene,zygosity=zygosity,CADD=cadd, popfreq=popfreq))
