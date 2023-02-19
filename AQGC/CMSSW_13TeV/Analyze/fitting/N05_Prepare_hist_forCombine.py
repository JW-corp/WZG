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
	index_list = ["None", "jesTotalUp", "jesTotalDown", "jerUp", "jerDown", "MuonIDup", "MuonIDdown", "ElectronIDup", "ElectronIDdown", "ElectronRECOup", "ElectronRECOdown", "puup", "pudown", "l1up", "l1down"]



	parser = argparse.ArgumentParser()
	parser.add_argument('idx', type=int,
				help="The index of reweight factor")
	args = parser.parse_args()

	# Reweight index
	idx = args.idx
	
   
	try:
		file_hist = ROOT.TFile(f'./test/{channel_map[channel]}.root',"OPEN")
	except:
		print ("nonvalid root file")
		sys.exit(0)

	output_directory="Summary_for_HCtool"
	Path(output_directory).mkdir(exist_ok=True,parents=True)
	new_file_hist = ROOT.TFile(f'{output_directory}/{channel_map[channel]}_{year}_Rwt{idx}.root',"RECREATE")
	new_file_hist.cd()

	


	# Merge hist
	for index in index_list:

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

			for file in filelist_MC:

				# Condition for LHE rewegiht "aQGC"
				if filelist_MC[file]['name'] == "aQGC":
					hist_temp = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{index}_Rwt{idx}')
					hist_aQGC_list.append(hist_temp)

				# Non-reweight case
				else:
					# print(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{index}')
					hist_temp = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{index}')
					# print(type(hist_temp))

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

		hist_FakePho = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_FakePho_None')
		hist_FakePho.SetName(f'{channel_map[channel]}_{plot_branch}_FakePho_None')
		hist_FakePho.Write()

	#c1 = ROOT.TCanvas("","",1000,1000)
	#c1.Draw()
	#pad1 = ROOT.TPad("pad1", "pad1", 0, 0.30, 1, 1.00)
	#pad1.SetTopMargin(0.1)  # joins upper and lower plot
	##pad1.SetBottomMargin(0.035)  # joins upper and lower plot
	#pad1.SetBottomMargin(0.065)  # joins upper and lower plot
	## pad1.SetGridx()
	#pad1.Draw()
	## Lower ratio plot is pad2
	#c1.cd()  # returns to main canvas before defining pad2
	#pad2 = ROOT.TPad("pad2", "pad2", 0, 0.00, 1, 0.30)
	##pad2.SetTopMargin(0.040)  # joins upper and lower plot
	#pad2.SetTopMargin(0.060)  # joins upper and lower plot
	#pad2.SetBottomMargin(0.40)  # joins upper and lower plot
	#pad2.SetGridy()
	#pad2.Draw()

	## draw everything
	#pad1.cd()
	#hist_Top.SetLineColor(4)
	#hist_Top.SetFillColor(4)

	#hist_VVV.SetLineColor(7)
	#hist_VVV.SetFillColor(7)

	#hist_VV.SetLineColor(3)
	#hist_VV.SetFillColor(3)

	#hist_VG.SetLineColor(6)
	#hist_VG.SetFillColor(6)
	#
	#hist_WZG.SetLineColor(9)
	#hist_WZG.SetFillColor(9)
	#
	#hist_aQGC.SetLineColor(2)
	#hist_aQGC.SetFillColor(0)
	#hist_aQGC.SetLineWidth(4)

	#legend = ROOT.TLegend(0.20, 0.65, 0.85, 0.85)
	#legend.SetNColumns(2)
	#legend.SetBorderSize(0)
	#legend.SetFillColor(0)
	#legend.SetTextSize(0.035)
	#legend.SetLineWidth(1)
	#legend.SetLineStyle(0)
	#	
	#legend.AddEntry( hist_Top ,'Top','F')
	#legend.AddEntry( hist_VVV ,'VVV','F')
	#legend.AddEntry( hist_VV  ,'VV','F')
	#legend.AddEntry( hist_VG  ,'VG','F')
	#legend.AddEntry( hist_WZG ,'WZG','F')
	#legend.AddEntry( hist_aQGC,'aQGC','L')

	#hist_Top.Draw("HIST")
	#hist_VVV.Draw("HIST SAME")
	#hist_VV.Draw("HIST SAME")
	#hist_VG.Draw("HIST SAME")
	#hist_WZG.Draw("HIST SAME")
	#hist_aQGC.Draw("HIST SAME")
	#legend.Draw("SAME")

	#c1.Print("MergedPlot.png")
	new_file_hist.Close()
	file_hist.Close()
