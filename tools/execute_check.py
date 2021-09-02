import glob
import subprocess





##### -----Please add input hist list here
sample_name = 'Egamma'
file_list  = glob.glob("/x6/cms/skim_2ElIdPt10_Electron_channel/x6/cms/store/data/Run2018*/EGamma/*/*/*/*.root")


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


	fn_out = sample_name + "_" + str(i) + ".npy"


	print("############################## SET: ",fn_out)
	print(infiles)
	
	# Run specific excutable codes
	args = 'python' + ' '+ 'check.py' + ' ' + '--outname' + ' ' + fn_out + ' '+  infiles
	subprocess.call(args,shell=True)
