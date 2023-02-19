import matplotlib
import numpy
import numba
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
import pandas as pd
from tqdm import trange
import ROOT
import os,sys
from array import array
from copy import deepcopy
import time
import awkward as ak
import uproot



from AddHist_help_aQGC import AddHist
from AddHist_help_aQGC import AddHist_FakeLepton
from AddHist_help_aQGC import AddHist_FakePhoton
from AddHist_help_aQGC import SetHistStyle


from Control_pad import channel_map
from Control_pad import channel
from Control_pad import UpDown_map
from Control_pad import filelist_data
from Control_pad import filelist_MC
from Control_pad import branch
from Control_pad import lumi
from pathlib import Path


		
sys.path.append('..')
from lumi import CMS_lumi
from ratio import createRatio


def Prepare_hist():

	time_total_init = time.time()


	# --> Process MC
	for file in filelist_MC:
		hist_MC = {}
		for branch_name in branch:
			plot_branch = branch[branch_name]["name"]
			if branch[branch_name].__contains__("bin_array"):
				hist_MC_temp = ROOT.TH1F("", "", len(branch[branch_name]["bin_array"])-1, array('d', branch[branch_name]["bin_array"]))
			else:
				hist_MC_temp = ROOT.TH1F("", "", branch[branch_name]["xbins"], branch[branch_name]["xleft"], branch[branch_name]["xright"])
			SetHistStyle(hist_MC_temp, filelist_MC[file]["color"])
			hist_MC_temp.SetXTitle(f'{branch[branch_name]["axis_name"]}')

			
			# >> Add this block to only fill WZG mllla
			if filelist_MC[file]["name"] == "aQGC":
				print("----is aQGC 0------",branch_name,file)
				Rwt = uproot.open(filelist_MC[file]["path"])["Events/LHEReweightingWeight"].array()[0]
				#Rwt=[0]
				for i in range(len(Rwt)):

					for UpDown in range(0,5):
						hist_MC[plot_branch+f"_{UpDown_map[UpDown]}_Rwt{i}"] = deepcopy(hist_MC_temp)
					hist_MC[plot_branch+f"_MuonIDup_Rwt{i}"] = deepcopy(hist_MC_temp)
					hist_MC[plot_branch+f"_MuonIDdown_Rwt{i}"] = deepcopy(hist_MC_temp)
					hist_MC[plot_branch+f"_ElectronIDup_Rwt{i}"] = deepcopy(hist_MC_temp)
					hist_MC[plot_branch+f"_ElectronIDdown_Rwt{i}"] = deepcopy(hist_MC_temp)
					hist_MC[plot_branch+f"_ElectronRECOup_Rwt{i}"] = deepcopy(hist_MC_temp)
					hist_MC[plot_branch+f"_ElectronRECOdown_Rwt{i}"] = deepcopy(hist_MC_temp)
					hist_MC[plot_branch+f"_l1up_Rwt{i}"] = deepcopy(hist_MC_temp)
					hist_MC[plot_branch+f"_l1down_Rwt{i}"] = deepcopy(hist_MC_temp)
					hist_MC[plot_branch+f"_puup_Rwt{i}"] = deepcopy(hist_MC_temp)
					hist_MC[plot_branch+f"_pudown_Rwt{i}"] = deepcopy(hist_MC_temp)
			else:
				for UpDown in range(0,5):
					hist_MC[plot_branch+f"_{UpDown_map[UpDown]}"] = deepcopy(hist_MC_temp)
				hist_MC[plot_branch+f"_MuonIDup"] = deepcopy(hist_MC_temp)
				hist_MC[plot_branch+f"_MuonIDdown"] = deepcopy(hist_MC_temp)
				hist_MC[plot_branch+f"_ElectronIDup"] = deepcopy(hist_MC_temp)
				hist_MC[plot_branch+f"_ElectronIDdown"] = deepcopy(hist_MC_temp)
				hist_MC[plot_branch+f"_ElectronRECOup"] = deepcopy(hist_MC_temp)
				hist_MC[plot_branch+f"_ElectronRECOdown"] = deepcopy(hist_MC_temp)
				hist_MC[plot_branch+f"_l1up"] = deepcopy(hist_MC_temp)
				hist_MC[plot_branch+f"_l1down"] = deepcopy(hist_MC_temp)
				hist_MC[plot_branch+f"_puup"] = deepcopy(hist_MC_temp)
				hist_MC[plot_branch+f"_pudown"] = deepcopy(hist_MC_temp)
		
				
		print(f"Processing {file}")
		AddHist(filelist_MC[file]["path"], hist_MC, 0, filelist_MC[file]["xsec"], lumi, channel, branch)
		filelist_MC[file]["hist"] = hist_MC

	# --> Process Fake Photon
	hist_FakePho= {}
	for branch_name in branch:
		plot_branch = branch[branch_name]["name"]
		if branch[branch_name].__contains__("bin_array"):
			hist_FakePho_temp = ROOT.TH1F("", "", len(branch[branch_name]["bin_array"])-1, array('d', branch[branch_name]["bin_array"]))
		else:
			hist_FakePho_temp = ROOT.TH1F("", "", branch[branch_name]["xbins"], branch[branch_name]["xleft"], branch[branch_name]["xright"])
		hist_FakePho_temp.SetXTitle(f'{branch[branch_name]["axis_name"]}')
		hist_FakePho_temp.SetYTitle(f'events / bin')
		SetHistStyle(hist_FakePho_temp,30)
		hist_FakePho[plot_branch] = deepcopy(hist_FakePho_temp)

	if channel in [0,1,2,3,4,20,21,22,23,24,30,31,32]:
		for file in filelist_data:
			AddHist_FakePhoton(file, hist_FakePho, 1, 0, 0, channel, branch)
		for file in filelist_MC:

			# - Pass aQGC (since there is no list of Fake Lepton, MC and FakeLepton modules are merged)
			if filelist_MC[file]['name'] == 'aQGC':
				continue

			AddHist_FakePhoton(filelist_MC[file]["path"], hist_FakePho, 0, filelist_MC[file]["xsec"], lumi, channel, branch)
	else:
		pass

	# --> Process Data 
	hist_data = {}
	for branch_name in branch:
		plot_branch = branch[branch_name]["name"]
		if branch[branch_name].__contains__("bin_array"):
			hist_data_temp = ROOT.TH1F("", "", len(branch[branch_name]["bin_array"])-1, array('d', branch[branch_name]["bin_array"]))
		else:
			hist_data_temp = ROOT.TH1F("", "", branch[branch_name]["xbins"], branch[branch_name]["xleft"], branch[branch_name]["xright"])
		hist_data_temp.SetXTitle(f'{branch[branch_name]["axis_name"]}')
		hist_data_temp.SetYTitle(f'events / bin')
		SetHistStyle(hist_data_temp, 1)
		hist_data[plot_branch] = deepcopy(hist_data_temp)
	for file in filelist_data:
		AddHist(file, hist_data, 1, 0, 0, channel, branch)

	
	# --> Process Fake Lepton
	hist_FakeLep = {}
	for branch_name in branch:
		plot_branch = branch[branch_name]["name"]
		if branch[branch_name].__contains__("bin_array"):
			hist_FakeLep_temp = ROOT.TH1F("", "", len(branch[branch_name]["bin_array"])-1, array('d', branch[branch_name]["bin_array"]))
		else:
			hist_FakeLep_temp = ROOT.TH1F("", "", branch[branch_name]["xbins"], branch[branch_name]["xleft"], branch[branch_name]["xright"])
		hist_FakeLep_temp.SetXTitle(f'{branch[branch_name]["axis_name"]}')
		hist_FakeLep_temp.SetYTitle(f'events / bin')
		SetHistStyle(hist_FakeLep_temp,23)
		hist_FakeLep[plot_branch] = deepcopy(hist_FakeLep_temp)
	for file in filelist_data:
		AddHist_FakeLepton(file, hist_FakeLep, 1, 0, 0, channel, branch)
	for file in filelist_MC:
		
		# - Pass aQGC (since there is no list of Fake Lepton, MC and FakeLepton modules are merged)
		if filelist_MC[file]['name'] == 'aQGC':
			continue

		AddHist_FakeLepton(filelist_MC[file]["path"], hist_FakeLep, 0, filelist_MC[file]["xsec"], lumi, channel, branch)



	
	# --- Write all!
	output_directory="test"
	Path(output_directory).mkdir(exist_ok=True,parents=True)
	file_hist = ROOT.TFile(f'./test/{channel_map[channel]}.root',"RECREATE")
	file_hist.cd()
	for branch_name in branch:


		if branch_name != "WZG_mllla":
			continue

		plot_branch = branch[branch_name]["name"]

		hist_data[plot_branch].SetName(f"{channel_map[channel]}_{plot_branch}_data_{str(UpDown_map[0])}")
		hist_FakeLep[plot_branch].SetName(f"{channel_map[channel]}_{plot_branch}_FakeLep_{str(UpDown_map[0])}")
		hist_FakePho[plot_branch].SetName(f"{channel_map[channel]}_{plot_branch}_FakePho_{str(UpDown_map[0])}")
		hist_data[plot_branch].Write()
		hist_FakeLep[plot_branch].Write()
		hist_FakePho[plot_branch].Write()

		for file in filelist_MC:

			if filelist_MC[file]["name"] == "aQGC":

		
				for i in range(len(Rwt)):
			
					# --reweight
					for UpDown in range(0,5):
						filelist_MC[file]["hist"][plot_branch+f"_{UpDown_map[UpDown]}_Rwt{i}"].SetName(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{str(UpDown_map[UpDown])}_Rwt{i}')
						filelist_MC[file]["hist"][plot_branch+f"_{UpDown_map[UpDown]}_Rwt{i}"].Write()
					#updown
						filelist_MC[file]["hist"][plot_branch+f"_MuonIDup_Rwt{i}"].SetName(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_MuonIDup_Rwt{i}')
						filelist_MC[file]["hist"][plot_branch+f"_MuonIDup_Rwt{i}"].Write()
						filelist_MC[file]["hist"][plot_branch+f"_MuonIDdown_Rwt{i}"].SetName(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_MuonIDdown_Rwt{i}')
						filelist_MC[file]["hist"][plot_branch+f"_MuonIDdown_Rwt{i}"].Write()
						filelist_MC[file]["hist"][plot_branch+f"_ElectronIDup_Rwt{i}"].SetName(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_ElectronIDup_Rwt{i}')
						filelist_MC[file]["hist"][plot_branch+f"_ElectronIDup_Rwt{i}"].Write()
						filelist_MC[file]["hist"][plot_branch+f"_ElectronIDdown_Rwt{i}"].SetName(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_ElectronIDdown_Rwt{i}')
						filelist_MC[file]["hist"][plot_branch+f"_ElectronIDdown_Rwt{i}"].Write()
						filelist_MC[file]["hist"][plot_branch+f"_ElectronRECOup_Rwt{i}"].SetName(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_ElectronRECOup_Rwt{i}')
						filelist_MC[file]["hist"][plot_branch+f"_ElectronRECOup_Rwt{i}"].Write()
						filelist_MC[file]["hist"][plot_branch+f"_ElectronRECOdown_Rwt{i}"].SetName(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_ElectronRECOdown_Rwt{i}')
						filelist_MC[file]["hist"][plot_branch+f"_ElectronRECOdown_Rwt{i}"].Write()
						filelist_MC[file]["hist"][plot_branch+f"_l1up_Rwt{i}"].SetName(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_l1up_Rwt{i}')
						filelist_MC[file]["hist"][plot_branch+f"_l1up_Rwt{i}"].Write()
						filelist_MC[file]["hist"][plot_branch+f"_l1down_Rwt{i}"].SetName(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_l1down_Rwt{i}')
						filelist_MC[file]["hist"][plot_branch+f"_l1down_Rwt{i}"].Write()
						filelist_MC[file]["hist"][plot_branch+f"_puup_Rwt{i}"].SetName(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_puup_Rwt{i}')
						filelist_MC[file]["hist"][plot_branch+f"_puup_Rwt{i}"].Write()
						filelist_MC[file]["hist"][plot_branch+f"_pudown_Rwt{i}"].SetName(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_pudown_Rwt{i}')
						filelist_MC[file]["hist"][plot_branch+f"_pudown_Rwt{i}"].Write()

			else:

				# --Non reweight
				#Nominal + JES JER updown
				for UpDown in range(0,5):
					filelist_MC[file]["hist"][plot_branch+f"_{UpDown_map[UpDown]}"].SetName(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{str(UpDown_map[UpDown])}')
					filelist_MC[file]["hist"][plot_branch+f"_{UpDown_map[UpDown]}"].Write()
				#updown
					filelist_MC[file]["hist"][plot_branch+f"_MuonIDup"].SetName(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_MuonIDup')
					filelist_MC[file]["hist"][plot_branch+f"_MuonIDup"].Write()
					filelist_MC[file]["hist"][plot_branch+f"_MuonIDdown"].SetName(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_MuonIDdown')
					filelist_MC[file]["hist"][plot_branch+f"_MuonIDdown"].Write()
					filelist_MC[file]["hist"][plot_branch+f"_ElectronIDup"].SetName(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_ElectronIDup')
					filelist_MC[file]["hist"][plot_branch+f"_ElectronIDup"].Write()
					filelist_MC[file]["hist"][plot_branch+f"_ElectronIDdown"].SetName(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_ElectronIDdown')
					filelist_MC[file]["hist"][plot_branch+f"_ElectronIDdown"].Write()
					filelist_MC[file]["hist"][plot_branch+f"_ElectronRECOup"].SetName(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_ElectronRECOup')
					filelist_MC[file]["hist"][plot_branch+f"_ElectronRECOup"].Write()
					filelist_MC[file]["hist"][plot_branch+f"_ElectronRECOdown"].SetName(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_ElectronRECOdown')
					filelist_MC[file]["hist"][plot_branch+f"_ElectronRECOdown"].Write()
					filelist_MC[file]["hist"][plot_branch+f"_l1up"].SetName(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_l1up')
					filelist_MC[file]["hist"][plot_branch+f"_l1up"].Write()
					filelist_MC[file]["hist"][plot_branch+f"_l1down"].SetName(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_l1down')
					filelist_MC[file]["hist"][plot_branch+f"_l1down"].Write()
					filelist_MC[file]["hist"][plot_branch+f"_puup"].SetName(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_puup')
					filelist_MC[file]["hist"][plot_branch+f"_puup"].Write()
					filelist_MC[file]["hist"][plot_branch+f"_pudown"].SetName(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_pudown')
					filelist_MC[file]["hist"][plot_branch+f"_pudown"].Write()
	file_hist.Close()

	print (time.time()-time_total_init)

if __name__ == "__main__":
	sys.exit(Prepare_hist())
