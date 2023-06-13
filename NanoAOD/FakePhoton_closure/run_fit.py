import subprocess
import pathlib

import argparse




def execute(strs):
	for isochg in IsoChg_sb:
		#args = strs + ' ' + isochg + ' ' + '--isclosure False'
		args = strs + ' ' + isochg + ' ' + '--isclosure True'

		print(args)
		subprocess.call(args,shell=True)


if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument('region', type=str,
				help="EB_PT1 ~ EB_PT5 EE_PT1 ~ EE_PT2")
	args = parser.parse_args()
	
	
	

	# All SB
	low_isochg		= list(range(3,9,1))
	high_isochg		= list(range(8,14,1))
	IsoChg_sb		= []
	
	for l,low in enumerate(low_isochg):
		for h,high in enumerate(high_isochg):
			if l > h:
				continue
			
			name = f"from_{low}_to_{high}"
			IsoChg_sb.append(name)		

	# --Just test for one SB
	IsoChg_sb = ["from_4_to_10"]

	pt_bin = args.region
	#execute(f"python n02_FakePhoton_CR_template_Fit2016.py {pt_bin}") # 2016
	#execute(f"python n02_FakePhoton_CR_template_Fit2017.py {pt_bin}") # 2017 
	execute(f"python n02_FakePhoton_CR_template_Fit2018.py {pt_bin}") # 2018

