import sys
#arguments a a bunch of vcf files, separated by 
hets_patient=0
hom_patient=0

sample_data={}
first=True
q_lim=60
min_depth=20
max_depth=40

for sample in sys.argv:
    if first:
        first=False
        continue
    sample_data[sample.split("/")[-1].replace(".vcf","")]={"hom":0,"het":0}

    for line in open(sample):
        if line[0] == "#":
            continue
        content=line.strip().split()
        if content[6] <= q_lim:
            continue
        depth=int(line.split(";DP=")[-1].split(";")[0])

        if depth < min_depth or depth > max_depth:
            continue

        if "\t0/1:" in line:
             sample_data[sample.split("/")[-1].replace(".vcf","")]["het"]+=1
        elif "\t1/1:" in line:
             sample_data[sample.split("/")[-1].replace(".vcf","")]["hom"]+=1

print "sample\thets\thom\ttotal\tratio"
for sample in sample_data:
    total=sample_data[sample]["het"]+sample_data[sample]["hom"]
    print "{}\t{}\t{}\t{}\t{}".format(sample,sample_data[sample]["het"],sample_data[sample]["hom"],total,sample_data[sample]["het"]/float(total))

