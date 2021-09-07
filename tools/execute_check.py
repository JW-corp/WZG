import glob
import subprocess
import argparse

##### -----Please add input hist list here

parser = argparse.ArgumentParser()
parser.add_argument('--name', help='outname')
args  =parser.parse_args()
sample_name = args.name
file_list = glob.glob("../skim_2ElIdPt10_Electron_channel/x6/cms/store/data/*/SingleMuon/*/*/*/*.root")


if sample_name =='Egamma':
	file_list  = glob.glob("/x6/cms/skim_2ElIdPt10_Electron_channel/x6/cms/store/data/Run2018*/EGamma/*/*/*/*.root") +  glob.glob("/x5/cms/jwkim/anaNanoAOD/skimNanoAOD/skim_2ElIdPt20_RunC/x6/cms/store/data/Run2018C/EGamma/NANOAOD/UL2018_MiniAODv1_NanoAODv2-v1/*/*.root")

if sample_name == 'SingleMuon':
	file_list = glob.glob("../skim_2ElIdPt10_Electron_channel/x6/cms/store/data/*/SingleMuon/*/*/*/*.root")

#if sample_name == 'EGamma':
#	file_list  = glob.glob("/x6/cms/skim_2ElIdPt10_Electron_channel/x6/cms/store/data/Run2018*/EGamma/*/*/*/*.root")

if sample_name == 'DoubleMuon':
	file_list = glob.glob("/x6/cms/skim_2ElIdPt10_Electron_channel/x6/cms/store/data/*/DoubleMuon/NANOAOD/*/*/*.root")

if sample_name == 'MuonEG':
	file_list = glob.glob("/x6/cms/skim_2ElIdPt10_Electron_channel/x6/cms/store/data/*/MuonEG/*/*/*/*.root")






def calc_Nout(maxfile,nfile):
	nfile = maxfile + nfile - 1
	nout = int(nfile / maxfile)
	return(nout)




##### -----Please add batch size here 
maxfile=50 # Max number of input files for each run 

nfile=len(file_list) #  Number of total input files
nout  = calc_Nout(maxfile,nfile) # Number of output files
for i in range(nout):
	start = i*maxfile 
	end = start + maxfile 
	
	infiles = (' '.join(file_list[start:end]))
	print(infiles)

	fn_out = sample_name + "_" + str(i) + ".npy"


	print("############################## SET: ",fn_out)
	#print(infiles)

	
	# Run specific excutable codes
	args = 'python' + ' '+ 'check.py' + ' ' + '--outname' + ' ' + fn_out + ' '+  infiles
	subprocess.call(args,shell=True)
