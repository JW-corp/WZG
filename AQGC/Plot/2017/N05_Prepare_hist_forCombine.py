import os,sys
import ROOT

sys.path.append(os.getcwd())
from Control_pad import channel_map
from Control_pad import channel
from Control_pad import UpDown_map
from Control_pad import filelist_MC
from Control_pad import branch
from Control_pad import year

import argparse
from pathlib import Path



if __name__ == '__main__':



	Top_list = ["ttgjets", "ttztollnunu", "ttztoll", "ttwjetstolnu", "tttt", "tZq_ll", "st antitop", "st top"]
	VVV_list = ["www","wwz","zzz","wzz"]
	VV_list = ["qqzz","ggzz","wz"]
	VG_list = ["zgtollg","wgtolnug"]
	index_list = ["None", "jesTotalUp", "jesTotalDown", "jerUp", "jerDown", "MuonIDup", "MuonIDdown", "ElectronIDup", "ElectronIDdown", "ElectronRECOup", "ElectronRECOdown", "puup", "pudown", "l1up", "l1down","PhotonIDup","PhotonIDdown"]

	parser = argparse.ArgumentParser()
	parser.add_argument('idx', type=int,
				help="The index of reweight factor")
	args = parser.parse_args()

	# Reweight index
	idx = args.idx
 
	# Read File   
	try:
		file_hist = ROOT.TFile(f'./test/{channel_map[channel]}.root',"OPEN")
	except:
		print ("nonvalid root file")
		sys.exit(0)
	# Write File

	output_directory="Summary_for_HCtool"
	Path(output_directory).mkdir(exist_ok=True,parents=True)
	new_file_hist = ROOT.TFile(f'{output_directory}/{channel_map[channel]}_{year}_Rwt{idx}.root',"RECREATE")
	new_file_hist.cd()



	# Merge hist
	for index in index_list:


		## ----  Write MC sample
		for branch_name in branch:


			# >> Only consider WZG mllla
			if branch_name != "WZG_mllla":
				continue
			# <<



			hist_Top_list = []
			hist_VVV_list = []
			hist_VV_list = []
			hist_VG_list = []
			hist_WZG_list = []
			hist_aQGC_list = []
			plot_branch = branch[branch_name]["name"]

			## Setup Categories
			for file in filelist_MC:


				# Condition for LHE rewegiht "aQGC"
				if filelist_MC[file]['name'] == "aQGC":
					hist_temp = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{index}_Rwt{idx}')
					hist_aQGC_list.append(hist_temp)


				else:
					# print(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{index}')
					hist_temp = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{index}')
					

					if filelist_MC[file]["name"].lower() in Top_list:
						hist_Top_list.append(hist_temp)

					elif filelist_MC[file]["name"].lower() in VVV_list:
						hist_VVV_list.append(hist_temp)

					elif filelist_MC[file]["name"].lower() in VV_list or 'ggZZ' in filelist_MC[file]["name"] or 'qqZZ' in filelist_MC[file]["name"]:
						hist_VV_list.append(hist_temp)
					
					elif filelist_MC[file]["name"].lower() in VG_list:
						hist_VG_list.append(hist_temp)

					elif 'WZG' in filelist_MC[file]["name"]:
						hist_WZG_list.append(hist_temp)

								

			# TOP
			if len(hist_Top_list) > 0:
				hist_Top = hist_Top_list[0].Clone()
				for i in range(1, len(hist_Top_list)):
					hist_Top.Add(hist_Top_list[i])
				hist_Top.SetName(f'{channel_map[channel]}_{plot_branch}_Top_{index}')
				hist_Top.Write()

			# VVV
			if len(hist_VVV_list) > 0:
				hist_VVV = hist_VVV_list[0].Clone()
				for i in range(1, len(hist_VVV_list)):
					hist_VVV.Add(hist_VVV_list[i])
				hist_VVV.SetName(f'{channel_map[channel]}_{plot_branch}_VVV_{index}')
				hist_VVV.Write()

			# VV
			if len(hist_VV_list) > 0:
				hist_VV = hist_VV_list[0].Clone()
				for i in range(1, len(hist_VV_list)):
					hist_VV.Add(hist_VV_list[i])
				hist_VV.SetName(f'{channel_map[channel]}_{plot_branch}_VV_{index}')
				hist_VV.Write()

			# VG
			if len(hist_VG_list) > 0:
				hist_VG = hist_VG_list[0].Clone()
				for i in range(1, len(hist_VG_list)):
					hist_VG.Add(hist_VG_list[i])
				hist_VG.SetName(f'{channel_map[channel]}_{plot_branch}_VG_{index}')
				hist_VG.Write()


			# WZG
			if len(hist_WZG_list) == 0:
				print('!!!Warning: No signal input!!!')
			else:
				hist_WZG = hist_WZG_list[0].Clone()
				if len(hist_WZG_list) > 1:
					print('!!!Warning: More than 1 signal input!!!')
					for i in range(1, len(hist_WZG_list)):
						hist_WZG.Add(hist_WZG_list[i])
				hist_WZG.SetName(f'{channel_map[channel]}_{plot_branch}_WZG_{index}')
				hist_WZG.Write()

			# aQGC
			if len(hist_aQGC_list) == 0:
				print('!!!Warning: No signal input!!!')
			else:
				hist_aQGC = hist_aQGC_list[0].Clone()
				if len(hist_aQGC_list) > 1:
					print('!!!Warning: More than 1 signal input!!!')
					for i in range(1, len(hist_aQGC_list)):
						hist_aQGC.Add(hist_aQGC_list[i])
				hist_aQGC.SetName(f'{channel_map[channel]}_{plot_branch}_aQGC_{index}_Rwt{idx}')
				hist_aQGC.Write()


	for branch_name in branch:
		# >> Only consider WZG mllla
		if branch_name != "WZG_mllla":
			continue
		# <<
	
		plot_branch = branch[branch_name]["name"]
		hist_data = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_data_None')
		hist_data.SetName(f'{channel_map[channel]}_{plot_branch}_data_None')
		hist_data.Write()
	
		hist_FakeLep = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_FakeLep_None')
		hist_FakeLep.SetName(f'{channel_map[channel]}_{plot_branch}_FakeLep_None')
		hist_FakeLep.Write()

		hist_FakeLep_sys_up = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_FakeLep_sys_up')
		hist_FakeLep_sys_up.SetName(f'{channel_map[channel]}_{plot_branch}_FakeLep_sys_up')
		hist_FakeLep_sys_up.Write()
		
		hist_FakeLep_sys_down = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_FakeLep_sys_down')
		hist_FakeLep_sys_down.SetName(f'{channel_map[channel]}_{plot_branch}_FakeLep_sys_down')
		hist_FakeLep_sys_down.Write()

		hist_FakeLep_stat_up = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_FakeLep_stat_up')
		hist_FakeLep_stat_up.SetName(f'{channel_map[channel]}_{plot_branch}_FakeLep_stat_up')
		hist_FakeLep_stat_up.Write()

		hist_FakeLep_stat_down = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_FakeLep_stat_down')
		hist_FakeLep_stat_down.SetName(f'{channel_map[channel]}_{plot_branch}_FakeLep_stat_down')
		hist_FakeLep_stat_down.Write()
	
		hist_FakePho = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_FakePho_None')
		hist_FakePho.SetName(f'{channel_map[channel]}_{plot_branch}_FakePho_None')
		hist_FakePho.Write()

	new_file_hist.Close()
	file_hist.Close()
