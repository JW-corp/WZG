import matplotlib
import uproot, uproot3
import numpy
import numba
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import trange
import ROOT
import os,sys
from array import array
import sys


sys.path.append("./tools")
from lumi_17 import *
from tdr import *
from ratio import *
import data_dict_FakeLep

@numba.njit
def sgn(num):
	if (num >= 0):
		return 1
	else:
		return -1

# --------- Setup data related variables
file_list	   	= data_dict_FakeLep.file_list_2018_M
file_WJets	  	= data_dict_FakeLep.file_WJets_2018
file_ZJets	  	= data_dict_FakeLep.file_ZJets_2018
file_ZJets2	 	= data_dict_FakeLep.file_ZJets2_2018
file_list_QCD   = data_dict_FakeLep.file_list_QCD_2018_M




# ----- Distribution

def AddHist_FTdist(file, branch, hist_pre1, hist_pre2, isData, xsec):
	
	if isData:
		print('is Data')
		init_branches = ['is_lepton_tight','jet_pt','mt','met','lepton_pt','lepton_eta','lepton_pdgid','lepton_pfRelIso04_all',
													   'HLT_IsoMu24','HLT_Mu8_TrkIsoVVL','HLT_Mu17_TrkIsoVVL','hlt',
													  'HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30','HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30','HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30']
		if not (branch in init_branches):
			init_branches.append(branch)
		branches = uproot.open(file+':Events').arrays(init_branches, library='pd')

	else:
		print('is MC')
		init_branches = ['is_lepton_tight','jet_pt','mt','met','lepton_pt','lepton_eta','lepton_pdgid','lepton_pfRelIso04_all','lepton_gen_matching','gen_weight',
													   'HLT_IsoMu24','HLT_Mu8_TrkIsoVVL','HLT_Mu17_TrkIsoVVL','hlt',
													  'HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30','HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30','HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30']
		if not (branch in init_branches):
			init_branches.append(branch)
		branches = uproot.open(file+':Events').arrays(init_branches, library='pd')
		true_events = uproot.open(file)['nEventsGenWeighted'].values()[0]

		weight_lowpt = (1000*xsec*lumi_Mu8) / true_events
		weight_highpt = (1000*xsec*lumi_Mu17) / true_events
		lepton_gen_cut1 = branches.loc[:,'lepton_gen_matching'] == 1
		lepton_gen_cut2 = branches.loc[:,'lepton_gen_matching'] == 15
		
	HLT_cut1 = branches.loc[:,'HLT_Mu8_TrkIsoVVL'] == True
	HLT_cut2 = branches.loc[:,'HLT_Mu17_TrkIsoVVL'] == True
	
	met_cut = branches.loc[:,'met'] < 20
	mt_cut = branches.loc[:,'mt'] < 2000000
	lepton_cut = abs(branches.loc[:,'lepton_pdgid']) == 13
	pf_cut = branches.loc[:,'lepton_pfRelIso04_all'] < 0.4
	#pf_cut = branches.loc[:,'is_lepton_tight'] == 1
	pt_edge = branches.loc[:,'lepton_pt'] < 20
	jet_pt = branches.loc[:,'jet_pt'] > 35
	
	if isData:
		arrays_0_20 = branches.loc[HLT_cut1 & lepton_cut & pf_cut & pt_edge & met_cut & mt_cut & jet_pt,:] 
		arrays_20_Inf = branches.loc[HLT_cut2 & lepton_cut & pf_cut & ~pt_edge & met_cut & mt_cut & jet_pt,:] 
		for i in trange(0, len(arrays_0_20[branch]), desc=f'fill pt<20 part for {file}'):
			hist_pre1.Fill(float(arrays_0_20[branch].values[i]))
		for i in trange(0, len(arrays_20_Inf[branch]), desc=f'fill pt>20 part for {file}'):
			hist_pre2.Fill(float(arrays_20_Inf[branch].values[i]))
	
	else:
		if ('TTbar' in file) or ('QCD' in file):
			print ("QCD process\n")
			arrays_0_20 = branches.loc[HLT_cut1 & lepton_cut & pf_cut & pt_edge & met_cut & mt_cut & jet_pt,:] 
			arrays_20_Inf = branches.loc[HLT_cut2 & lepton_cut & pf_cut & ~pt_edge & met_cut & mt_cut & jet_pt,:] 
		else:
			arrays_0_20 = branches.loc[HLT_cut1 & lepton_cut & pf_cut & pt_edge & met_cut & mt_cut & (lepton_gen_cut1 | lepton_gen_cut2) & jet_pt,:] 
			arrays_20_Inf = branches.loc[HLT_cut2 & lepton_cut & pf_cut & ~pt_edge & met_cut & mt_cut & (lepton_gen_cut1 | lepton_gen_cut2) & jet_pt,:] 
		for i in trange(0, len(arrays_0_20[branch]), desc=f'fill pt<20 part for {file}'):
			hist_pre1.Fill(float(arrays_0_20[branch].values[i]), weight_lowpt*sgn(arrays_0_20['gen_weight'].values[i]))
		for i in trange(0, len(arrays_20_Inf[branch]), desc=f'fill pt>20 part for {file}'):
			hist_pre2.Fill(float(arrays_20_Inf[branch].values[i]), weight_highpt*sgn(arrays_20_Inf['gen_weight'].values[i]))
		
	print("DONE")
	return True






####>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  -- 1. Check PT distribution
#print(">>>>>>>>>>>>>>>>>>>> 1. Start Distributing")
#
#xbins = 20
#xlow = 0
#xup = 200
##branch = 'lepton_pt'
#branch = 'mt'
##branch = 'met'
#ptbins = [10, 13, 16, 20, 24, 28, 35, 45, 200]
#
#
## --original
#hist_dist1_DATA = ROOT.TH1D("","",xbins, xlow, xup)
#hist_dist2_DATA = ROOT.TH1D("","",xbins, xlow, xup)
#
## --for pt distribution
##hist_dist1_DATA = ROOT.TH1D("","",8, array('d',ptbins))
##hist_dist2_DATA = ROOT.TH1D("","",8, array('d',ptbins))
#
#hist_dist1_DATA.Sumw2()
#hist_dist2_DATA.Sumw2()
#
#
#for file in file_list:
#	AddHist_FTdist(file, branch, hist_dist1_DATA, hist_dist2_DATA, 1, 1)
#
## --original
#hist_dist1_WJets = ROOT.TH1D("","",xbins, xlow, xup)
#hist_dist2_WJets = ROOT.TH1D("","",xbins, xlow, xup)
#hist_dist1_ZJets = ROOT.TH1D("","",xbins, xlow, xup)
#hist_dist2_ZJets = ROOT.TH1D("","",xbins, xlow, xup)
#
## --for pt 
##hist_dist1_WJets = ROOT.TH1D("","",8, array('d',ptbins))
##hist_dist2_WJets = ROOT.TH1D("","",8, array('d',ptbins))
##hist_dist1_ZJets = ROOT.TH1D("","",8, array('d',ptbins))
##hist_dist2_ZJets = ROOT.TH1D("","",8, array('d',ptbins))
#
#hist_dist1_WJets.Sumw2()
#hist_dist2_WJets.Sumw2()
#hist_dist1_ZJets.Sumw2()
#hist_dist2_ZJets.Sumw2()
#
#
#
#AddHist_FTdist(file_WJets, branch, hist_dist1_WJets, hist_dist2_WJets, 0, 61526.7)
#AddHist_FTdist(file_ZJets, branch, hist_dist1_ZJets, hist_dist2_ZJets, 0, 6077.22)
#AddHist_FTdist(file_ZJets2, branch, hist_dist1_ZJets, hist_dist2_ZJets, 0, 18610)
#
## --original
#hist_dist1_ttbar = ROOT.TH1D("","",xbins, xlow, xup)
#hist_dist2_ttbar = ROOT.TH1D("","",xbins, xlow, xup)
#
## --for pt
##hist_dist1_ttbar = ROOT.TH1D("","",8, array('d',ptbins))
##hist_dist2_ttbar = ROOT.TH1D("","",8, array('d',ptbins))
#
#hist_dist1_ttbar.Sumw2()
#hist_dist2_ttbar.Sumw2()
#
xsec_list_QCD = [
	2799000, # _Pt-15To20
	2526000, # Pt-20To30
	1362000, # Pt-30To50
	376600, # Pt-50To80
	88930, # Pt-80To120
	21230, # Pt-120To170
	7055, # Pt-170To300
	619.3, # Pt-300To470
	59.24, # Pt-470To600
	18.21, # Pt-600To800
	3.275, # Pt-800To1000
	1.078 # Pt-1000toInf
]


#
#
#for i in range(len(file_list_QCD)):
#	AddHist_FTdist(file_list_QCD[i], branch, hist_dist1_ttbar, hist_dist2_ttbar, 0, xsec_list_QCD[i])
#
#
#
#
#c1 = ROOT.TCanvas("","",1000,800)
#
#def SetHistStyle_dist(hist, color, isData):
#	if isData:
#		hist.SetMarkerStyle(20)
#		hist.SetMarkerColor(color)
#	else:
#		hist.SetFillColor(color)
#		hist.SetFillStyle(4100)
#		hist.SetLineColor(color)
#		hist.SetLineStyle(0)
#		hist.SetLineWidth(0)
#	hist.SetYTitle('events/bin')
#
#
#	# X-axis check! ----#
#
#	#hist.SetXTitle('MET [GeV]')
#	hist.SetXTitle('$m_{T,\mu}$ [GeV]')
#	# Adjust y-axis settings
#	# hist.GetYaxis().SetNdivisions(105)
#	hist.GetYaxis().SetTitleSize(25)
#	hist.GetYaxis().SetTitleFont(43)
#	hist.GetYaxis().SetTitleOffset(1.40)
#	hist.GetYaxis().SetLabelFont(43)
#	hist.GetYaxis().SetLabelSize(25)
#
#	# Adjust x-axis settings
#	hist.GetXaxis().SetTitleSize(25)
#	hist.GetXaxis().SetTitleFont(43)
#	hist.GetXaxis().SetTitleOffset(5.0)
#	hist.GetXaxis().SetLabelFont(43)
#	hist.GetXaxis().SetLabelSize(25)
#	hist.SetStats(0)
#
#
#SetHistStyle_dist(hist_dist1_WJets, 22, 0)
#SetHistStyle_dist(hist_dist2_WJets, 22, 0)
#SetHistStyle_dist(hist_dist1_ZJets, 27, 0)
#SetHistStyle_dist(hist_dist2_ZJets, 27, 0)
#SetHistStyle_dist(hist_dist1_ttbar, 32, 0)
#SetHistStyle_dist(hist_dist2_ttbar, 32, 0)
#SetHistStyle_dist(hist_dist1_DATA, 1, 1)
#SetHistStyle_dist(hist_dist2_DATA, 1, 1)
#
#hist_dist_WJets = hist_dist1_WJets.Clone()
#hist_dist_WJets.Add(hist_dist2_WJets)
#SetHistStyle_dist(hist_dist_WJets, 22, 0)
#hist_dist_ZJets = hist_dist1_ZJets.Clone()
#hist_dist_ZJets.Add(hist_dist2_ZJets)
#SetHistStyle_dist(hist_dist_ZJets, 27, 0)
#hist_dist_ttbar = hist_dist1_ttbar.Clone()
#hist_dist_ttbar.Add(hist_dist2_ttbar)
#SetHistStyle_dist(hist_dist_ttbar, 32, 0)
#
## Stack name
#hs_dist = ROOT.THStack("",";M_{T,e} [GeV];events/bin")
#hs_dist.Add(hist_dist_ZJets)
#hs_dist.Add(hist_dist_WJets)
#hs_dist.Add(hist_dist_ttbar)
#
## --original
#MC_err = ROOT.TH1D("","",xbins,xlow,xup)
## --for PT
##MC_err = ROOT.TH1D("","",8,array('d',ptbins))
#MC_err.Sumw2()
#MC_err.Add(hist_dist1_WJets)
#MC_err.Add(hist_dist2_WJets)
#MC_err.Add(hist_dist1_ZJets)
#MC_err.Add(hist_dist2_ZJets)
#MC_err.Add(hist_dist1_ttbar)
#MC_err.Add(hist_dist2_ttbar)
#MC_err.SetFillColor(ROOT.kGray+2)
#MC_err.SetFillStyle(3345)
#MC_err.SetMarkerSize(0.)
#MC_err.SetMarkerColor(ROOT.kGray+2)
#MC_err.SetLineWidth(2)
#MC_err.SetLineColor(0)
#MC_err.SetStats(0)
#
## --originral
#hs_data = ROOT.TH1D("","",xbins,xlow,xup)
## --for PT
##hs_data = ROOT.TH1D("","",8,array('d',ptbins))
#
#hs_data.Add(hist_dist1_DATA)
#hs_data.Add(hist_dist2_DATA)
#SetHistStyle_dist(hs_data, 1, 1)
#
#legend = ROOT.TLegend(0.55, 0.45, 0.70, 0.75)
#legend.SetBorderSize(0)
#legend.SetFillColor(0)
#legend.SetTextSize(0.035)
#legend.SetLineWidth(1)
#legend.SetLineStyle(0)
## legend.AddEntry(hist_dist1_DATA,'Double Muon 2018')
#legend.AddEntry(hist_dist1_DATA,f'DoubleMuon 2016: {format(hs_data.GetSumOfWeights(), ".2f")}')
#legend.AddEntry(hist_dist1_WJets,f'WJetsToLNu: {format(hist_dist_WJets.GetSumOfWeights(), ".2f")}','F')
#legend.AddEntry(hist_dist1_ZJets,f'DYToLNu: {format(hist_dist_ZJets.GetSumOfWeights(), ".2f")}','F')
#legend.AddEntry(hist_dist1_ttbar,f'QCD-EMEnriched: {format(hist_dist_ttbar.GetSumOfWeights(), ".2f")}','F')
#
#c1.Draw()
#pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
#pad1.SetBottomMargin(0.015)  # joins upper and lower plot
## pad1.SetGridx()
#pad1.Draw()
## Lower ratio plot is pad2
#c1.cd()  # returns to main canvas before defining pad2
#pad2 = ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
#pad2.SetTopMargin(0)  # joins upper and lower plot
#pad2.SetBottomMargin(0.3)
#pad2.SetGridy()
#pad2.Draw()
#
## draw everything
#pad1.cd()
## hs_data.GetYaxis().SetMaxDigits(3)
#hs_dist.Draw("HIST")
#hs_dist.SetMaximum(10000000)
#hs_dist.SetMinimum(1)
## hs_dist.GetXaxis().SetRangeUser(10,60)
#hs_dist.GetXaxis().SetLabelSize(0)
#hs_data.Draw("ep SAME")
#MC_err.Draw("e2 SAME")
#legend.Draw("SAME")
#ROOT.gPad.SetLogy()
#ROOT.gPad.RedrawAxis()
#
#
## h1.GetXaxis().SetLabelSize(0)
#pad2.cd()
#h3 = createRatio(hs_data, MC_err)
#h4 = createRatio(MC_err, MC_err)
#h3.Draw("ep")
## h3.GetXaxis().SetRangeUser(10,60)
#h4.Draw("e2 SAME")
#ROOT.gPad.RedrawAxis()
#
##CMS_lumi(pad1, 0, 0)
#c1.SaveAs("Fake_Lepton_MR_dist_mu.png")
##c1.SaveAs('Fake_Lepton/2018/eta_TightElectron_dist_MR_2018_new.pdf')
##c1.SaveAs('Fake_Lepton/2018/eta_TightElectron_dist_MR_2018_new.png')
##c1.SaveAs('Fake_Lepton/2018/MET_FakeElectron_dist_MR_2018_new.pdf')
##c1.SaveAs('Fake_Lepton/2018/MET_FakeElectron_dist_MR_2018_new.png')


###>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  -- 2. Calculate FakeRate
def AddHist_FR_Mu(file, h_nume_m, h_deno_m, isAdd, isData, lumi_Mu8, lumi_Mu17, xsec):
	
	if isData:
		print('is Data')
		branches = uproot.open(file+':Events').arrays(['jet_pt','is_lepton_tight','mt','met','lepton_pt','lepton_eta','lepton_pdgid','lepton_pfRelIso04_all',
													   'HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30','HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30',
													   'HLT_Mu8_TrkIsoVVL','HLT_Mu17_TrkIsoVVL','hlt'], library='pd')
	else:
		print('is MC')
		branches = uproot.open(file+':Events').arrays(['jet_pt','is_lepton_tight','mt','met','lepton_pt','lepton_eta','lepton_pdgid','lepton_pfRelIso04_all',
													   'lepton_gen_matching','HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30','HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30',
													   'HLT_Mu8_TrkIsoVVL','HLT_Mu17_TrkIsoVVL','hlt','gen_weight'], library='pd')
		true_events = uproot.open(file)['nEventsGenWeighted'].values()[0]
		weight_lowpt = (1000*lumi_Mu8*xsec*isAdd) / true_events
		weight_highpt = (1000*lumi_Mu17*xsec*isAdd) / true_events
		lepton_gen_cut1 = branches.loc[:,'lepton_gen_matching'] == 1
		lepton_gen_cut2 = branches.loc[:,'lepton_gen_matching'] == 15
		
	HLT_cut1 = branches.loc[:,'HLT_Mu8_TrkIsoVVL'] == True
	HLT_cut2 = branches.loc[:,'HLT_Mu17_TrkIsoVVL'] == True
	met_cut = branches.loc[:,'met'] < 20
	mt_cut = branches.loc[:,'mt'] < 20
	Muon_cut = abs(branches.loc[:,'lepton_pdgid']) == 13
	pf_cut = branches.loc[:,'lepton_pfRelIso04_all'] < 0.15
	pt_edge = branches.loc[:,'lepton_pt'] < 20
	jet_pt = branches.loc[:,'jet_pt'] > 35

	
	overflow_Y = h_deno_m.GetYaxis().GetBinUpEdge(h_deno_m.GetNbinsY())
	center_upper_Y = h_deno_m.GetYaxis().GetBinCenter(h_deno_m.GetNbinsY())
	

	if isData:
		deno_m_lowpt = branches.loc[HLT_cut1 & pt_edge & Muon_cut & met_cut & mt_cut & jet_pt,:]
		deno_m_highpt = branches.loc[HLT_cut2 & ~pt_edge & Muon_cut & met_cut & mt_cut & jet_pt,:]
		
		
		for i in trange(0, len(deno_m_lowpt['lepton_pt']), desc=f'fill pt < 20 GeV for {file}'):
			if float(deno_m_lowpt['lepton_pt'].values[i]) < overflow_Y:
				h_deno_m.Fill(abs(float(deno_m_lowpt['lepton_eta'].values[i])), float(deno_m_lowpt['lepton_pt'].values[i]))
				if deno_m_lowpt['lepton_pfRelIso04_all'].values[i] < 0.15:
					h_nume_m.Fill(abs(float(deno_m_lowpt['lepton_eta'].values[i])), float(deno_m_lowpt['lepton_pt'].values[i]))
			else:
				h_deno_m.Fill(abs(float(deno_m_lowpt['lepton_eta'].values[i])), center_upper_Y)
				if deno_m_lowpt['lepton_pfRelIso04_all'].values[i] < 0.15:
					h_nume_m.Fill(abs(float(deno_m_lowpt['lepton_eta'].values[i])), center_upper_Y)
				
		for i in trange(0, len(deno_m_highpt['lepton_pt']), desc=f'fill pt > 20 GeV for {file}'):
			if float(deno_m_highpt['lepton_pt'].values[i]) < overflow_Y:
				h_deno_m.Fill(abs(float(deno_m_highpt['lepton_eta'].values[i])), float(deno_m_highpt['lepton_pt'].values[i]))
				if deno_m_highpt['lepton_pfRelIso04_all'].values[i] < 0.15 :
					h_nume_m.Fill(abs(float(deno_m_highpt['lepton_eta'].values[i])), float(deno_m_highpt['lepton_pt'].values[i]))
			else:
				h_deno_m.Fill(abs(float(deno_m_highpt['lepton_eta'].values[i])), center_upper_Y)
				if deno_m_highpt['lepton_pfRelIso04_all'].values[i] < 0.15:
					h_nume_m.Fill(abs(float(deno_m_highpt['lepton_eta'].values[i])), center_upper_Y)
					
				
	else:

		if ('TTbar' in file) or ('QCD' in file):
			print ("QCD process\n")
			deno_m_lowpt = branches.loc[HLT_cut1 & pt_edge & Muon_cut & met_cut & mt_cut & jet_pt,:].copy()
			deno_m_highpt = branches.loc[HLT_cut2 & ~pt_edge & Muon_cut & met_cut & mt_cut & jet_pt,:].copy()
		else:
			deno_m_lowpt = branches.loc[HLT_cut1 & pt_edge & Muon_cut & met_cut & mt_cut & (lepton_gen_cut1 | lepton_gen_cut2) & jet_pt,:].copy()
			deno_m_highpt = branches.loc[HLT_cut2 & ~pt_edge & Muon_cut & met_cut & mt_cut & (lepton_gen_cut1 | lepton_gen_cut2) & jet_pt,:].copy()




		# Fill pt < 20
		if	len(deno_m_lowpt['lepton_pt'])!=0:
			for i in trange(0, len(deno_m_lowpt['lepton_pt']), desc=f'fill pt < 20 GeV for {file}'):
				if float(deno_m_lowpt['lepton_pt'].values[i]) < overflow_Y:
					h_deno_m.Fill(abs(float(deno_m_lowpt['lepton_eta'].values[i])), float(deno_m_lowpt['lepton_pt'].values[i]), weight_lowpt*sgn(deno_m_lowpt['gen_weight'].values[i]))
					if deno_m_lowpt['lepton_pfRelIso04_all'].values[i] < 0.15:				   
						h_nume_m.Fill(abs(float(deno_m_lowpt['lepton_eta'].values[i])), float(deno_m_lowpt['lepton_pt'].values[i]), weight_lowpt*sgn(deno_m_lowpt['gen_weight'].values[i]))
				else:
					h_deno_m.Fill(abs(float(deno_m_lowpt['lepton_eta'].values[i])), center_upper_Y, weight_lowpt*sgn(deno_m_lowpt['gen_weight'].values[i]))
					if deno_m_lowpt['lepton_pfRelIso04_all'].values[i] < 0.15:
						h_nume_m.Fill(abs(float(deno_m_lowpt['lepton_eta'].values[i])), center_upper_Y, weight_lowpt*sgn(deno_m_lowpt['gen_weight'].values[i]))

		# Fill pt > 20
		if	len(deno_m_highpt['lepton_pt'])!=0:
			for i in trange(0, len(deno_m_highpt['lepton_pt']), desc=f'fill pt > 20 GeV for {file}'):
				if float(deno_m_highpt['lepton_pt'].values[i]) < overflow_Y:
					h_deno_m.Fill(abs(float(deno_m_highpt['lepton_eta'].values[i])), float(deno_m_highpt['lepton_pt'].values[i]), weight_highpt*sgn(deno_m_highpt['gen_weight'].values[i]))
					if deno_m_highpt['lepton_pfRelIso04_all'].values[i] < 0.15:
						h_nume_m.Fill(abs(float(deno_m_highpt['lepton_eta'].values[i])), float(deno_m_highpt['lepton_pt'].values[i]), weight_highpt*sgn(deno_m_highpt['gen_weight'].values[i]))
				else:
					h_deno_m.Fill(abs(float(deno_m_highpt['lepton_eta'].values[i])), center_upper_Y, weight_highpt*sgn(deno_m_highpt['gen_weight'].values[i]))
					if deno_m_highpt['lepton_pfRelIso04_all'].values[i] < 0.15:
						h_nume_m.Fill(abs(float(deno_m_highpt['lepton_eta'].values[i])), center_upper_Y, weight_highpt*sgn(deno_m_highpt['gen_weight'].values[i]))
		
	
	deno_counts = 0
	for i in range(h_deno_m.GetNbinsX()):
		for j in range(h_deno_m.GetNbinsY()):
			deno_counts += h_deno_m.GetBinContent(i+1,j+1) 

	nume_counts = 0
	for i in range(h_nume_m.GetNbinsX()):
		for j in range(h_nume_m.GetNbinsY()):
			nume_counts += h_nume_m.GetBinContent(i+1,j+1) 

	print (f"normalized deno :{deno_counts}")
	print (f"normalized nume :{nume_counts}")





ybins = [15, 20, 24, 28, 35, 45, 60]
xbins = [.0, 0.5, 1.0, 1.5, 2.0, 2.5]

from array import array
h_deno_m = ROOT.TH2D("","", len(xbins)-1, array('d',xbins), len(ybins)-1, array('d',ybins))
h_deno_m.StatOverflows(1)
h_deno_m.Sumw2()
h_nume_m = ROOT.TH2D("","", len(xbins)-1, array('d',xbins), len(ybins)-1, array('d',ybins))
h_nume_m.StatOverflows(1)
h_nume_m.Sumw2()



# -- Calculate fake rate from real-data
# -- Temporarly stop
print(">>>>>>>>>>>>>>>>>>>> 2. Start Calculating Fake Rate")
for file_DATA in file_list:
	AddHist_FR_Mu(file_DATA, h_nume_m, h_deno_m, 1, 1, 0, 0, 0)

xsec_WJets = 61526.7  
xsec_ZJets = 6077.22 
xsec_ZJets2 = 18610


AddHist_FR_Mu(file_WJets, h_nume_m, h_deno_m, -1, 0, lumi_Mu8, lumi_Mu17, xsec_WJets)
AddHist_FR_Mu(file_ZJets, h_nume_m, h_deno_m, -1, 0, lumi_Mu8, lumi_Mu17, xsec_ZJets)
AddHist_FR_Mu(file_ZJets2, h_nume_m, h_deno_m, -1, 0, lumi_Mu8, lumi_Mu17, xsec_ZJets2)
print (lumi_Mu8, lumi_Mu17, xsec_WJets)
print (lumi_Mu8, lumi_Mu17, xsec_ZJets)
print (lumi_Mu8, lumi_Mu17, xsec_ZJets2)


fake_rate_mu = h_nume_m.Clone("fake_rate_mu")
fake_rate_mu.Divide(h_deno_m)

fake_rate_mu.SetDirectory(0)
c1 = ROOT.TCanvas("","",1200,800)
fake_rate_mu.SetStats(0)
fake_rate_mu.SetXTitle("|#eta|")
fake_rate_mu.SetYTitle("P_{T} [GeV]")
fake_rate_mu.SetMarkerSize(1.3)
ROOT.gStyle.SetPaintTextFormat('4.2f')
fake_rate_mu.Draw("COLZe TEXT")
c1.Draw()
CMS_lumi(c1,0,0)
c1.SaveAs('Muon_FakeRate_2018.png')

file1 = ROOT.TFile("Mu_Fake_Rate_2D_2018.root","recreate")
file1.cd()
fake_rate_mu.Write()
file1.Close()
c1.Close()




####  ->>>- for closure_test


print(">>>>>>>>>>>>>>>>>>>> 3. Start QCD (Closure test)")

ybins = [15, 20, 24, 28, 35, 45, 60]
xbins = [.0, 0.5, 1.0, 1.5, 2.0, 2.5]



from array import array


# -- Hist using QCD
h_deno_mu_valid = ROOT.TH2D("","", len(xbins)-1, array('d',xbins), len(ybins)-1, array('d',ybins))
h_deno_mu_valid.StatOverflows(1)
h_deno_mu_valid.Sumw2()
h_nume_mu_valid = ROOT.TH2D("","", len(xbins)-1, array('d',xbins), len(ybins)-1, array('d',ybins))
h_nume_mu_valid.StatOverflows(1)
h_nume_mu_valid.Sumw2()



# -- Fill QCD
for i in range(len(file_list_QCD)):
	AddHist_FR_Mu(file_list_QCD[i],h_nume_mu_valid,h_deno_mu_valid,1,0,lumi_Mu8,lumi_Mu17, xsec_list_QCD[i])

h_deno_m_val  = h_deno_m.Clone()
h_nume_m_val  = h_nume_m.Clone()
h_deno_m_diff = h_deno_m.Clone()
h_nume_m_diff = h_nume_m.Clone()

TH1D_data_deno = h_deno_m_val.ProjectionX("TH1D_data_deno",1,8)
TH1D_data = h_nume_m_val.ProjectionX("TH1D_data",1,8)
TH1D_data.Divide(TH1D_data_deno)


TH1D_QCD_deno = h_deno_mu_valid.ProjectionX("TH1D_QCD_deno",1,8)
TH1D_QCD	  = h_nume_mu_valid.ProjectionX("TH1D_QCD",1,8)
TH1D_QCD.Divide(TH1D_QCD_deno)



# >>> To save 2d hist of Fake rate from QCD
fake_rate_mu_valid = h_nume_mu_valid.Clone("fake_rate_mu_valid")
fake_rate_mu_valid.Divide(h_deno_mu_valid)

fake_rate_mu_valid.SetDirectory(0)
c1 = ROOT.TCanvas("c1","",1200,800)
fake_rate_mu_valid.SetStats(0)
fake_rate_mu_valid.SetXTitle("|#eta|")
fake_rate_mu_valid.SetYTitle("P_{T} [GeV]")
fake_rate_mu_valid.SetMarkerSize(1.2)
fake_rate_mu_valid.Draw("TEXT COLZe")
c1.Draw()
CMS_lumi(c1, 0, 0)


c1.SaveAs('Muon_FakeRate_valid_2018.png')
c1.SaveAs('Muon_FakeRate_valid_2018.pdf')
c1.Close()


file1 = ROOT.TFile("Mu_Fake_Rate_2D_closure2018.root","recreate")
file1.cd()
fake_rate_mu_valid.Write()
file1.Close()




## >>>>>>> Validate Data-driven fake-rate and pseudo-data fake-rate

c1 = ROOT.TCanvas("c1","",1000,800)
TH1D_data.SetStats(0)
TH1D_data.SetMarkerStyle(20)
TH1D_data.SetMarkerColor(1)
TH1D_data.SetLineColor(1)
TH1D_data.GetXaxis().SetTitle("|#eta|")
TH1D_data.GetYaxis().SetTitle("Muon Fake Rate")

TH1D_QCD.SetStats(0)
TH1D_QCD.SetMarkerStyle(20)
TH1D_QCD.SetMarkerColor(2)
TH1D_QCD.SetLineColor(2)

h1 = TH1D_data.Clone("h1")
h2 = TH1D_QCD.Clone("h2")
h3 = createRatio(h1, h2)

c1.Draw()
pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
pad1.SetBottomMargin(0.015)  # joins upper and lower plot
# pad1.SetGridx()
pad1.Draw()
# Lower ratio plot is pad2
c1.cd()  # returns to main canvas before defining pad2
pad2 = ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
pad2.SetTopMargin(0)  # joins upper and lower plot
pad2.SetBottomMargin(0.3)
pad2.SetGridy()
pad2.Draw()

h1.SetMaximum(1)
h1.SetMinimum(0)
# CMS_lumi(c1, 0, 0)


# Upper histogram plot is pad1
legend = ROOT.TLegend(0.65, 0.60, 0.90, 0.7)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetTextSize(0.035)
legend.SetLineWidth(1)
legend.SetLineStyle(2)
legend.AddEntry(h1,'data')
legend.AddEntry(h2,'QCD')

# draw everything
pad1.cd()
h1.Draw("ep")
h2.Draw("ep same")
legend.Draw("same")
# to avoid clipping the bottom zero, redraw a small axis
h1.GetXaxis().SetLabelSize(0)
# axis = TGaxis(-5, 20, -5, 220, 20, 220, 510, "")
# axis.SetLabelFont(43)
# axis.SetLabelSize(15)
# axis.Draw()
pad2.cd()
h3.Draw("ep")

CMS_lumi(pad1, 0, 0)

c1.SaveAs('Closure_FR_Muon_datavsQCD_pt_2018.pdf')
c1.SaveAs('Closure_FR_Muon_datavsQCD_pt_2018.png')
