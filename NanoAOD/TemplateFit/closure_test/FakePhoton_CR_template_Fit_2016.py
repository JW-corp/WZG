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

from Lumi import *
from Ratio_Plot import *
from TDR_Style import *
import data_dict_FakeFrac 



# --------- Setup data related variables

closure_dict			= data_dict_FakeFrac.closure_dict
filelist_data			= data_dict_FakeFrac.filelist_data
filelist_pseudo_data	= data_dict_FakeFrac.filelist_pseudo_data
filelist_MC				= data_dict_FakeFrac.filelist_MC
pt_dicts				= data_dict_FakeFrac.pt_dicts



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
	isEE_sieie = 0.0326

	if isbarrel:
		return 0.01015
	else:
		return 0.0326



# --------- Template maker functions

# -- Add data template
def AddHist_data(file, hist, ptrange, isbarrel,closure=False,xsec=1,lumi=1):


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

	# Add branches for pseudo-data
	if closure:
		true_events = uproot.open(file)['nEventsGenWeighted'].values()[0]
		for_pseudo_data_add_branch = ['photon_genPartFlav','puWeight','Generator_weight']
		init_branches.extend(for_pseudo_data_add_branch)
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
	HLT_DoubleMuon1 = branches.loc[:,'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL'] == True
	HLT_DoubleMuon2 = branches.loc[:,'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL'] == True
	HLT_DoubleMuon3 = branches.loc[:,'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ'] == True
	HLT_DoubleMuon4 = branches.loc[:,'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ'] == True
	if 'DoubleMuon_Run2016H'in file:
		comb_HLT_DoubleMuon = (HLT_DoubleMuon3 | HLT_DoubleMuon4)
	elif 'DoubleMuon_Run2016' in file:
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

	print('before trigger',len(branches))
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

	# Medium ID cut without sieie
	mask_mediumID_withoutsieie = (1<<1) | (1<<3) | (1<<5) | (1<<9) | (1<<11) | (1<<13)
	arrays['mediumID'] = arrays['photon_vidNestedWPBitmap'] & mask_mediumID_withoutsieie
	arrays = arrays.loc[arrays.loc[:,'mediumID'] == mask_mediumID_withoutsieie, :]
	
	# PT cut (bins)
	if ptrange[1] == -1:
		pt_cut = (arrays.loc[:,'photon_pt'] >= ptrange[0])
	else:
		pt_cut = (arrays.loc[:,'photon_pt'] >= ptrange[0]) & (arrays.loc[:,'photon_pt'] < ptrange[1]) 
		
	arrays = arrays.loc[pt_cut & eta_cut,:]

	
	# Fill histogram
	if closure: # Pseudo-data MC. Including all SFs and Noram
		arrays['Generator_weight_sgn'] = arrays['Generator_weight'].apply(lambda x: 1 if x >= 0 else -1)
		arrays['true_weight'] = lumi * xsec * 1000 * arrays['puWeight'] * arrays['Generator_weight_sgn'] / true_events
		#for i in trange(0, len(arrays['photon_sieie']), desc=f'fill sigma ieta ieta for {file}'):
		for i in trange(0, len(arrays['photon_sieie'])):
			hist.Fill(float(arrays['photon_sieie'].values[i]), float(arrays['true_weight'].values[i]))

	else: # data
		#for i in trange(0, len(arrays['photon_sieie']), desc=f'fill sigma ieta ieta for {file}'):
		for i in trange(0, len(arrays['photon_sieie'])):
			hist.Fill(float(arrays['photon_sieie'].values[i]))
	


# --Add True(Real) Template
def AddHist_mcTruth(file, hist, ptrange, isbarrel, xsec, lumi):
	branches = uproot.open(file+':Events').arrays([
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
					,'photon_pfRelIso03_chg'
					,'photon_genPartFlav'
					,'Generator_weight'
					,'puWeight'], library='pd')   
	true_events = uproot.open(file)['nEventsGenWeighted'].values()[0]
	
	 # Single Electron HLT
	HLT_SingleElectron = branches.loc[:,'HLT_Ele27_WPTight_Gsf'] == True

	# DoubleEG HLT
	HLT_DoubleEG = branches.loc[:,'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'] == True

	# Single MuonHLT
	HLT_SingleMuon1 = branches.loc[:,'HLT_IsoTkMu24'] == True
	HLT_SingleMuon2 = branches.loc[:,'HLT_IsoMu24'] == True
	comb_HLT_SingleMuon  = (HLT_SingleMuon1 | HLT_SingleMuon2)

	# Double Muon HLT
	HLT_DoubleMuon1 = branches.loc[:,'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL'] == True
	HLT_DoubleMuon2 = branches.loc[:,'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL'] == True
	HLT_DoubleMuon3 = branches.loc[:,'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ'] == True
	HLT_DoubleMuon4 = branches.loc[:,'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ'] == True
	if 'DoubleMuon_Run2016H'in file:
		comb_HLT_DoubleMuon = (HLT_DoubleMuon3 | HLT_DoubleMuon4)
	elif 'DoubleMuon_Run2016' in file:
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
		

	arrays = branches.loc[comb_HLT_SingleMuon | comb_HLT_DoubleMuon | comb_HLT_MuonEG | HLT_SingleElectron |  HLT_DoubleEG ,:].copy()
	
	if isbarrel == 1:
		eta_cut = abs(arrays.loc[:,'photon_eta']) < 1.4442
	elif isbarrel == 0:
		eta_cut = abs((arrays.loc[:,'photon_eta']) > 1.566) & abs((arrays.loc[:,'photon_eta']) < 2.5)
		
	mask_mediumID_withoutsieie = (1<<1) | (1<<3) | (1<<5) | (1<<9) | (1<<11) | (1<<13)
	arrays['mediumID'] = arrays['photon_vidNestedWPBitmap'] & mask_mediumID_withoutsieie
	arrays = arrays.loc[arrays.loc[:,'mediumID'] == mask_mediumID_withoutsieie, :]
	
	
	if ptrange[1] == -1:
		pt_cut = (arrays.loc[:,'photon_pt'] >= ptrange[0])
	else:
		pt_cut = (arrays.loc[:,'photon_pt'] >= ptrange[0]) & (arrays.loc[:,'photon_pt'] < ptrange[1]) 
	gen_cut = arrays.loc[:,'photon_genPartFlav'] != 0
	arrays = arrays.loc[pt_cut & eta_cut  & gen_cut,:]
	
	arrays['Generator_weight_sgn'] = arrays['Generator_weight'].apply(lambda x: 1 if x >= 0 else -1)
	arrays['true_weight'] = lumi * xsec * 1000 * arrays['puWeight'] * arrays['Generator_weight_sgn'] / true_events
	
	# Fill histogram
	#for i in trange(0, len(arrays['photon_sieie']), desc=f'fill sigma ieta ieta for {file}'):
	for i in trange(0, len(arrays['photon_sieie'])):
		hist.Fill(float(arrays['photon_sieie'].values[i]), float(arrays['true_weight'].values[i]))
		


# -- Add Fake Template
def AddHist_dataFake(file, hist, ptrange, isbarrel,sb,closure=False,xsec=1,lumi=1):
	

	
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

	# Add branches for pseudo-data
	if closure:
		true_events = uproot.open(file)['nEventsGenWeighted'].values()[0]
		for_pseudo_data_add_branch = ['photon_genPartFlav','puWeight','Generator_weight']
		init_branches.extend(for_pseudo_data_add_branch)
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
	
	# Only for closure test (pseudo data)
	if closure:
		
		# -- real photon samples
		if 'G' in file.split("/")[-1]: 
			print(f"Real Photon!!!!--Before applying genFlav cut : {len(arrays)}")
			gen_cut = arrays.loc[:,'photon_genPartFlav'] != 0
			arrays = arrays.loc[gen_cut,:]
			print(f"Real Photon!!!!--After applying genFlav cut : {len(arrays)}")
		# -- fake photon samples
		else:
			print(f"Fake Photon!!!!--Before applying genFlav cut : {len(arrays)}")
			gen_cut = arrays.loc[:,'photon_genPartFlav'] == 0
			arrays = arrays.loc[gen_cut,:]
			print(f"Fake Photon!!!!--After applying genFlav cut : {len(arrays)}")
				
		
	# Fill histogram
	if closure: # Pseudo-data MC. Including all SFs and Noram
		arrays['Generator_weight_sgn'] = arrays['Generator_weight'].apply(lambda x: 1 if x >= 0 else -1)
		arrays['true_weight'] = lumi * xsec * 1000 * arrays['puWeight'] * arrays['Generator_weight_sgn'] / true_events
		#for i in trange(0, len(arrays['photon_sieie']), desc=f'fill sigma ieta ieta for {file}'):
		for i in trange(0, len(arrays['photon_sieie'])):
			hist.Fill(float(arrays['photon_sieie'].values[i]), float(arrays['true_weight'].values[i]))

	else: # data
		#for i in trange(0, len(arrays['photon_sieie']), desc=f'fill sigma ieta ieta for {file}'):
		for i in trange(0, len(arrays['photon_sieie'])):
			hist.Fill(float(arrays['photon_sieie'].values[i]))


# --------- Feeding functions 
def Make_HistDict(template='Fake',closure=False):


	## --Fake Template-- ##
	if template=="Fake":
		
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
			
				hist_datafake = ROOT.TH1F("","",xbins,xleft,xright)
				hist_datafake.Sumw2()
			
				# >>> Closure test (pseudo data)
				if closure:
					
					sum_prompt_photon = 0
					sum_non_prompt_photon  = 0

					# File loop
					for file in filelist_pseudo_data:
						print(f" ##>>>>>>>>>>>>>>>>>>>>>>>>> Procesing File: {file}")
						AddHist_dataFake(filelist_pseudo_data[file]['path'], hist_datafake, ptrange, ptrange[-1],sb,closure,filelist_pseudo_data[file]['xsec'], 35.86)
						
						sieie_val_org = set_sieie_limit(ptrange[-1])
						
						if 'G' in file:
							#print("Prompt photon sample: {0} weighted evt: {1}".format(file,hist_datafake.Integral(1,hist_datafake.GetXaxis().FindFixBin(sieie_val_org))))
							sum_prompt_photon += hist_datafake.Integral(1,hist_datafake.GetXaxis().FindFixBin(sieie_val_org))
						else:
							#print("Non-prompt photon sample: {0} weighted evt: {1}".format(file,hist_datafake.Integral(1,hist_datafake.GetXaxis().FindFixBin(sieie_val_org))))
							sum_non_prompt_photon += hist_datafake.Integral(1,hist_datafake.GetXaxis().FindFixBin(sieie_val_org))
					
					total_photon			 = sum_prompt_photon + sum_non_prompt_photon
					true_fake_fraction	   = sum_non_prompt_photon / total_photon
					pt_bin_hist_dict[ptname] = hist_datafake
					true_fake_frac_dict[ptname] = true_fake_fraction
						
				else: # <<< Closure test

					# >>> Non-closure
					# File loop
					for file in filelist_data:
						AddHist_dataFake(file, hist_datafake, ptrange, ptrange[-1],sb,closure) # need region_mark here
					pt_bin_hist_dict[ptname] = hist_datafake 
					# <<< closure		

			# Write as a dictionary			
			if closure:  
				fake_hist_dict[sb_name] = {'histo':pt_bin_hist_dict,'true_fake_fraction':true_fake_frac_dict}
			else:
				fake_hist_dict[sb_name] = pt_bin_hist_dict
		return fake_hist_dict




	## --Real Template-- ##
	elif template=="Real":
		
		real_hist_dict={}
		for ptname,ptrange in pt_dicts.items():
			print("start ptbins: {0}".format(ptname))
			
			xleft,xright,xbins = set_xrange(ptrange[-1])
			
			# file loop
			hist_mctruth = ROOT.TH1F("","",xbins,xleft,xright)
			hist_mctruth.Sumw2()
			for file in filelist_MC:
				if (file != "WZG") and (file != "ZGToLLG"):
					continue
				AddHist_mcTruth(filelist_MC[file]['path'], hist_mctruth, ptrange, ptrange[-1], filelist_MC[file]['xsec'], 35.86)
			real_hist_dict[ptname] = hist_mctruth
			#print("Sucessfully created...total bins: ",hist_mctruth.GetNbinsX())
			#print("Sucessfully created...total bins: ",real_hist_dict[ptname].GetNbinsX())

		return real_hist_dict
			
	## --Data Template-- ##
	elif template=="Data":
		
		data_hist_dict={}
		for ptname,ptrange in pt_dicts.items():
			print("start ptbins: {0}".format(ptname))
			
			xleft,xright,xbins = set_xrange(ptrange[-1])
			
			# file loop
			hist_data = ROOT.TH1F("","",xbins,xleft,xright)
			hist_data.Sumw2()

			# >>> closure test
			if closure:
				for file in filelist_pseudo_data:
					AddHist_data(filelist_pseudo_data[file]['path'], hist_data, ptrange, ptrange[-1],closure,filelist_pseudo_data[file]['xsec'], 35.86)

			# >>> non closure test
			else:
				for file in filelist_data:
					AddHist_data(file, hist_data, ptrange, ptrange[-1],closure)
					
			data_hist_dict[ptname] = hist_data
		return data_hist_dict
	else:
		print("Wrong template")





if __name__ == "__main__":




	parser = argparse.ArgumentParser()
	parser.add_argument('template', type=str,
				help="fake or data or real")
	args = parser.parse_args()



	# -- Write files
	# Template, Bins, Closure test
	Path('pickle_dict_sample').mkdir(exist_ok=True,parents=True)

	# --- Fake template
	start = time.time()
	if args.template == 'fake':
		print(">>>> Start Fake ")
		hist_datafake_dict = Make_HistDict("Fake",True)
		with open('pickle_dict_sample/fake_hist_dict.pickle','wb') as fw:
			pickle.dump(hist_datafake_dict,fw)


	# --- Data template
	if args.template == 'data':
		print(">>>> Start Data ")
		hist_data_dict	 = Make_HistDict("Data",True) 
		with open('pickle_dict_sample/data_hist_dict.pickle','wb') as fw:
			pickle.dump(hist_data_dict,fw)


	# --- Real template
	if args.template == 'real':
		print(">>>> Start Real")
		hist_mctruth_dict  = Make_HistDict("Real",False)
		with open('pickle_dict_sample/real_hist_dict.pickle','wb') as fw:
			pickle.dump(hist_mctruth_dict,fw)
		
	print("time :", time.time() - start)
