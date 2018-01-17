import sys
import os

if len(sys.argv) != 4:
	print "ERROR: missing input, use the following command"
	print "python extractRegion.py regions.txt input.bam prefix"
	print "Do not set the input and output to the same file!"

dist=10000

f=open("{}.bed".format(sys.argv[3]),"w")
for line in open(sys.argv[1]):
	content=line.strip().split()
	P1_start=int(content[1])-dist
	if P1_start < 0:
		P1_start=0
	P1_end=int(content[1])+dist
	
	P2_start=int(content[3])-dist
	if P2_start < 0:
		P2_start=0
	if P2_start <= P1_end and content[0] == content[2]:
		P2_start=P1_end+1
	P2_end=int(content[3])+dist
	
	f.write("{}\t{}\t{}\n".format(content[0],P1_start,P1_end))
        f.write("{}\t{}\t{}\n".format(content[2],P2_start,P2_end))

f.close()
os.system("bedtools sort -i {}.bed | bedtools merge -i - > {}.sort.bed".format(sys.argv[3],sys.argv[3]))
regions=[]
for line in open("{}.sort.bed".format(sys.argv[3])):
	content=line.strip().split()
	regions.append("{}:{}-{}".format(content[0],content[1],content[2]))

if sys.argv[2] != sys.argv[3]:
	os.system("samtools view -bh {} {} > {}.bam".format(sys.argv[2]," ".join(regions),sys.argv[3] ))
else:
	print "Nope! Try again"

	
