import matplotlib
from pathlib import Path
import uproot, uproot3
import numpy
import awkward
import numba
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
import pandas as pd
from tqdm import trange
import ROOT
import os,sys
from array import array
import pickle
import argparse
import time

from Lumi_16 import *
from Ratio_Plot import *
from TDR_Style import *
import data_dict_FakeFrac_2016



# --------- Setup data related variables

closure_dict			= data_dict_FakeFrac_2016.closure_dict
filelist_data			= data_dict_FakeFrac_2016.filelist_data
filelist_pseudo_data	= data_dict_FakeFrac_2016.filelist_pseudo_data
filelist_MC				= data_dict_FakeFrac_2016.filelist_MC
pt_dicts				= data_dict_FakeFrac_2016.pt_dicts



# --------- Helper functions 

def check_isbarrel(ptrange):
	if ptrange[-1]  == 0:
		return False
	else:
		return True

   
def set_xrange(isbarrel):
	xleft=0
	xright=0
	xbins=0
	if isbarrel:
		xleft  = 0.00615
		xright = 0.02015
		xbins  = 28
	else:
		xleft  = 0.0172
		xright = 0.0572
		xbins  = 40
	return xleft,xright,xbins

def set_sieie_limit(isbarrel):
	isEB_sieie = 0.01015
	isEE_sieie = 0.0272

	if isbarrel:
		return isEB_sieie
	else:
		return isEE_sieie



# --------- Template maker functions

		
	

# -- Add Fake Template
def AddHist_dataFake(file, hist, ptrange, isbarrel,sb,xsec=1,lumi=1):
	

	
	if 'MuonEG_Run2016H' in file:
		init_branches = [
					'channel_mark'
					,'HLT_Ele27_WPTight_Gsf'
					,'HLT_IsoTkMu24'
					,'HLT_IsoMu24'
					,'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL'
					,'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL'
					,'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ'
					,'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ'
					,'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL'
					,'HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL'
					,'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'
					,'HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_DZ'
					,'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'
					,'photon_sieie'
					,'photon_vidNestedWPBitmap'
					,'photon_eta'
					,'photon_pt'
					,'photon_pfRelIso03_chg']
	
	else:
		init_branches = [
					'channel_mark'
					,'HLT_Ele27_WPTight_Gsf'
					,'HLT_IsoTkMu24'
					,'HLT_IsoMu24'
					,'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL'
					,'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL'
					,'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ'
					,'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ'
					,'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL'
					,'HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL'
					,'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'
					,'photon_sieie'
					,'photon_vidNestedWPBitmap'
					,'photon_eta'
					,'photon_pt'
					,'photon_pfRelIso03_chg']

	branches = uproot.open(file+':Events').arrays(init_branches,library='pd')


	
	 # Single Electron HLT
	HLT_SingleElectron = branches.loc[:,'HLT_Ele27_WPTight_Gsf'] == True

	# DoubleEG HLT
	HLT_DoubleEG = branches.loc[:,'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'] == True

	# Single MuonHLT
	HLT_SingleMuon1 = branches.loc[:,'HLT_IsoTkMu24'] == True
	HLT_SingleMuon2 = branches.loc[:,'HLT_IsoMu24'] == True
	comb_HLT_SingleMuon  = (HLT_SingleMuon1 | HLT_SingleMuon2)

	# Double Muon HLT
	HLT_DoubleMuon1 = branches.loc[:,'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL'] == True		# 2016 B-G 
	HLT_DoubleMuon2 = branches.loc[:,'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL'] == True		# 2016 B-G
	HLT_DoubleMuon3 = branches.loc[:,'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ'] == True		# 2016 H
	HLT_DoubleMuon4 = branches.loc[:,'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ'] == True	# 2016 H
	if 'DoubleMuon_Run2016H'in file: # 2016 H
		comb_HLT_DoubleMuon = (HLT_DoubleMuon3 | HLT_DoubleMuon4)
	elif 'DoubleMuon_Run2016' in file: # 2016 B-G
		comb_HLT_DoubleMuon = (HLT_DoubleMuon1 | HLT_DoubleMuon2)
	else: 
		comb_HLT_DoubleMuon = (HLT_DoubleMuon1 | HLT_DoubleMuon2) | (HLT_DoubleMuon3 | HLT_DoubleMuon4)

	# MuonEG HLT
	HLT_MuonEG1 = branches.loc[:,'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL'] == True
	HLT_MuonEG2 = branches.loc[:,'HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL'] == True


	if 'MuonEG_Run2016H' in file:
		HLT_MuonEG3 = branches.loc[:,'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'] == True
		HLT_MuonEG4 = branches.loc[:,'HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_DZ'] == True
		comb_HLT_MuonEG = (HLT_MuonEG1 | HLT_MuonEG2) | (HLT_MuonEG3 | HLT_MuonEG4)
	else:
		comb_HLT_MuonEG = (HLT_MuonEG1 | HLT_MuonEG2)

	
	# Apply trigger
	if 'SingleMuon' in file:
		arrays = branches.loc[comb_HLT_SingleMuon , :].copy()
	elif 'DoubleMuon' in file:
		arrays = branches.loc[~comb_HLT_SingleMuon & comb_HLT_DoubleMuon, :].copy()
	elif 'SingleElectron' in file:
		arrays = branches.loc[~comb_HLT_SingleMuon & ~comb_HLT_DoubleMuon &   HLT_SingleElectron ,:].copy()
	elif 'MuonEG' in file:
		arrays = branches.loc[~comb_HLT_SingleMuon & ~comb_HLT_DoubleMuon &  ~HLT_SingleElectron & comb_HLT_MuonEG,:].copy()
	elif 'DoubleEG' in file:
		arrays = branches.loc[~comb_HLT_SingleMuon & ~comb_HLT_DoubleMuon &  ~HLT_SingleElectron & ~comb_HLT_MuonEG & HLT_DoubleEG,:].copy()
	else:
		arrays = branches.loc[comb_HLT_SingleMuon | comb_HLT_DoubleMuon | comb_HLT_MuonEG | HLT_SingleElectron |  HLT_DoubleEG ,:].copy()

	# EB BB cut	
	if isbarrel == 1:
		eta_cut = abs(arrays.loc[:,'photon_eta']) < 1.4442
	elif isbarrel == 0:
		eta_cut = abs((arrays.loc[:,'photon_eta']) > 1.566) & abs((arrays.loc[:,'photon_eta']) < 2.5)
		
	# IsoChg SB cut
	chg_cut = ((arrays.loc[:,"photon_pfRelIso03_chg"]*arrays.loc[:,"photon_pt"]) > sb[0]) & ((arrays.loc[:,"photon_pfRelIso03_chg"]*arrays.loc[:,"photon_pt"]) < sb[1])
	
	# pt cut (bins)
	if ptrange[1] == -1:
		pt_cut = (arrays.loc[:,'photon_pt'] >= ptrange[0])		
	else:
		pt_cut = (arrays.loc[:,'photon_pt'] >= ptrange[0]) & (arrays.loc[:,'photon_pt'] < ptrange[1])
			
	arrays = arrays.loc[pt_cut & eta_cut & chg_cut ,:]
	
				
	arrays['photon_IsoChgpt'] = arrays.loc[:,"photon_pfRelIso03_chg"]*arrays.loc[:,"photon_pt"]

	# Fill histogram
	for i in trange(0, len(arrays['photon_pfRelIso03_chg'])):
		hist.Fill(float(arrays['photon_IsoChgpt'].values[i]))



def Make_HistDict():


	## --Fake Template-- ##
	
	# SB loop
	fake_hist_dict={}
	for sb_name,sb in closure_dict.items(): # sb: [IsoChgMin,IsoChgMax]
		print("start closure: {0}".format(sb_name))
		
		# PT loop
		pt_bin_hist_dict={}
		true_fake_frac_dict = {}
		
		for ptname,ptrange in pt_dicts.items(): # [ptMin, ptMax, EBorEE]
			print("start ptbins: {0}".format(ptname))
			
			xleft,xright,xbins = set_xrange(ptrange[-1])
		
			hist_datafake = ROOT.TH1F("","",50,sb[0],sb[1])
			hist_datafake.Sumw2()

			# File loop
			for file in filelist_data:
				AddHist_dataFake(file, hist_datafake, ptrange, ptrange[-1],sb) # need region_mark here
			pt_bin_hist_dict[ptname] = hist_datafake 

		fake_hist_dict[sb_name] = pt_bin_hist_dict
	return fake_hist_dict




if __name__ == "__main__":

	Path('pickle_dict_sample').mkdir(exist_ok=True,parents=True)
	# --- Fake template
	start = time.time()
	print(">>>> Start Fake ")
	hist_datafake_dict = Make_HistDict()
	with open('pickle_dict_sample/fake_IsoChg_dict_16.pickle','wb') as fw:
		pickle.dump(hist_datafake_dict,fw)
	
