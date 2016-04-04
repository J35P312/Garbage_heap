import argparse
import sys
import yaml
import os
import subprocess
import re
import fnmatch
import tracking_module

#the module used to perform the variant calling
def calling(args,config,output,programDirectory):
    general_config=config["FindSV"]["general"]
    prefix=args.prefix
    output_prefix=os.path.join(output,prefix)


    CNVNator="""#! /bin/bash -l
#SBATCH -A {account}
#SBATCH -o {filename}.out
#SBATCH -e {filename}.err
#SBATCH -J {name}.job
#SBATCH -p core
#SBATCH -t 20:00:00
module load bioinfo-tools
module load tabix

""".format(name="annotation_{}".format(args.prefix),account=general_config["account"],filename=os.path.join( output,"annotation_{}".format(args.prefix) ) )
    
    cadd_annotate= os.path.join(os.path.dirname(os.path.abspath(__file__)),"annotate_vcf_cadd.py" )
    outputPrefix=os.path.join(output,prefix)
    CNVNator += "python {} {} > {}_nobenign.vcf\n".format(os.path.join(os.path.dirname(os.path.abspath(__file__)),"remove_benign.py" ),args.bam,os.path.join(output,prefix))
    CNVNator += "python {0} --vcf {1}_nobenign.vcf --cadd {2} --popfreq {3} > {1}_CADD.vcf\n".format(cadd_annotate ,outputPrefix,config["FindSV"]["general"]["CADD"],config["FindSV"]["general"]["POP"])
    CNVNator += "python {0} {1}_CADD.vcf > {1}_filtered.vcf\n".format(os.path.join(os.path.dirname(os.path.abspath(__file__)),"pop_freq_filter.py" ), outputPrefix)
    sbatch_ID=submitSlurmJob( os.path.join(output,"slurm/annotation/CNVnator_{}.slurm".format(prefix)) ,CNVNator)

    return("some_vcf",sbatch_ID)

#this function prints the scripts, submits the slurm job, and then returns the jobid
def submitSlurmJob(path,message):
    slurm=open( path ,"w")
    slurm.write(message)
    slurm.close()

    process = "sbatch {0}".format(path)
    p_handle = subprocess.Popen(process, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)    
    p_out, p_err = p_handle.communicate()
    try:
        return( re.match(r'Submitted batch job (\d+)', p_out).groups()[0] );
    except:
        return("123456")

#read the config file, prefer command line option to config
def readconfig(path,command_line):
    config={}
    if path:
        config_file=path
    else:
        programDirectory = os.path.dirname(os.path.abspath(__file__))
        config_file=os.path.join(programDirectory,"config.txt")
    with open(config_file, 'r') as stream:
        config=yaml.load(stream)
    return(config)

def main(args):
    programDirectory = os.path.dirname(os.path.abspath(__file__))
    config=readconfig("config.txt",args);
    caller_slurm_ID=[];
    caller_output=[];
    #fetch the scripts
    #initiate the output location
    output=config["FindSV"]["general"]["output"]
    
    tracking=True;
    #create a folder to keep the output sbatch scripts and logs
    if not os.path.exists(os.path.join(output,"slurm/annotation/")):
        os.makedirs(os.path.join(output,"slurm/annotation/"))
    if not os.path.exists(os.path.join(output,"tracker.yml")) or not tracking:
        tracking_module.generate_tracker(output)
    #the prefix of the output is set to the prefix of the bam file
    prefix=args.bam.split("/")[-1]
    args.prefix=prefix.replace(".vcf","")
    
    
    with open(os.path.join(output,"tracker.yml"), 'r') as stream:
        tracker=yaml.load(stream)
    
    #run the callers
    if not args.prefix in tracker["FindSV"]["annotation"]:    
        outputVCF,sbatch_ID=calling(args,config,output,programDirectory)
        caller_output=outputVCF.split()
        tracking_module.add_sample(args.prefix,args.bam,[caller_output],sbatch_ID,"annotation",output)
        caller_vcf=outputVCF
    else:
        tracker=tracking_module.update_status(args.prefix,"annotation",output)

parser = argparse.ArgumentParser("FindSV core module",add_help=False)
parser.add_argument('--bam', type=str,help="annotate a snp vcf file")
parser.add_argument("--folder", type=str,help="annotate all vcf files in a given folder")
args, unknown = parser.parse_known_args()

programDirectory = os.path.dirname(os.path.abspath(__file__))
 
if args.bam:
    caller_error=False;annotation_error=False
    try:
        if args.config:
            config_path=args.config
        else:
            config_path=os.path.join(programDirectory,"config.txt")
    except:
        pass
        
    if caller_error or annotation_error:
        print("FindSV is not correctly setup, all errors must be solved before running")
    else:
        if os.path.exists(os.path.join(programDirectory,"config.txt")):
            main(args)
            
#analyse all bamfiles within a folder(recursive searching)
elif args.folder:
    caller_error=False;annotation_error=False
    try:
        if args.config:
            config_path=args.config
        else:
            config_path=os.path.join(programDirectory,"config.txt")
    except:
        pass
        
    if caller_error or annotation_error:
        print("FindSV is not correctly setup, all errors must be solved before running")
    else:
        if os.path.exists(os.path.join(programDirectory,"config.txt")):
            for root, dirnames, filenames in os.walk(args.folder):
                for filename in fnmatch.filter(filenames, '*.vcf'):
                    bam_file=os.path.join(root, filename)
                    args.bam=bam_file
                    main(args)


    
else:
    parser.print_help()
