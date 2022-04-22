import os,sys
import ROOT
import numpy as np
from array import array
from Control_pad import channel_map
from Control_pad import channel
from Control_pad import UpDown_map
from Control_pad import filelist_MC
from Control_pad import branch
from Control_pad import year

if __name__ == '__main__':

	Top_list = ["TTGJets", "TTZToLLNuNu", "TTWJetsToLNu", "tZq_ll"]
	VVV_list = ["WWW","WWZ","ZZZ","WZZ"]
	VV_list = ["qqZZ","ggZZ","WZ","ZGToLLG"]
	index_list = ["None", "jesTotalUp", "jesTotalDown", "jerUp", "jerDown", "MuonIDup", "MuonIDdown", "ElectronIDup", "ElectronIDdown", "ElectronRECOup", "ElectronRECOdown"]

	
	try:
		file_hist = ROOT.TFile(f'./test/{channel_map[channel]}.root',"OPEN")
	except:
		print ("nonvalid root file")
		sys.exit(0)

	new_file_hist = ROOT.TFile(f'./{channel_map[channel]}_{year}.root',"RECREATE")
	new_file_hist.cd()

	# --Loop over Uncs
	for index in index_list:

		# --Loop over physics variables
		for branch_name in branch:
			
			if branch_name != "WZG_mlla": continue;

			hist_Top_list = []
			hist_VVV_list = []
			hist_VV_list = []
			hist_WZG_list = []
			plot_branch = branch[branch_name]["name"]


			# --Loop over file --> append categories
			for file in filelist_MC:
				# print(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{index}')
				hist_temp = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{index}')
				# print(type(hist_temp))

				if filelist_MC[file]["name"] in Top_list:
					hist_Top_list.append(hist_temp)

				elif filelist_MC[file]["name"] in VVV_list:
					hist_VVV_list.append(hist_temp)

				elif filelist_MC[file]["name"] in VV_list or 'ggZZ' in filelist_MC[file]["name"] or 'qqZZ' in filelist_MC[file]["name"]:
					hist_VV_list.append(hist_temp)
				
				elif 'WZG' in filelist_MC[file]["name"]:
					hist_WZG_list.append(hist_temp)
			# <-- End file Loop, append categories

			
			# Merge hist along with categories

			# Top 
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

			# binning, IO
			xbins = [200,400,600,1000,2000]
			nbins = len(xbins) - 1 
			infile="aqgc_reweight/FT0_llA_mass.npy"
			x = np.load(infile,allow_pickle=True)[()]

			# You need just one point, you other points are auto-cal by quadratic-fit
			SFlist_aQGC = x[1]['FT0_3.00E-12']

			# Define histogram
			hist_aQGC  = ROOT.TH1D("hist_aQGC","hist_aQGC",nbins,array("d", xbins))

			# Check bin size
			if nbins != len(SFlist_aQGC):
				raise Exception("Wrong bin size!!")
			
			# Reweight and Fill
			for i in range(1,nbins+1):
				sm_wzg_bin_content  = hist_WZG.GetBinContent(i)
				y_aQGC				= sm_wzg_bin_content * SFlist_aQGC[i-1]
				hist_aQGC.SetBinContent(i,y_aQGC)
			
			hist_aQGC.SetName(f'{channel_map[channel]}_{plot_branch}_aQGC_{index}')
			hist_aQGC.Write()			

			# -- this function will be updated
			#print("MC yields: ",MC_yields)
			#print("SM WZG yields: ",sm_wzg_bin_content)
			#print("FT0_m2e-12 yields: ",h1_aQGC_FT0_m2e_12.Integral(nbins,6), h1_aQGC_FT0_m2e_12.GetBinContent(nbins))
			#print("FT0_1e-12 yields: ",h1_aQGC_FT0_1e_12.Integral(nbins,6), h1_aQGC_FT0_1e_12.GetBinContent(nbins))
			#print("FT0_3e-12 yields: ",h1_aQGC_FT0_3e_12.Integral(nbins,6),h1_aQGC_FT0_3e_12.GetBinContent(nbins))
			#print("FT0_5e-12 yields: ",h1_aQGC_FT0_5e_12.Integral(nbins,6),h1_aQGC_FT0_5e_12.GetBinContent(nbins))


			



	for branch_name in branch:
		plot_branch = branch[branch_name]["name"]
		hist_data = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_data_None')
		hist_data.SetName(f'{channel_map[channel]}_{plot_branch}_data_None')
		hist_data.Write()

		hist_FakeLep = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_FakeLep_None')
		hist_FakeLep.SetName(f'{channel_map[channel]}_{plot_branch}_FakeLep_None')
		hist_FakeLep.Write()

		hist_FakePho = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_FakePho_None')
		hist_FakePho.SetName(f'{channel_map[channel]}_{plot_branch}_FakePho_None')
		hist_FakePho.Write()

	new_file_hist.Close()
	file_hist.Close()
