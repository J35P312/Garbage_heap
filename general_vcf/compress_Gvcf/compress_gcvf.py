import sys
import os
import fnmatch
import subprocess

#this is a script used to compress all the gvcf files in a folder
#first argument is the path to the folder containing gcvcf files
#the script launches the script called delly, this script loads a module containing tabix and compresses it to gz files.

def detect_bam_files(path):
    bam_files={};
    
    for project in path:
        path_to_sample = os.path.join(project.strip())
        tmp_bam_files=[]
        for root, dirnames, filenames in os.walk(path_to_sample):
            for filename in fnmatch.filter(filenames, '*.genomic.vcf'):
                file=(os.path.join(root, filename))
                
                print file
                process = "sbatch delly.sh {0}".format(file)
                print process
                p_handle = subprocess.Popen(process, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)    
                p_out, p_err = p_handle.communicate()
    

        for root, dirnames, filenames in os.walk(path_to_sample):
            for filename in fnmatch.filter(filenames, '*.g.vcf'):
                file=os.path.join(root, filename)

                print file
                process = "sbatch delly.sh {0}".format(file)
                print process
                p_handle = subprocess.Popen(process, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)    
                p_out, p_err = p_handle.communicate()
                

    return(tmp_bam_files)
    
    

files = detect_bam_files(sys.argv[1])
