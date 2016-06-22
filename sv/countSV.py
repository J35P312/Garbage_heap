import sys
import readVCF
#the vcf file is accepted as argument 1, prints the number of different variants of each type within the vcf
variant_histogram={}
for line in open sys.argv[0]:
    content=line.split("\t")
    if not line[0] == "#":
        variant=readVCFLine(None,line)
        if not variant[-1]  == "":
            #check if we have an 
            if content[4] in variant_histogram:
                variant_histogram[variant[-1]] += 1
            else:
                variant_histogram[variant[-1]]=1
        else:
            if variant[0] == variant[3]:
                if "BND" in variant_histogram:
                    variant_histogram["BND"] +=1
                else:
                    variant_histogram["BND"]=1
            else:
                if "TRA" in variant_histogram:
                    variant_histogram["TRA"] += 1
                else:
                    variant_histogram["TRA"]= 1
                
for variant_type in variant_histogram:
    print("{}\t{}".format(variant_type,variant_histogram[variant_type]))
