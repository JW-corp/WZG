import glob


# This program works in below file structures

# dir1
	# --submit1.jdl submit2.jdl ....
	# --out1.root out2.root ....
	# --log
		# --condor1.output condor2.output

# When you accidently kill the condor_job, this program find the killed job and provide list for the rerun





def failfile_finder(required_files,output_files,rootout_files):


	# 1. required vs output 
	fail_list_output_memory=[]
	if len(required_files) != len(output_files):

		for fout in required_files:
			tmp = fout.replace('jdl','output')
			tmp = tmp.replace('submit_','log/')

			if not tmp in output_files:
				fail_list_output_memory.append(fout)	

	


	# 2. required vs root
	fail_list_root_memory=[]
	if len(required_files) != len(rootout_files):

		for fout in required_files:
			tmp = fout.replace('jdl','root')
			tmp = tmp.replace('submit_','')

			if not tmp in rootout_files:
				fail_list_root_memory.append(fout)	
		

	fail_list = list(set(fail_list_output_memory) | set(fail_list_root_memory))
	print(f"{len(required_files)} requested {len(output_files)} outputs  {len(rootout_files)} root outputs check {len(fail_list)} failed files below")
	for idx,f in enumerate(fail_list):
		print(idx+1,f)
		
	return fail_list


def rm_failed_file(fa_list):
	

	with open ("remove_failed_list.sh","w+") as f:

		f.write("## Do you really want to remove these files? \n")
		for fa in fa_list:
		
			tmp = 'log/' + fa.replace('jdl','output')

			f.write(f"rm {fa.replace('jdl','root')}\n")
			f.write(f"rm {tmp}\n")
		
		
if __name__ == "__main__":

	required_files = glob.glob("submit*")
	output_files   = glob.glob("log/*.output")
	rootout_files  = glob.glob("*.root")
		
	fail_list = failfile_finder(required_files,output_files,rootout_files)
	rm_failed_file(fail_list)
	
	with open ("rerun_failed_list.sh","w+") as f:
	
		f.write("## Do you really want to run these files? \n")
		for fa in fail_list:
	
			f.write(f"condor_submit {fa}\n")



# test one file: submit_WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8_2016Post_file4_7B26075C-9224-8C47-A3BE-A6DE2FACE30D.root.jdl
