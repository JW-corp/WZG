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

import argparse
from pathlib import Path

from Lumi_17 import *
from Ratio_Plot import *
from TDR_Style import *
import data_dict_FakeFrac_2017


# --------- Helper functions 

def check_isbarrel(ptrange):
	if ptrange[-1]  == 0:
		return False
	else:
		return True

	
def set_xrange(isbarrel):
	xleft=0
	xright=0
	
	if isbarrel:
		xleft  = 0.006
		xright = 0.02
	else:
		xleft  = 0.01
		xright = 0.06
	return xleft,xright

def set_sieie_limit(isbarrel):
	isEB_sieie = 0.01015
	isEE_sieie = 0.0272

	if isbarrel:
		return isEB_sieie
	else:
		return isEE_sieie




# --------- Setup data related variables

filelist_data = data_dict_FakeFrac_2017.filelist_data
filelist_MC	  = data_dict_FakeFrac_2017.filelist_MC
pt_dicts	  = data_dict_FakeFrac_2017.pt_dicts


if __name__ == "__main__":



	parser = argparse.ArgumentParser()
	parser.add_argument('region', type=str,
				help="EB_PT1 ~ EB_PT5 EE_PT1 ~ EE_PT2")
	parser.add_argument('sb', type=str,
				help="from_4_to_10 .." )
	parser.add_argument('--isclosure', type=str,
				help="--isclosure True / False")
	args = parser.parse_args()

	
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

	
	sb		 = args.sb
	region   = args.region
	closure = (args.isclosure == "True")

	# -- From fit	


	### >> REAL TEMPLATE ###
	with open('N01_Closure_test_results/pickle_dict_sample/real_hist_dict_17.pickle','rb') as fr:
		hist_mctruth_picke	 = pickle.load(fr)
	
	# real template unc --
	#with open('pickle_dict_sample/real_ZG_hist_dict_17.pickle','rb') as fr:
	#	hist_mctruth_picke	 = pickle.load(fr)
	#with open('pickle_dict_sample/real_WZG_hist_dict_17.pickle','rb') as fr:
	#	hist_mctruth_picke	 = pickle.load(fr)


	### >> FAKE TEMPLATE ###
	with open('N01_Closure_test_results/pickle_dict_sample/fake_hist_dict_17.pickle','rb') as fr:
		hist_datafake_pickle   = pickle.load(fr)
	

	# SB  unc --		
	#with open('pickle_dict_sample/fake_hist_high_dict_17.pickle','rb') as fr:
	#	hist_datafake_pickle   = pickle.load(fr)

	#with open('pickle_dict_sample/fake_hist_low_dict_17.pickle','rb') as fr:
	#	hist_datafake_pickle   = pickle.load(fr)

	### >> DATA TEMPLATE ###
	with open('N01_Closure_test_results/pickle_dict_sample/data_hist_dict_17.pickle','rb') as fr:
		hist_data_pickle 	   = pickle.load(fr)
	

	# -- From real
	if closure:
		with open('N01_Closure_test_results/pickle_dict_sample/hist_true_fake_dict_17.pickle','rb') as fr:
			hist_true_fake_pickle  = pickle.load(fr)

		with open('N01_Closure_test_results/pickle_dict_sample/hist_true_real_dict_17.pickle','rb') as fr:
			hist_true_real_pickle  = pickle.load(fr)


	# data template
	hist_data	  = hist_data_pickle[region]
	# true template
	hist_mctruth  = hist_mctruth_picke[region]
	
	if closure:
		# fake template
		hist_datafake  = hist_datafake_pickle[sb][region]
		hist_true_fake = hist_true_fake_pickle[region]
		hist_true_real = hist_true_real_pickle[region]
	else:
		# fake template
		hist_datafake  = hist_datafake_pickle[sb][region]
	
	
	
	# -- Fitting
	ptrange		 = pt_dicts[region]
	isbarrel	 = check_isbarrel(ptrange)
	xleft,xright = set_xrange(isbarrel)
	
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
	



	## -- Before Fit 

	c1 = ROOT.TCanvas("","",1000,800)

	xbins = hist_data.GetNbinsX()
	print("bins :", xbins)
	
	hist_data.SetStats(False)
	c1.Draw()
	hist_data.GetXaxis().SetTitle("#sigma_{i#etai#eta}")
	hist_data.GetYaxis().SetTitle("events/bin")
	hist_data.Draw("ep")
	
	hist_mctruth.SetMarkerStyle(0)
	hist_mctruth.SetLineColor(4)
	hist_mctruth.SetLineWidth(3)
	hist_mctruth.Draw("HiST SAME e")
	
	hist_datafake.SetMarkerStyle(0)
	hist_datafake.SetLineColor(2)
	hist_datafake.SetLineWidth(3)
	hist_datafake.Draw("HiST SAME e")
	
	
	legend = ROOT.TLegend(0.65, 0.65, 0.80, 0.85)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetTextSize(0.020)
	legend.SetLineWidth(1)
	legend.SetLineStyle(0)
	legend.AddEntry(hist_data,'data template')
	legend.AddEntry(hist_mctruth,'True photons (from MC)')
	legend.AddEntry(hist_datafake,'Fake photons (from data)')
	legend.Draw("SAME")
	
	# ROOT.gPad.SetLogy()
	# ROOT.gPad.SetGrid()
	CMS_lumi(c1, 0, 0)
	c1.Update()

	if closure:
		outname = sb + '_' +  region +'_Before_Fit.png'
	else:
		outname = region + '_Before_Fit.png'

	outdir='fit_out_images_beforeFit'
	Path(outdir).mkdir(exist_ok=True,parents=True)
	outpath = outdir + '/' + outname
	c1.Print(outpath)



	# -- After Fit

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
	xframe.Draw()
	c1.Draw()
	
	legend = ROOT.TLegend(0.60, 0.60, 0.80, 0.85)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetTextSize(0.020)
	legend.SetLineWidth(1)
	legend.SetLineStyle(0)
	legend.AddEntry(hist_data,'data template')
	hist_fit_NaN = hist_data.Clone() # Just for plot
	hist_fit_NaN.SetLineColor(20)
	hist_fit_NaN.SetLineWidth(2)
	hist_fit_NaN.SetFillColor(20)
	hist_fit_NaN.SetMarkerStyle(0)

	if closure:
		hist_true_fake.SetMarkerStyle(0)
		hist_true_fake.SetLineColor(3)
		hist_true_fake.SetLineWidth(3)
		hist_true_fake.Draw("HiST SAME e")

		hist_true_real.SetMarkerStyle(0)
		hist_true_real.SetLineColor(6)
		hist_true_real.SetLineWidth(3)
		hist_true_real.Draw("HiST SAME e")


	#legend.AddEntry(hist_fit_NaN,'Fit result', "F")
	legend.AddEntry(hist_fit_NaN,'Fit result')
	legend.AddEntry(hist_mctruth,'True template (from MC)')
	legend.AddEntry(hist_datafake,'Fake template (from pseudo data)')

	if closure:
		legend.AddEntry(hist_true_real,'True photons (from MC)')
		legend.AddEntry(hist_true_fake,'Fake photons (from pseudo data)')
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

	# Origirnal mediume photon range
	if isbarrel == 1:
		sieie.setRange('window', 0.00515, 0.01015)
	else:
		sieie.setRange('window', 0.0172, 0.0272)

	fakeratio = efake_pdf.createIntegral(sieie, sieie, 'window')
	nfake_window = result_nfake*fakeratio.getVal()
	nfake_window_err = numpy.sqrt(result_nfake_err*result_nfake_err*fakeratio.getVal()*fakeratio.getVal())
	
	trueratio = etrue_pdf.createIntegral(sieie, sieie, 'window')
	ntrue_window = result_ntrue*trueratio.getVal()
	ntrue_window_err = numpy.sqrt(result_ntrue_err*result_ntrue_err*trueratio.getVal()*trueratio.getVal())
	
	fake_fraction = nfake_window / (nfake_window + ntrue_window)
	fake_fraction_err = numpy.sqrt(pow(nfake_window/pow(ntrue_window+nfake_window,2),2)*pow(ntrue_window_err,2) + pow(ntrue_window/pow(nfake_window+ntrue_window,2),2)*pow(nfake_window_err,2))


	sieie_val_org = set_sieie_limit(isbarrel)
	
	if closure:
		N_true_fake = hist_true_fake.Integral(1,hist_true_fake.GetXaxis().FindFixBin(sieie_val_org))
		N_true_real = hist_true_real.Integral(1,hist_true_real.GetXaxis().FindFixBin(sieie_val_org))
		N_data 	  	= hist_data.Integral(1,hist_data.GetXaxis().FindFixBin(sieie_val_org))
		true_fake_fraction = N_true_fake/N_data
		
		Closure_Unc = abs(N_true_fake - nfake_window) / N_true_fake

		print("###"*20)
		print(f"N_true_fake: {N_true_fake}, N_estimated_fake: {nfake_window}")
		print(f"True fake Estimated fake Error: {Closure_Unc}")
		print("###"*20)

		textChi2.DrawLatex(0.55, 0.45,f"N_true_fake: {N_true_fake:.1f} \n N_estimated_fake: {nfake_window:.1f} \n Unc: {Closure_Unc:.3f}")
	#textChi2.DrawLatex(0.55, 0.45,f"Fake fraction: {fake_fraction:.3f} #pm {fake_fraction_err:.3f}")
	
	
	CMS_lumi(c1, 0, 0)
	c1.Update()
	

	if closure:
		outname = sb + '_' +  region +'_AfterFit_17.png'
	else:
		outname = region + '_AfterFit_17.png'


	outdir='fit_out_images_AfterFit_17'
	Path(outdir).mkdir(exist_ok=True,parents=True)
	outpath = outdir + '/' + outname
	c1.Print(outpath)
	fake_fraction_out_name = outdir + '/' + 'fake_fraction.csv'
	f = open(fake_fraction_out_name,'a')
	f.write("{0} {1} {2} \n".format(region,fake_fraction,fake_fraction_err))
	f.close()


	# -- print out ( and closure csv)

	if closure:
		
		sb_lower = sb.split('_')[1]
		sb_upper = sb.split('_')[3]

		#closure_out_name = 'closure_' + region + '.csv'
		closure_out_name = outdir + '/closure.csv'
		f = open(closure_out_name,'a')
		f.write("{0} {1} {2} {3} {4} {5}\n".format(region, sb_lower, sb_upper, Closure_Unc, N_true_fake, nfake_window))
		f.close()
