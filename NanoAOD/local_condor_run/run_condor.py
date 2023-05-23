import sys,os
import argparse
import re
import optparse
sys.path.append('..')
import json


parser = argparse.ArgumentParser(description='condor for postproc')
parser.add_argument('-f', dest='file', default='', help='json file input')
parser.add_argument('-isFake',type=bool, default=False, help='json file input')
args = parser.parse_args()


with open(args.file, "r") as f:
	jsons = json.load(f)
	f.close()

initial_path = os.getcwd()

import glob
# Dataset Loop
for dataset in jsons:
	
	os.chdir(initial_path)


	## data/MC type setting
	isdata=False # initilize isdata 
	period='B' # initialize period
	if dataset['type'] !='MC':
		isdata=True

	# MC case
	if not isdata:
		datasetname = dataset['name'].split('/')[5] + '_' + dataset['year']

	# Data case -- not used yet (need improvement)
	#else:
	#	run_name	= dataset['name'].split('/')[5]
	#	data_name   = dataset['name'].split('/')[6]
	#	period	  = run_name[7]
	#	datasetname = data_name + '_' + run_name + '_' + dataset['year']
		
	
	## make save directory
	os.system("mkdir -p "+datasetname+"/log")
	os.system("mkdir -p "+datasetname+"/condorOut")
	os.chdir(datasetname)

	flist = glob.glob(dataset['name'])
	i = 0
	for i,filepath in enumerate(flist):

		# Prepare submit	
		filename = filepath.split('/')[-1].split('_')[0]
		print("##"*20)
		print("dataset: ",datasetname)
		print("fname: ",filename)
		print("path: ",filepath)


		## -->>  submit.jds script
		with open ("submit_"+datasetname+"_file"+str(i)+"_"+filename+".jdl","w+") as f:
			f.write("universe \t = vanilla\n")
			f.write("executable \t = wrapper_"+datasetname+"_file"+str(i)+"_"+filename+".sh\n")
			f.write("error \t = log/"+datasetname+"_file"+str(i)+"_"+filename+".err\n")
			f.write("output \t = log/"+datasetname+"_file"+str(i)+"_"+filename+".output\n")
			f.write("log \t = log/"+datasetname+"_file"+str(i)+"_"+filename+".log\n\n")
			f.write("accounting_group=group_cms\n")
			f.write("should_transfer_files \t = YES\n")
			f.write("when_to_transfer_output \t = ON_EXIT\n")
			f.write("transfer_output_files \t = condorOut\n")
			f.write("queue 1")
		f.close()
		print "file",str(i),filename," submit code prepared" 



		## -->>  run scruipt
		with open ("wrapper_"+datasetname+"_file"+str(i)+"_"+filename+".sh","w+") as f:
			f.write("#!/bin/bash\n\n")
			#f.write("condorOut\n\n")

			# set path
			#f.write("initial_path=${PWD}\n\n")
			f.write("home_path=${PWD}\n\n")
	
			# set CMSENV				
			f.write("export SCRAM_ARCH=slc7_amd64_gcc700\n")
			f.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
			
			# !!! You need to modity your path!!!
			f.write("cd /cms/ldap_home/jwkim2/New_ccp/Ntuplizer/CMSSW_10_6_19/src\n")
			f.write("eval `scramv1 runtime -sh`\n")
			f.write("echo $CMSSW_BASE\n\n")


			# set NanoAOD tool and run jobs
			if args.isFake:
				f.write("cd PhysicsTools/NanoAODTools/nanoAOD-WVG/FakePhoton\n")
			else:
				f.write("cd PhysicsTools/NanoAODTools/nanoAOD-WVG/WZG_selector\n")

			# Need absolute path here
			f.write("datasetpath=$home_path/condorOut/" + datasetname + "\n")
		
			
			# Prepare runable script
			ui10_xrootd_path = "root://cms-xrdr.private.lo:2094//xrd/" 
			filepath = filepath.split('xrootd')[-1]
			filepath = ui10_xrootd_path + filepath
			if isdata:

				if args.isFake:
					f.write("python full_Template_postproc.py -f" + " " + filepath + " " + "-y" + " " + dataset['year'] + " " + "-d" + " " +\
					"-dataset_name" + " " + "$datasetpath" + " " +  "-p" + " " +  period + "\n")

				else:
					f.write("python WZG_postproc.py -f" + " " + filepath + " " + "-y" + " " + dataset['year'] + " " + "-d" + " " +\
					"-dataset_name" + " " + "$datasetpath" + " " +  "-p" + " " +  period + "\n")
			else:

				if args.isFake:
					f.write("python full_Template_postproc.py -f" + " " + filepath + " " + "-y" + " " + dataset['year'] + " " +\
					"-dataset_name" + " " + "$datasetpath" + " " +  "-p" + " " +  period + "\n")

				else:
					f.write("python WZG_postproc.py -f" + " " + filepath + " " + "-y" + " " + dataset['year'] + " " +\
					"-dataset_name" + " " + "$datasetpath" + " " +  "-p" + " " +  period + "\n")
				
		
			#f.write("cp " + datasetname + "/*.root ${initial_path}")
			f.close()


		print "file",str(i),filename," shell prepared" 
		os.system("condor_submit submit_"+datasetname+"_file"+str(i)+"_"+filename+".jdl")
		print "file",str(i),filename," submitted\n" 
		## check just one file

	print "total "+str(i)+" file(s) submitted\n" 
