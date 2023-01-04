import sys,os
import argparse
import re
import optparse
sys.path.append('..')
import json


parser = argparse.ArgumentParser(description='condor for postproc')
parser.add_argument('-f', dest='file', default='', help='json file input')
parser.add_argument('-y', dest='year', default='2018', help='year')
parser.add_argument('-isFakeFR',type=bool, default=False, help='json file input')
parser.add_argument('-isFakeAR',type=bool, default=False, help='json file input')
args = parser.parse_args()

year = args.year

with open(args.file, "r") as f:
	jsons = json.load(f)
	f.close()

#initial_path = os.getcwd()

import glob
# Dataset Loop
for dataset in jsons:
	
#	os.chdir(initial_path)


	## data/MC type setting
	isdata=False # initilize isdata 
	period='B' # initialize period
	if dataset['type'] !='MC':
		isdata=True

	# MC case
	if not isdata:

		# Private signal case
		if dataset['name'].startswith("/x5/cms/jwkim/store/signal"):
			datasetname = dataset['name'].split('/')[6].split('_')[0] + '_' + dataset['year']

		# General case
		else:
			#datasetname = dataset['name'].split('/')[6].split('_')[0] + '_' + dataset['year']
			datasetname = dataset['name'].split('/')[6]  + '_' + dataset['year']
			
	# Data case
	else:
		run_name	= dataset['name'].split('/')[5]
		data_name   = dataset['name'].split('/')[6]
		period	  = run_name[7]
		datasetname = data_name + '_' + run_name + '_' + dataset['year']
		
	
	## make save directory
	os.system("mkdir -p "+datasetname+"/log")
	os.system("mkdir -p "+datasetname+"/condorOut")
	os.chdir(datasetname)

	flist = glob.glob(dataset['name'])
	i = 0
	for i,filepath in enumerate(flist):

		# Prepare1 submit	
		filename = filepath.split('/')[-1].split('_')[0]
		#print("##"*20)
		#print("dataset: ",datasetname)
		#print("fname: ",filename)
		#print("path: ",filepath)



		## -->>  submit.jds script
		with open ("submit_"+datasetname+"_file"+str(i)+"_"+filename+".jdl","w+") as f:
			f.write("universe \t = vanilla\n")
			f.write("executable \t = wrapper_"+datasetname+"_file"+str(i)+"_"+filename+".sh\n")
			f.write("error \t = log/"+datasetname+"_file"+str(i)+"_"+filename+".err\n")
			f.write("output \t = log/"+datasetname+"_file"+str(i)+"_"+filename+".output\n")
			f.write("log \t = log/"+datasetname+"_file"+str(i)+"_"+filename+".log\n\n")
			f.write('requirements = (machine == "node01")||(machine == "node02")||(machine == "node03") ||(machine == "node04")\n')
			f.write("should_transfer_files \t = YES\n")
			f.write("when_to_transfer_output \t = ON_EXIT\n")
			f.write("transfer_output_files \t = condorOut\n")
			f.write("queue 1")
		f.close()
		print "file",str(i),filename," submit code prepared" 



		## -->>  run scruipt
		with open ("wrapper_"+datasetname+"_file"+str(i)+"_"+filename+".sh","w+") as f:
			f.write("#!/bin/bash\n\n")
			f.write("condorOut\n\n")

			# set path
			f.write("home_path=${PWD}\n\n")

			# set CMSENV				
			f.write("export SCRAM_ARCH=slc7_amd64_gcc700\n")
			f.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
			
			# !!! You need to modity your path!!!
			f.write("cd /x5/cms/jwkim/gitdir/JWCorp/JW_analysis/for_graduation2022/CMSSW_10_6_19/src\n")
			f.write("eval `scramv1 runtime -sh`\n")
			f.write("echo $CMSSW_BASE\n\n")



			# set NanoAOD tool and run jobs
			if args.isFakeFR or args.isFakeAR:
				f.write("cd PhysicsTools/NanoAODTools/nanoAOD-WVG/FakePhoton\n")
			else:
				f.write("cd PhysicsTools/NanoAODTools/nanoAOD-WVG/WZG_selector\n")

			# >> This part make "su" directories
			#f.write("[[ -d " + datasetname + " ]]" + " || " +  " mkdir " +  datasetname + "\n")

			# Need absolute path here
			f.write("datasetpath=$home_path/condorOut/" + datasetname + "\n")

			
			if isdata:
				
				if args.isFakeFR:
					f.write("python CR_full_Template_postproc.py -f" + " " + filepath + " " + "-y" + " " + year + " " + "-d" + " " +\
					"-dataset_name" + " " + "$datasetpath" + " " +  "-p" + " " +  period + "\n")
					
				elif args.isFakeAR:
					f.write("python full_Template_postproc.py -f" + " " + filepath + " " + "-y" + " " + year + " " + "-d" + " " +\
					"-dataset_name" + " " + "$datasetpath" + " " +  "-p" + " " +  period + "\n")

				else:
					f.write("python WZG_postproc.py -f" + " " + filepath + " " + "-y" + " " + year + " " + "-d" + " " +\
					"-dataset_name" + " " + "$datasetpath" + " " +  "-p" + " " +  period + "\n")
			else:

				if args.isFakeFR:
					f.write("python CR_full_Template_postproc.py -f" + " " + filepath + " " + "-y" + " " + year + " " +\
					"-dataset_name" + " " + "$datasetpath" + " " +  "-p" + " " +  period + "\n")

				elif args.isFakeAR:
					f.write("python full_Template_postproc.py -f" + " " + filepath + " " + "-y" + " " + year + " " +\
					"-dataset_name" + " " + "$datasetpath" + " " +  "-p" + " " +  period + "\n")

				else:
					f.write("python WZG_postproc.py -f" + " " + filepath + " " + "-y" + " " + year + " " +\
					"-dataset_name" + " " + "$datasetpath" + " " +  "-p" + " " +  period + "\n")
				
			
			#f.write("cp " + datasetname + "/*.root ${initial_path}")
			f.close()


		print "file",str(i),filename," shell prepared" 
		os.system("condor_submit submit_"+datasetname+"_file"+str(i)+"_"+filename+".jdl")
		print "file",str(i),filename," submitted\n" 


	print "total "+str(i)+" file(s) submitted\n" 
