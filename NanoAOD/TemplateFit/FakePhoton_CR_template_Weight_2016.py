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
import data_dict_FakeWeight



# --------- Setup data related variables

xbins		  = data_dict_FakeWeight.xbins
closure_dict  = data_dict_FakeWeight.closure_dict
filelist_data = data_dict_FakeWeight.filelist_data
filelist_MC	  = data_dict_FakeWeight.filelist_MC
pt_dicts	  = data_dict_FakeWeight.pt_dicts


# --------- Template maker functions

def AddHist_data(file, hist,isbarrel,isData=True, xsec=1, lumi=1):
	
	
	# --read branches special case for MuonEG 2016H
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
					,'photon_pfRelIso03_chg'
					,'MET'
					,"dilepton_mass"
					,"nJets"
		]
		
	# --read branches 
	else:
		init_branches =[
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
					,'MET'
					,"dilepton_mass"
					,"nJets"
		]  
	
	# --Complete branches (data) 
	if isData:
		print('is Data')
 
				
	# --Complete branches (MC)
	else:
		print('is MC')
		add_branches = ['Generator_weight','puWeight','PrefireWeight']
		met_branches = uproot.open(file+':Events').keys(filter_name='MET_T1Smear*')
		gen_lepton_branches = uproot.open(file+':Events').keys(filter_name='*_lepton*genPartFlav')
		gen_photon_branches= uproot.open(file+':Events').keys(filter_name='*_photon*genPartFlav')
		true_events = uproot.open(file)['nEventsGenWeighted'].values()[0]
		init_branches.extend(add_branches)
		init_branches.extend(gen_lepton_branches)
		init_branches.extend(gen_photon_branches)
		init_branches.extend(met_branches)

				
	# --Prepare main branches
	branches = uproot.open(file+':Events').arrays(init_branches, library='pd')

				
				
	# --Triggers
	
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
		
	
	# --cuts
	
	# MET 
#	if isData:
#		MET_cut = (arrays.loc[:,'MET'] > 30)
#	else:
#		MET_cut = (arrays.loc[:,f'MET_T1Smear_pt'] > 30)
#	arrays = arrays.loc[MET_cut,:]
#	print('after MET',len(arrays))
	
	
	# Zmass window
	Zmass_mask	 = abs(arrays.loc[:,"dilepton_mass"]-91.188) <= 15
	arrays = arrays.loc[Zmass_mask,:]
	print('after Zmass',len(arrays))
	
	# bjet veto
#	bjet_veto_mask = arrays.loc[:,"nJets"] == 0
#	arrays = arrays.loc[lepton_pt_mask & Zmass_mask & bjet_veto_mask,:]
#	arrays = arrays.loc[bjet_veto_mask,:]
#	print('after bjet_veto',len(arrays))

	
	# Photon Eta
	if isbarrel == 1:
		eta_cut = abs(arrays.loc[:,'photon_eta']) < 1.4442
	elif isbarrel == 0:
		eta_cut = abs((arrays.loc[:,'photon_eta']) > 1.566) & abs((arrays.loc[:,'photon_eta']) < 2.5)
	
	mask_mediumID = (1<<1) | (1<<3) | (1<<5) | (1<<7) | (1<<9) | (1<<11) | (1<<13)

	# Original Photon MediumID 
	arrays['mediumID'] = arrays['photon_vidNestedWPBitmap'] & mask_mediumID
	arrays = arrays.loc[arrays.loc[:,'mediumID'] == mask_mediumID, :]
	print('after Photon ID',len(arrays))
		
	# Photon PT
	pt_cut = (arrays.loc[:,'photon_pt'] >= 20)
	arrays = arrays.loc[pt_cut & eta_cut ,:]
	print('after photon pt eta',len(arrays))
	
	# -- Fill hist
	print("events: ",len(arrays))
	# data
	if isData:
		for i in trange(0, len(arrays['photon_pt']), desc=f'fill photonPT for {file}'):
			hist.Fill(float(arrays['photon_pt'].values[i]))
	# MC
	else:
		arrays['Generator_weight_sgn'] = arrays['Generator_weight'].apply(lambda x: 1 if x >= 0 else -1)
		arrays['true_weight'] = lumi * xsec * 1000 *  arrays['PrefireWeight'] * arrays['puWeight']*  arrays['Generator_weight_sgn'] / true_events   

		for i in trange(len(arrays['photon_pt']), desc=f'fill photonPT for {file}'):
			hist.Fill(float(arrays['photon_pt'].values[i]),float(arrays['true_weight'].values[i]))


def AddHist_dataFake(file, hist,isbarrel,isData=True,xsec=1,lumi=1):
	
	# --read branches special case for MuonEG 2016H
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
					,'photon_pfRelIso03_chg'
					,'MET'
					,"dilepton_mass"
					,"nJets"
		]
		
	# --read branches 
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
					,'photon_pfRelIso03_chg'
					,'MET'
					,"dilepton_mass"
					,"nJets"
		] 
	
	# --Complete branches (data) 
	if isData:
		print('is Data')

				
	# --Complete branches (MC)
	else:
		add_branches = ['Generator_weight','puWeight','PrefireWeight']
		met_branches = uproot.open(file+':Events').keys(filter_name='MET_T1Smear*')
		gen_lepton_branches = uproot.open(file+':Events').keys(filter_name='*_lepton*genPartFlav')
		gen_photon_branches= uproot.open(file+':Events').keys(filter_name='*_photon*genPartFlav')
		true_events = uproot.open(file)['nEventsGenWeighted'].values()[0]
		init_branches.extend(add_branches)
		init_branches.extend(gen_lepton_branches)
		init_branches.extend(gen_photon_branches)
		init_branches.extend(met_branches)

				
	# --Prepare main branches
	branches = uproot.open(file+':Events').arrays(init_branches, library='pd')
	
	# --Triggers
	
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
		
	
	# --cuts
#	# MET 
#	if isData:
#		MET_cut = (arrays.loc[:,'MET'] > 30)
#	else:
#		MET_cut = (arrays.loc[:,f'MET_T1Smear_pt'] > 30)
#	arrays = arrays.loc[MET_cut,:]

	
	# Zmass window
	Zmass_mask	 = abs(arrays.loc[:,"dilepton_mass"]-91.188) <= 15
	arrays = arrays.loc[Zmass_mask,:]
	print('after Zmass',len(arrays))
	
#	# bjet veto
#	bjet_veto_mask = arrays.loc[:,"nJets"] == 0
#	arrays = arrays.loc[lepton_pt_mask & Zmass_mask & bjet_veto_mask,:]
#	arrays = arrays.loc[bjet_veto_mask,:]
#	print('after bjet_veto',len(arrays))

	
	# Photon Eta
	if isbarrel == 1:
		eta_cut = abs(arrays.loc[:,'photon_eta']) < 1.4442
	elif isbarrel == 0:
		eta_cut = abs((arrays.loc[:,'photon_eta']) > 1.566) & abs((arrays.loc[:,'photon_eta']) < 2.5)		
	arrays = arrays.loc[eta_cut,:]
	print("Photon eta cut: ",len(arrays))
	
	pt_cut  = (arrays.loc[:,'photon_pt'] >= 20)
	arrays = arrays.loc[pt_cut,:]
	print("Photon pt cut: ",len(arrays))
	
	# Invert Photon MediumID 
	mask_mediumID = (1<<1) | (1<<3) | (1<<5) | (1<<7) | (1<<9) | (1<<11) | (1<<13)
	mask_invert_IsoChg = (1<<1) | (1<<3) | (1<<5) | (1<<7) | (1<<11) | (1<<13)
	mask_invert_sieie  = (1<<1) | (1<<3) | (1<<5) | (1<<9)  | (1<<11) | (1<<13)
	
	arrays['mediumID'] = arrays['photon_vidNestedWPBitmap'] & mask_mediumID
	
	# case I cut fail sieie or IsoChg in medium cut
	cut_fail_IsoChg = (arrays.loc[:,'mediumID'] == mask_invert_IsoChg)
	cut_fail_Sieie  = (arrays.loc[:,'mediumID'] == mask_invert_sieie)
	cut_fail_medium = cut_fail_IsoChg | cut_fail_Sieie
	
	# case II cut fail one of medium cut
	#cut_fail_medium = (arrays.loc[:,'mediumID'] != mask_mediumID)
	
	
	
	arrays = arrays.loc[cut_fail_medium, :]
	print('after not medium',len(arrays)) 
	
	
	# -- Fill hist
	
	print("events: ",len(arrays))
	# data
	if isData:
		for i in trange(0, len(arrays['photon_pt']), desc=f'fill photonPT for {file}'):
			hist.Fill(float(arrays['photon_pt'].values[i]))
	# MC
	else:

		arrays['Generator_weight_sgn'] = arrays['Generator_weight'].apply(lambda x: 1 if x >= 0 else -1)
		arrays['true_weight'] = lumi * xsec * 1000 *  arrays['PrefireWeight'] * arrays['puWeight'] *  arrays['Generator_weight_sgn'] / true_events   

		for i in trange(len(arrays['photon_pt']), desc=f'fill photonPT for {file}'):
			hist.Fill(float(arrays['photon_pt'].values[i]),float(arrays['true_weight'].values[i]))






if __name__ == "__main__":

	from array import array
	
	# Origin
	xbins_EB = [20,30,50,80,120,180]
	xbins_EE = [20,50,180]
	
	# Tunning
	#xbins_EB = [20,35,400]
	#xbins_EE = [20,400]
	
	
	
	#isbarrel = 1 # barrel
	isbarrel = 0 # endcap
	
	
	nbins=-1
	if isbarrel == 1:
		xbins = xbins_EB
		nbins = len(xbins_EB) - 1
	elif isbarrel ==0:
		xbins = xbins_EE
		nbins = len(xbins_EE) - 1
	else:
		print("wrong!")
	


	# ---- Feed data
	# --Fake template
	hist_datafake = ROOT.TH1F("","",nbins,array('d',xbins))
	hist_datafake.Sumw2()
	# data
	for file in filelist_data:
		AddHist_dataFake(file, hist_datafake,isbarrel,True)
	# MC
	for file in filelist_MC:
		AddHist_dataFake(filelist_MC[file]['path'], hist_datafake,isbarrel,False,filelist_MC[file]['xsec'],35.86)
		
		
	# Data template
	hist_data = ROOT.TH1F("","",nbins,array('d',xbins))
	hist_data.Sumw2()
	# data
	for file in filelist_data:
		AddHist_data(file, hist_data, isbarrel)   
	# MC
	for file in filelist_MC:
		AddHist_data(filelist_MC[file]['path'], hist_data,isbarrel,False,filelist_MC[file]['xsec'],35.86)  
	

	

	# Draw Plots
	c1 = ROOT.TCanvas("","",1000,800)
	c1.Draw()
	
	hist_data.GetXaxis().SetTitle("photon P_{T} [GeV]")
	hist_data.GetYaxis().SetTitle("Events/bin")
	hist_data.SetMarkerStyle(0)
	hist_data.SetLineColor(4)
	hist_data.SetLineWidth(3)
	hist_data.Draw("HIST e")
	
	
	
	hist_datafake.SetMarkerStyle(0)
	hist_datafake.SetLineColor(2)
	hist_datafake.SetLineWidth(3)
	hist_datafake.Draw("HIST SAME e")
	
	legend = ROOT.TLegend(0.65, 0.65, 0.80, 0.85)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetTextSize(0.020)
	legend.SetLineWidth(1)
	legend.SetLineStyle(0)
	legend.AddEntry(hist_data,'data template with full selection')
	legend.AddEntry(hist_datafake,'fake template with full selection')
	legend.Draw("SAME")
	
	
	
	
	#ROOT.gPad.SetLogx()
	ROOT.gPad.SetGrid()
	
	CMS_lumi(c1,0,0)

	if isbarrel == 1:
		name = "EB"
	else:
		name = "EE"

	outname = "FakeWeight_{0}.png".format(name)
	c1.Print(outname)


	outdate_root_file = "DataTemplate_{0}_data.root".format(name)
	file1 = ROOT.TFile(outdate_root_file,"recreate")
	file1.cd()
	hist_data.Write()
	file1.Close()
	
	outfake_root_file = "FakeTemplate_{0}_data.root".format(name)
	file2 = ROOT.TFile(outfake_root_file,"recreate")
	file2.cd()
	hist_datafake.Write()
	file2.Close()

	fake_fraction_2016	= {"Barrel":[0.39038252303100174 ,0.22844984416387987 ,0.13816706152938085 ,0.07864533513131099 ,0.06039361244494585],"Endcap": [0.3755692571005475,0.16799087157261716 ]}

	for i in range(1,hist_data.GetNbinsX()+1):
	
		ydata= hist_data.GetBinContent(i)
		yfake= hist_datafake.GetBinContent(i)
		
		j = i-1
		
		
		if isbarrel == 1:
			print('isbarrel')
			fake_fraction = fake_fraction_2016['Barrel'][j]
		elif isbarrel ==0:
			print('isEndcap')
			fake_fraction = fake_fraction_2016['Endcap'][j]
		
		
		if (ydata == 0) or (yfake == 0):
			ratio = 0
		else:
			ratio = ydata / yfake
		
		fake_weight = ratio * fake_fraction
		print("{0}th  ydata: {1} yfake:  {2} ydata/yfake: {3:.2f} fake fraction: {4} fake weight: {5:.2f}".format(i,ydata,yfake,ratio,fake_fraction,fake_weight))







