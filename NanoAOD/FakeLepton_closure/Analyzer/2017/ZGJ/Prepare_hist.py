import matplotlib
import uproot
import numpy
import awkward
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

from pathlib import Path

sys.path.append('..')
sys.path.append(os.getcwd())
from lumi import CMS_lumi
from AddHist_help import AddHist
from AddHist_help import AddHist_FakeLepton
#from AddHist_help import AddHist_FakePhoton
from AddHist_help import SetHistStyle
from ratio import createRatio
from Control_pad import channel_map
from Control_pad import channel
from Control_pad import UpDown_map
#from Control_pad import filelist_data
from Control_pad import filelist_pseudo_data
#from Control_pad import filelist_pseudo_data_Ele
#from Control_pa`d import filelist_pseudo_data_Mu
#from Control_pad import filelist_data_FakePho
#from Control_pad import filelist_MC
#from Control_pad import filelist_MC_FakePho
#from Control_pad import filelist_MC_FakeLep
from Control_pad import branch
from Control_pad import lumi
		
def Prepare_hist():

	time_total_init = time.time()

## --Fill data -->>>>>>
#	hist_data = {}
#	for branch_name in branch:
#		plot_branch = branch[branch_name]["name"]
#		if branch[branch_name].__contains__("bin_array"):
#			hist_data_temp = ROOT.TH1F("", "", len(branch[branch_name]["bin_array"])-1, array('d', branch[branch_name]["bin_array"]))
#		else:
#			hist_data_temp = ROOT.TH1F("", "", branch[branch_name]["xbins"], branch[branch_name]["xleft"], branch[branch_name]["xright"])
#		hist_data_temp.SetXTitle(f'{branch[branch_name]["axis_name"]}')
#		hist_data_temp.SetYTitle(f'events / bin')
#		SetHistStyle(hist_data_temp, 1)
#		hist_data[plot_branch] = deepcopy(hist_data_temp)
#	for file in filelist_data:
#		AddHist(file, hist_data, 1, 0, 0, channel, branch)
#
#	for file in filelist_MC:
#		hist_MC = {}
#		for branch_name in branch:
#			plot_branch = branch[branch_name]["name"]
#			if branch[branch_name].__contains__("bin_array"):
#				hist_MC_temp = ROOT.TH1F("", "", len(branch[branch_name]["bin_array"])-1, array('d', branch[branch_name]["bin_array"]))
#			else:
#				hist_MC_temp = ROOT.TH1F("", "", branch[branch_name]["xbins"], branch[branch_name]["xleft"], branch[branch_name]["xright"])
#			SetHistStyle(hist_MC_temp, filelist_MC[file]["color"])
#			hist_MC_temp.SetXTitle(f'{branch[branch_name]["axis_name"]}')
#			for UpDown in range(0,5):
#				hist_MC[plot_branch+f"_{UpDown_map[UpDown]}"] = deepcopy(hist_MC_temp)
#			hist_MC[plot_branch+f"_MuonIDup"] = deepcopy(hist_MC_temp)
#			hist_MC[plot_branch+f"_MuonIDdown"] = deepcopy(hist_MC_temp)
#			hist_MC[plot_branch+f"_ElectronIDup"] = deepcopy(hist_MC_temp)
#			hist_MC[plot_branch+f"_ElectronIDdown"] = deepcopy(hist_MC_temp)
#			hist_MC[plot_branch+f"_ElectronRECOup"] = deepcopy(hist_MC_temp)
#			hist_MC[plot_branch+f"_ElectronRECOdown"] = deepcopy(hist_MC_temp)
#			hist_MC[plot_branch+f"_l1up"] = deepcopy(hist_MC_temp)
#			hist_MC[plot_branch+f"_l1down"] = deepcopy(hist_MC_temp)
#			hist_MC[plot_branch+f"_puup"] = deepcopy(hist_MC_temp)
#			hist_MC[plot_branch+f"_pudown"] = deepcopy(hist_MC_temp)
#			
#		AddHist(filelist_MC[file]["path"], hist_MC, 0, filelist_MC[file]["xsec"], lumi, channel, branch)
#		filelist_MC[file]["hist"] = hist_MC
	
## --Fill Fake Lepton -->>>>>>


	for file in filelist_pseudo_data:

		hist_FakeLep_Estimated = {}
		for branch_name in branch:
			plot_branch = branch[branch_name]["name"]
			if branch[branch_name].__contains__("bin_array"):
				hist_FakeLep_temp = ROOT.TH1F("", "", len(branch[branch_name]["bin_array"])-1, array('d', branch[branch_name]["bin_array"]))
			else:
				hist_FakeLep_temp = ROOT.TH1F("", "", branch[branch_name]["xbins"], branch[branch_name]["xleft"], branch[branch_name]["xright"])
			hist_FakeLep_temp.SetXTitle(f'{branch[branch_name]["axis_name"]}')
			hist_FakeLep_temp.SetYTitle(f'events / bin')
			SetHistStyle(hist_FakeLep_temp,2)
			hist_FakeLep_Estimated[plot_branch] = deepcopy(hist_FakeLep_temp)
		AddHist_FakeLepton(filelist_pseudo_data[file]["path"], hist_FakeLep_Estimated, 0, filelist_pseudo_data[file]["xsec"], lumi, channel, branch,False)
		filelist_pseudo_data[file]['hist_E'] = hist_FakeLep_Estimated

		hist_FakeLep_True = {}
		for branch_name in branch:
			plot_branch = branch[branch_name]["name"]
			if branch[branch_name].__contains__("bin_array"):
				hist_FakeLep_temp2 = ROOT.TH1F("", "", len(branch[branch_name]["bin_array"])-1, array('d', branch[branch_name]["bin_array"]))
			else:
				hist_FakeLep_temp2 = ROOT.TH1F("", "", branch[branch_name]["xbins"], branch[branch_name]["xleft"], branch[branch_name]["xright"])
			hist_FakeLep_temp2.SetXTitle(f'{branch[branch_name]["axis_name"]}')
			hist_FakeLep_temp2.SetYTitle(f'events / bin')
			SetHistStyle(hist_FakeLep_temp2,4)
			hist_FakeLep_True[plot_branch] = deepcopy(hist_FakeLep_temp2)
		AddHist_FakeLepton(filelist_pseudo_data[file]["path"], hist_FakeLep_True, 0, filelist_pseudo_data[file]["xsec"], lumi, channel, branch,True)
		filelist_pseudo_data[file]['hist_T'] = hist_FakeLep_True
	

# - from data
#	for file in filelist_data_FakeLep:
#		AddHist_FakeLepton(file, hist_FakeLep, 1, 0, 0, channel, branch)

# - from MC (pseudo-data)



## --Fill Fake Photon -->>>>>>
#	hist_FakePho= {}
#	for branch_name in branch:
#		plot_branch = branch[branch_name]["name"]
#		if branch[branch_name].__contains__("bin_array"):
#			hist_FakePho_temp = ROOT.TH1F("", "", len(branch[branch_name]["bin_array"])-1, array('d', branch[branch_name]["bin_array"]))
#		else:
#			hist_FakePho_temp = ROOT.TH1F("", "", branch[branch_name]["xbins"], branch[branch_name]["xleft"], branch[branch_name]["xright"])
#		hist_FakePho_temp.SetXTitle(f'{branch[branch_name]["axis_name"]}')
#		hist_FakePho_temp.SetYTitle(f'events / bin')
#		SetHistStyle(hist_FakePho_temp,30)
#		hist_FakePho[plot_branch] = deepcopy(hist_FakePho_temp)
#
#	if channel in [0,1,2,3,4,20,21,22,23,24,30,31,32]:
#		for file in filelist_data_FakePho:
#			AddHist_FakePhoton(file, hist_FakePho, 1, 0, 0, channel, branch)
#		for file in filelist_MC_FakePho:
#			AddHist_FakePhoton(filelist_MC_FakePho[file]["path"], hist_FakePho, 0, filelist_MC_FakePho[file]["xsec"], lumi, channel, branch)
#	else:
#		pass





# -->> Write Data, FakeLepton/Photon
	
	Path("closure").mkdir(parents=True, exist_ok=True)
	file_hist = ROOT.TFile(f'./closure/FakeLepton_closure_2017.root',"RECREATE")
	file_hist.cd()
	for branch_name in branch:

		for file in filelist_pseudo_data:
			plot_branch = branch[branch_name]["name"]

			filelist_pseudo_data[file]['hist_E'][plot_branch].SetName(f'{channel_map[channel]}_{plot_branch}_FakeLepEstimated_{filelist_pseudo_data[file]["name"]}')
			filelist_pseudo_data[file]['hist_E'][plot_branch].Write()
		
			filelist_pseudo_data[file]['hist_T'][plot_branch].SetName(f'{channel_map[channel]}_{plot_branch}_FakeLepTrue_{filelist_pseudo_data[file]["name"]}')
			filelist_pseudo_data[file]['hist_T'][plot_branch].Write()

			

# -->> Write MC

#		for file in filelist_MC:
#			#Nominal + JES JER updown
#			for UpDown in range(0,5):
#				filelist_MC[file]["hist"][plot_branch+f"_{UpDown_map[UpDown]}"].SetName(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{str(UpDown_map[UpDown])}')
#				filelist_MC[file]["hist"][plot_branch+f"_{UpDown_map[UpDown]}"].Write()
#			#updown
#				filelist_MC[file]["hist"][plot_branch+f"_MuonIDup"].SetName(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_MuonIDup')
#				filelist_MC[file]["hist"][plot_branch+f"_MuonIDup"].Write()
#				filelist_MC[file]["hist"][plot_branch+f"_MuonIDdown"].SetName(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_MuonIDdown')
#				filelist_MC[file]["hist"][plot_branch+f"_MuonIDdown"].Write()
#				filelist_MC[file]["hist"][plot_branch+f"_ElectronIDup"].SetName(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_ElectronIDup')
#				filelist_MC[file]["hist"][plot_branch+f"_ElectronIDup"].Write()
#				filelist_MC[file]["hist"][plot_branch+f"_ElectronIDdown"].SetName(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_ElectronIDdown')
#				filelist_MC[file]["hist"][plot_branch+f"_ElectronIDdown"].Write()
#				filelist_MC[file]["hist"][plot_branch+f"_ElectronRECOup"].SetName(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_ElectronRECOup')
#				filelist_MC[file]["hist"][plot_branch+f"_ElectronRECOup"].Write()
#				filelist_MC[file]["hist"][plot_branch+f"_ElectronRECOdown"].SetName(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_ElectronRECOdown')
#				filelist_MC[file]["hist"][plot_branch+f"_ElectronRECOdown"].Write()
#				filelist_MC[file]["hist"][plot_branch+f"_l1up"].SetName(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_l1up')
#				filelist_MC[file]["hist"][plot_branch+f"_l1up"].Write()
#				filelist_MC[file]["hist"][plot_branch+f"_l1down"].SetName(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_l1down')
#				filelist_MC[file]["hist"][plot_branch+f"_l1down"].Write()
#				filelist_MC[file]["hist"][plot_branch+f"_puup"].SetName(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_puup')
#				filelist_MC[file]["hist"][plot_branch+f"_puup"].Write()
#				filelist_MC[file]["hist"][plot_branch+f"_pudown"].SetName(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_pudown')
#				filelist_MC[file]["hist"][plot_branch+f"_pudown"].Write()
	file_hist.Close()

	print (time.time()-time_total_init)

if __name__ == "__main__":
	sys.exit(Prepare_hist())
