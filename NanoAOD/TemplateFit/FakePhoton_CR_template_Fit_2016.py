import matplotlib
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

from Lumi import *
from Ratio_Plot import *
from TDR_Style import *
import data_dict_FakeFrac 



# --------- Setup data related variables

closure_dict  = data_dict_FakeFrac.closure_dict
filelist_data = data_dict_FakeFrac.filelist_data
filelist_MC	  = data_dict_FakeFrac.filelist_MC
pt_dicts	  = data_dict_FakeFrac.pt_dicts





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
		xleft  = 0.00616
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
					,'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'
					,'HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_DZ'
					,'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'
					,'photon_sieie'
					,'photon_vidNestedWPBitmap'
					,'photon_eta'
					,'photon_pt'
					,'photon_pfRelIso03_chg'], library='pd')
	
	else:
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
					,'photon_pfRelIso03_chg'], library='pd')		
		

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
		print('SingleMuon trigger')
		arrays = branches.loc[comb_HLT_SingleMuon , :].copy()
	elif 'DoubleMuon' in file:
		print('DoubleMuon trigger')
		arrays = branches.loc[~comb_HLT_SingleMuon & comb_HLT_DoubleMuon, :].copy()
	elif 'SingleElectron' in file:
		print('SingleElectron trigger')
		arrays = branches.loc[~comb_HLT_SingleMuon & ~comb_HLT_DoubleMuon &   HLT_SingleElectron ,:].copy()
	elif 'MuonEG' in file:
		print('MuonEG Trigger')
		arrays = branches.loc[~comb_HLT_SingleMuon & ~comb_HLT_DoubleMuon &  ~HLT_SingleElectron & comb_HLT_MuonEG,:].copy()
	elif 'DoubleEG' in file:
		print('DoubleEG trigger')
		arrays = branches.loc[~comb_HLT_SingleMuon & ~comb_HLT_DoubleMuon &  ~HLT_SingleElectron & ~comb_HLT_MuonEG & HLT_DoubleEG,:].copy()
		
	else:
		print('isMC')
		arrays = branches.loc[comb_HLT_SingleMuon | comb_HLT_DoubleMuon | comb_HLT_MuonEG | HLT_SingleElectron |  HLT_DoubleEG ,:].copy()
	print('after trigger',len(arrays))
	
	if isbarrel == 1:
		eta_cut = abs(arrays.loc[:,'photon_eta']) < 1.4442
#		 chg_cut = (arrays.loc[:,'photon_pfRelIso03_chg']*arrays.loc[:,'photon_pt']) < 1.141
	elif isbarrel == 0:
		eta_cut = abs((arrays.loc[:,'photon_eta']) > 1.566) & abs((arrays.loc[:,'photon_eta']) < 2.5)
#		 chg_cut = (arrays.loc[:,'photon_pfRelIso03_chg']*arrays.loc[:,'photon_pt']) < 1.051
		
	mask_mediumID_withoutsieie = (1<<1) | (1<<3) | (1<<5) | (1<<9) | (1<<11) | (1<<13)
	arrays['mediumID'] = arrays['photon_vidNestedWPBitmap'] & mask_mediumID_withoutsieie
	arrays = arrays.loc[arrays.loc[:,'mediumID'] == mask_mediumID_withoutsieie, :]
	
		
	if ptrange[1] == -1:
		pt_cut = (arrays.loc[:,'photon_pt'] >= ptrange[0])
	else:
		pt_cut = (arrays.loc[:,'photon_pt'] >= ptrange[0]) & (arrays.loc[:,'photon_pt'] < ptrange[1]) 
		
	arrays = arrays.loc[pt_cut & eta_cut,:]

	for i in trange(0, len(arrays['photon_sieie']), desc=f'fill sigma ieta ieta for {file}'):
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
	
	for i in trange(0, len(arrays['photon_sieie']), desc=f'fill sigma ieta ieta for {file}'):
		hist.Fill(float(arrays['photon_sieie'].values[i]), float(arrays['true_weight'].values[i]))
		


# -- Add Fake Template
def AddHist_dataFake(file, hist, ptrange, isbarrel,sb,closure=False,xsec=1,lumi=1):
	
	
	if 'MuonEG_Run2016H' in file:
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
					,'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'
					,'HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_DZ'
					,'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'
					,'photon_sieie'
					,'photon_vidNestedWPBitmap'
					,'photon_eta'
					,'photon_pt'
					,'photon_pfRelIso03_chg'], library='pd')
	
	else:
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
					,'photon_pfRelIso03_chg'], library='pd')	  
	
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

		
	if isbarrel == 1:
		eta_cut = abs(arrays.loc[:,'photon_eta']) < 1.4442
	elif isbarrel == 0:
		eta_cut = abs((arrays.loc[:,'photon_eta']) > 1.566) & abs((arrays.loc[:,'photon_eta']) < 2.5)
		
	chg_cut = ((arrays.loc[:,"photon_pfRelIso03_chg"]*arrays.loc[:,"photon_pt"]) > sb[0]) & ((arrays.loc[:,"photon_pfRelIso03_chg"]*arrays.loc[:,"photon_pt"]) < sb[1])
	
	if ptrange[1] == -1:
		pt_cut = (arrays.loc[:,'photon_pt'] >= ptrange[0])		
	else:
		pt_cut = (arrays.loc[:,'photon_pt'] >= ptrange[0]) & (arrays.loc[:,'photon_pt'] < ptrange[1])
			
	arrays = arrays.loc[pt_cut & eta_cut & chg_cut ,:]
	for i in trange(0, len(arrays['photon_sieie']), desc=f'fill sigma ieta ieta for {file}'):
		hist.Fill(float(arrays['photon_sieie'].values[i]))






# --------- Feeding functions 

def Make_HistDict(template='Fake',xbins=5,closure=False):
	if template=="Fake":
		
		# SB loop
		fake_hist_dict={}
		for sb_name,sb in closure_dict.items():
			print("start closure: {0}".format(sb_name))
			
			# PT loop
			pt_bin_hist_dict={}
			true_fake_frac_dict = {}
			for ptname,ptrange in pt_dicts.items():
				print("start ptbins: {0}".format(ptname))
				
				xleft,xright,xbins = set_xrange(ptrange[-1])
			
				# file loop
				hist_datafake = ROOT.TH1F("","",xbins,xleft,xright)
				hist_datafake.Sumw2()
			
				if closure:
					
					sum_prompt_photon = 0
					sum_non_prompt_photon  = 0
					for file in filelist_MC:
						AddHist_dataFake(filelist_MC[file]['path'], hist_datafake, ptrange, ptrange[-1],sb,closure,filelist_MC[file]['xsec'], 35.86)
						
						sieie_val_org = set_sieie_limit(ptrange[-1])
						
						if 'G' in file:
							print("Prompt photon sample: {0} weighted evt: {1}".format(file,hist_datafake.Integral(1,hist_datafake.GetXaxis().FindFixBin(sieie_val_org))))
							sum_prompt_photon += hist_datafake.Integral(1,hist_datafake.GetXaxis().FindFixBin(sieie_val_org))
						else:
							print("Non-prompt photon sample: {0} weighted evt: {1}".format(file,hist_datafake.Integral(1,hist_datafake.GetXaxis().FindFixBin(sieie_val_org))))
							sum_non_prompt_photon += hist_datafake.Integral(1,hist_datafake.GetXaxis().FindFixBin(sieie_val_org))
					
					total_photon			 = sum_prompt_photon + sum_non_prompt_photon
					true_fake_fraction	   = sum_non_prompt_photon / total_photon
					pt_bin_hist_dict[ptname] = hist_datafake
					true_fake_frac_dict[ptname] = true_fake_fraction
						
				else:
					for file in filelist_data:
						AddHist_dataFake(file, hist_datafake, ptrange, ptrange[-1],sb,closure)
					pt_bin_hist_dict[ptname] = hist_datafake
					
			if closure:  
				fake_hist_dict[sb_name] = {'histo':pt_bin_hist_dict,'true_fake_fraction':true_fake_frac_dict}
			else:
				fake_hist_dict[sb_name] = pt_bin_hist_dict

		return fake_hist_dict

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
			print("Sucessfully created...total bins: ",hist_mctruth.GetNbinsX())
			print("Sucessfully created...total bins: ",real_hist_dict[ptname].GetNbinsX())

		return real_hist_dict
			
	elif template=="Data":
		
		data_hist_dict={}
		for ptname,ptrange in pt_dicts.items():
			print("start ptbins: {0}".format(ptname))
			
			xleft,xright,xbins = set_xrange(ptrange[-1])
			
			# file loop
			hist_data = ROOT.TH1F("","",xbins,xleft,xright)
			hist_data.Sumw2()
			if closure:
				for file in filelist_MC:
					AddHist_data(filelist_MC[file]['path'], hist_data, ptrange, ptrange[-1],closure,filelist_MC[file]['xsec'], 35.86)
			else:
				for file in filelist_data:
					AddHist_data(file, hist_data, ptrange, ptrange[-1],closure)   
					
			data_hist_dict[ptname] = hist_data
		return data_hist_dict
	else:
		print("Wrong template")





if __name__ == "__main__":

	region = 'EB_PT1'
	ptrange	  = pt_dicts[region]
	isbarrel	 = check_isbarrel(ptrange)
	xleft,xright,xbins  = set_xrange(isbarrel)
	# -- Write files
	
	hist_data_dict	 = Make_HistDict("Data",xbins,False)
	hist_mctruth_dict  = Make_HistDict("Real",xbins)
	hist_datafake_dict = Make_HistDict("Fake",xbins,False)
	
	
	with open('pickle_dict_sample/real_hist_dict.pickle','wb') as fw:
		pickle.dump(hist_mctruth_dict,fw)
		
	with open('pickle_dict_sample/fake_hist_dict.pickle','wb') as fw:
		pickle.dump(hist_datafake_dict,fw)
		
	with open('pickle_dict_sample/data_hist_dict.pickle','wb') as fw:
		pickle.dump(hist_data_dict,fw)
	
	
	# -- Load files 
	pt_dicts={
		"EB_PT1": [20,30,1],
		"EB_PT2": [30,50,1],
		"EB_PT3": [50,80,1],
		"EB_PT4": [80,120,1],
		"EB_PT5": [120,-1,1],
		"EE_PT1": [20,50,0],
		"EE_PT2": [50,-1,0]
	}
	
	closure_dict={
		"from_4_to_10":[4,10]
	}
	
	
	with open('pickle_dict_sample/real_hist_dict.pickle','rb') as fr:
		hist_mctruth_picke = pickle.load(fr)
		
	with open('pickle_dict_sample/fake_hist_dict.pickle','rb') as fr:
		hist_datafake_pickle = pickle.load(fr)
		
	with open('pickle_dict_sample/data_hist_dict.pickle','rb') as fr:
		hist_data_pickle = pickle.load(fr)
	
	
	
	hist_data	 = hist_data_pickle[region]
	hist_mctruth  = hist_mctruth_picke[region]
	hist_datafake = hist_datafake_pickle['from_4_to_10'][region]
	
	
	# -- Fitting

	
	# Observable
	sieie = ROOT.RooRealVar("sieie","sieie",xleft,xright)
	
	
	# Import hist
	data_hist = ROOT.RooDataHist("data_hist", "data with x(sieie)", ROOT.RooArgList(sieie), ROOT.RooFit.Import(hist_data))
	TruePhotons_hist = ROOT.RooDataHist("TruePhotons_hist", "true photons MC with x(sieie)", ROOT.RooArgList(sieie), ROOT.RooFit.Import(hist_mctruth))
	FakePhotons_hist = ROOT.RooDataHist("FakePhotons_hist", "fake photons data with x(sieie)", ROOT.RooArgList(sieie), ROOT.RooFit.Import(hist_datafake))
	
	
	xbins = hist_data.GetNbinsX()
	print("bins :", xbins)
	
	ndata = hist_data.GetSumOfWeights()
	
	# Parameters
	# TrueFraction = ROOT.RooRealVar("TrueFraction","fraction of true photons", 0, 1)
	# FakeFraction = ROOT.RooRealVar("FakeFraction","fraction of fake photons", 0, 1)
	
	ntrue = ROOT.RooRealVar("true number", "true number", 0.5*ndata, 0, ndata)
	nfake = ROOT.RooRealVar("fake number", "fake number", 0.5*ndata, 0, ndata)
	
	# PDF
	true_pdf = ROOT.RooHistPdf("true_pdf", "truepdf", sieie, TruePhotons_hist)
	fake_pdf = ROOT.RooHistPdf("fake_pdf", "fakepdf", sieie, FakePhotons_hist)
	
	etrue_pdf = ROOT.RooExtendPdf("ntrue", "ntrue", true_pdf, ntrue)
	efake_pdf = ROOT.RooExtendPdf("nfake", "nfake", fake_pdf, nfake)
	
	fullpdf = ROOT.RooAddPdf("fullpdf", "true plus fake", ROOT.RooArgList(etrue_pdf, efake_pdf))
	
	# Fit
	fullpdf.fitTo(data_hist, ROOT.RooFit.SumW2Error(True), ROOT.RooFit.Extended(True))
	
	chi2 = ROOT.RooChi2Var("chi2", "chi2", fullpdf, data_hist)
	chi2ToNDF = chi2.getVal() / xbins
	
	if isbarrel == 1:
		region_mark = "Barrel"
	else:
		region_mark = "Endcap"
	
	xbins = hist_data.GetNbinsX()
	print("bins region :", xbins,region_mark)
	
	xframe = sieie.frame(ROOT.RooFit.Title(f"{region_mark} region, {ptrange[0]} GeV < photon PT < {ptrange[1]}"), ROOT.RooFit.Bins(xbins))
	xframe.GetXaxis().SetTitle("#sigma_{i#etai#eta}")
	xframe.GetYaxis().SetTitle("events / bin")
	data_hist.plotOn(xframe)
	fullpdf.plotOn(xframe, ROOT.RooFit.Name("sum"), ROOT.RooFit.FillStyle(4100), ROOT.RooFit.FillColor(20), ROOT.RooFit.DrawOption("F"))
	fullpdf.plotOn(xframe, ROOT.RooFit.Components("ntrue"), ROOT.RooFit.Name("true"), ROOT.RooFit.LineColor(4), ROOT.RooFit.LineStyle(9))
	fullpdf.plotOn(xframe, ROOT.RooFit.Components("nfake"), ROOT.RooFit.Name("fake"), ROOT.RooFit.LineColor(2), ROOT.RooFit.LineStyle(9))
	data_hist.plotOn(xframe)
	
	


		
	# -- Canvas

	c1 = ROOT.TCanvas("","",1000,800)
	c1.Draw()
	xframe.Draw()
	
	legend = ROOT.TLegend(0.60, 0.60, 0.80, 0.85)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetTextSize(0.020)
	legend.SetLineWidth(1)
	legend.SetLineStyle(0)
	legend.AddEntry(hist_data,'data template')
	hist_fit_NaN = hist_data.Clone() # Just for plot
	hist_fit_NaN.SetLineColor(20)
	hist_fit_NaN.SetLineWidth(0)
	hist_fit_NaN.SetFillColor(20)
	hist_fit_NaN.SetMarkerStyle(0)
	legend.AddEntry(hist_fit_NaN,'Fit result', "F")
	legend.AddEntry(hist_mctruth,'True photons (from MC)')
	legend.AddEntry(hist_datafake,'Fake photons (from data)')
	legend.Draw("SAME")
	
	textChi2 = ROOT.TLatex()
	textChi2.SetNDC()
	textChi2.SetTextSize(0.02)
	textChi2.DrawLatex(0.6, 0.55, "#chi^{2}/n="+str("%.2f" % chi2ToNDF))
	textChi2.DrawLatex(0.6, 0.50, str(ptrange[0])+" GeV < #gamma P_{T} < "+str(ptrange[1])+" GeV")
	result_nfake = nfake.getVal()
	result_nfake_err = nfake.getAsymErrorHi()
	result_ntrue = ntrue.getVal()
	result_ntrue_err = ntrue.getAsymErrorHi()
	fake_fraction = result_nfake/(result_ntrue+result_nfake)
	fake_fraction_err = numpy.sqrt(pow(result_nfake/pow(result_ntrue+result_nfake,2),2)*pow(result_ntrue_err,2) + pow(result_ntrue/pow(result_nfake+result_ntrue,2),2)*pow(result_nfake_err,2))
	textChi2.DrawLatex(0.6, 0.45, "Fake Fraction: "+ str("%.3f" % fake_fraction) + "#pm " + str("%.3f" % fake_fraction_err)) 
	
	
	CMS_lumi(c1, 0, 0)
	
	# print (ntrue.getVal())
	# print (ntrue.getAsymErrorHi())
	# print (ntrue.getAsymErrorLo())
	
	
	
	
	
	
	
