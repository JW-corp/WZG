import ROOT
import numpy as np
import matplotlib.pyplot as plt
import argparse
from ctypes import *
import pathlib
from tqdm import trange

import ROOT
import os,sys
from array import array


from Lumi import *
from Ratio_Plot import *
from TDR_Style import *



def read_data(infile,IsoChg):

	realindict = np.load('RealTemplate/'+infile, allow_pickle=True)[()]
	fakeindict = np.load('FakeTemplate/'+infile, allow_pickle=True)[()]
	dataindict = np.load('DataTemplate/'+infile, allow_pickle=True)[()]
	
	return dataindict, fakeindict[IsoChg], realindict


def Extract_data(bin_, content_):
	exr_arr = np.array([])


	for x, y in zip(bin_, content_):
		if y == 0:
			continue

		sub_arr = np.ones(int(y)) * x
		exr_arr = np.append(exr_arr, sub_arr)
	return exr_arr


def HisttoRoot(Extract_data, bins, data_template, Fake_template, Real_template,Eta_index):

	# Extract data from numpy hist
	data_arr = Extract_data(data_template["bins"], data_template["contents"])
	fake_arr = Extract_data(Fake_template["bins"], Fake_template["contents"])
	real_arr = Extract_data(Real_template["bins"], Real_template["contents"])


	# Set limit
	if (Eta_index == 1):
		print("is Barrel!")
		isbarrel = True
	else:
		print("is Endcap!")
		isbarrel = False

	bins = bins
	if isbarrel:
		#start = 0
		start = 0.006
		end = 0.02
	else:
		#start = 0.018
		start = 0.01
		#end = 0.075
		end = 0.06
	# Make ROOT-hist
	h_data = ROOT.TH1D("Data", "Data template", bins, start, end)
	h_fake = ROOT.TH1D("Fake", "Fake template", bins, start, end)
	h_real = ROOT.TH1D("Real", "Real template", bins, start, end)

	for i in data_arr:
		h_data.Fill(i)

	for i in fake_arr:
		h_fake.Fill(i)

	for i in real_arr:
		h_real.Fill(i)


	return h_data, h_fake, h_real


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



def set_limit(isbarrel):
	isEB_sieie = 0.01015
	isEE_sieie = 0.0326

	if isbarrel:
		return isEB_sieie
	else:
		return isEE_sieie



def draw(hist_data,hist_mctruth,hist_datafake,w_true,w_fake,xleft,xright):
	# Before fit and After fit histogram for validation
	c1 = ROOT.TCanvas("","",1000,800)

	xbins = hist_data.GetNbinsX()
	print("bins :", xbins)

	hist_data.SetStats(False)
	#c1.Draw()
	hist_data.GetXaxis().SetTitle("#sigma_{i#etai#eta}")
	hist_data.GetYaxis().SetTitle("events/bin")

	hist_mctruth_weighted = ROOT.TH1F("","",xbins,xleft,xright)
	hist_datafake_weighted = ROOT.TH1F("","",xbins,xleft,xright)
	hist_sum_weighted = ROOT.TH1F("","",xbins,xleft,xright)

	hist_mctruth.Copy(hist_mctruth_weighted)
	hist_datafake.Copy(hist_datafake_weighted)

	hist_mctruth_weighted.Scale(w_true)
	hist_datafake_weighted.Scale(w_fake)

	hist_sum_weighted.Add(hist_datafake_weighted)
	hist_sum_weighted.Add(hist_mctruth_weighted)


	hist_sum_weighted.SetFillColor(20)
	hist_sum_weighted.Draw("HiST")

	hist_data.Draw("ep same")


	hist_mctruth.SetLineColor(3)
	hist_mctruth.SetLineWidth(3)
	hist_mctruth.Draw("HiST SAME ")

	hist_datafake.SetLineColor(6)
	hist_datafake.SetLineWidth(3)
	hist_datafake.Draw("HiST SAME ")

	hist_mctruth_weighted.SetLineColor(4)
	hist_mctruth_weighted.SetLineWidth(3)
	hist_mctruth_weighted.Draw("HiST SAME")

	hist_datafake_weighted.SetLineColor(2)
	hist_datafake_weighted.SetLineWidth(3)
	hist_datafake_weighted.Draw("HiST SAME")


	legend = ROOT.TLegend(0.65, 0.65, 0.80, 0.85)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetTextSize(0.020)
	legend.SetLineWidth(1)
	legend.SetLineStyle(0)
	legend.AddEntry(hist_sum_weighted,'data fitted','F')
	legend.AddEntry(hist_data,'data template')
	legend.AddEntry(hist_mctruth,'True photons (from MC)')
	legend.AddEntry(hist_datafake,'Fake photons (from MC)')
	legend.AddEntry(hist_mctruth_weighted,'Weighted True photons')
	legend.AddEntry(hist_datafake_weighted,'Weighted Fake photons')



	legend.Draw("SAME")

	# ROOT.gPad.SetLogy()
	# ROOT.gPad.SetGrid()
	CMS_lumi(c1, 0, 0)
	c1.Print(name+ '/image/' + "total_" + IsoChg + '.png')

	return hist_mctruth_weighted , hist_datafake_weighted , hist_sum_weighted





def fit(hist_data, hist_mctruth, hist_datafake, Eta_index,name,IsoChg):


	if (Eta_index == 1):
		isbarrel = True
	else:
		isbarrel = False
	xleft,xright = set_xrange(isbarrel)
	xbins = hist_data.GetNbinsX()

	# Observable
	sieie = ROOT.RooRealVar("sieie","sieie",xleft,xright)

	# Import hist
	data_hist = ROOT.RooDataHist("data_hist", "data with x(sieie)", ROOT.RooArgList(sieie), ROOT.RooFit.Import(hist_data))
	TruePhotons_hist = ROOT.RooDataHist("TruePhotons_hist", "true photons MC with x(sieie)", ROOT.RooArgList(sieie), ROOT.RooFit.Import(hist_mctruth))
	FakePhotons_hist = ROOT.RooDataHist("FakePhotons_hist", "fake photons data with x(sieie)", ROOT.RooArgList(sieie), ROOT.RooFit.Import(hist_datafake))

	ndata = hist_data.GetSumOfWeights()
	ntrue = ROOT.RooRealVar("true number", "true number", 0.5*ndata, 0, ndata)
	nfake = ROOT.RooRealVar("fake number", "fake number", 0.5*ndata, 0, ndata)

	# PDF
	true_pdf = ROOT.RooHistPdf("true_pdf", "truepdf", sieie, TruePhotons_hist)
	fake_pdf = ROOT.RooHistPdf("fake_pdf", "fakepdf", sieie, FakePhotons_hist)

	etrue_pdf = ROOT.RooExtendPdf("ntrue", "ntrue", true_pdf, ntrue)
	efake_pdf = ROOT.RooExtendPdf("nfake", "nfake", fake_pdf, nfake)

	fullpdf = ROOT.RooAddPdf("fullpdf", "true plus fake", ROOT.RooArgList(etrue_pdf, efake_pdf))
	
	# Fit
	result = fullpdf.fitTo(data_hist, ROOT.RooFit.SumW2Error(True), ROOT.RooFit.Extended(True))

	chi2 = ROOT.RooChi2Var("chi2", "chi2", fullpdf, data_hist)
	chi2ToNDF = chi2.getVal() / xbins
	
	# Validation
	weighted_sum_fake = nfake.getVal()
	weighted_sum_true = ntrue.getVal()

	initial_sumw_true = hist_mctruth.GetSumOfWeights()
	initial_sumw_fake = hist_datafake.GetSumOfWeights()

	w_fake =  weighted_sum_fake / initial_sumw_fake
	w_true =  weighted_sum_true / initial_sumw_true

	print("### -----> Checked... perfect!")
	print("Weighted sumw fake: {0:3f} real {1:3f}".format(weighted_sum_fake, weighted_sum_true))
	print("Fake weight : {0:3f} real wegiht {1:3f}".format(w_fake, w_true))
	print("Fitted data sum {0:3f}, Real data sum{1:3f}".format(weighted_sum_fake+weighted_sum_true,ndata))


	hist_mctruth_weighted , hist_datafake_weighted , hist_sum_weighted = draw(hist_data,hist_mctruth,hist_datafake,w_true,w_fake,xleft,xright)
	
	
	# need check.. Error propagation
	#fake_fraction_err = numpy.sqrt(pow(result_nfake/pow(result_ntrue+result_nfake,2),2)
	#							   *pow(result_ntrue_err,2)
	#							   + pow(result_ntrue/pow(result_nfake+result_ntrue,2),2)*pow(result_nfake_err,2))
	
	sieie_val_org = set_limit(isbarrel)
	result_nfake = nfake.getVal()
	result_nfake_err = nfake.getAsymErrorHi()
	result_ntrue = ntrue.getVal()
	result_ntrue_err = ntrue.getAsymErrorHi()
	
	True_in_sieie_cut   = hist_mctruth_weighted.Integral(1,hist_mctruth_weighted.GetXaxis().FindFixBin(sieie_val_org))
	Fake_in_sieie_cut   = hist_datafake_weighted.Integral(1,hist_datafake_weighted.GetXaxis().FindFixBin(sieie_val_org))
	Fitted_in_sieie_cut = hist_sum_weighted.Integral(1,hist_sum_weighted.GetXaxis().FindFixBin(sieie_val_org))

	fake_fraction_err = numpy.sqrt(pow(Fake_in_sieie_cut/pow(result_ntrue+result_nfake,2),2)
								   *pow(result_ntrue_err,2)
								   + pow(result_ntrue/pow(result_nfake+result_ntrue,2),2)*pow(result_nfake_err,2))


	fake_fraction = Fake_in_sieie_cut / Fitted_in_sieie_cut
	print("fake_fraction: {0} +- {1} ".format(fake_fraction,fake_fraction_err))
	
	f = open(name + '/log.csv','a')
	f.write("{0} {1} {2} {3}\n".format(name,IsoChg,fake_fraction,fake_fraction_err))
	f.close()
	
	
	if isbarrel:
		region_mark = "Barrel"
	else:
		region_mark = "Endcap"

	xbins = hist_data.GetNbinsX()
	print("bins :", xbins)

	
	#xframe = sieie.frame(ROOT.RooFit.Title(f"{region_mark} region, {ptrange[0]} GeV < photon PT < {ptrange[1]}"), ROOT.RooFit.Bins(xbins))
	xframe = sieie.frame(ROOT.RooFit.Title(f"{region_mark} region"), ROOT.RooFit.Bins(xbins))
	xframe.GetXaxis().SetTitle("#sigma_{i#etai#eta}")
	xframe.GetYaxis().SetTitle("events / bin")
	data_hist.plotOn(xframe)
	fullpdf.plotOn(xframe, ROOT.RooFit.Name("sum"), ROOT.RooFit.FillColor(20), ROOT.RooFit.DrawOption("F"))
	fullpdf.plotOn(xframe, ROOT.RooFit.Components("ntrue"), ROOT.RooFit.Name("true"), ROOT.RooFit.LineColor(4), ROOT.RooFit.LineStyle(9))
	fullpdf.plotOn(xframe, ROOT.RooFit.Components("nfake"), ROOT.RooFit.Name("fake"), ROOT.RooFit.LineColor(2), ROOT.RooFit.LineStyle(9))
	data_hist.plotOn(xframe)

	
	c1 = ROOT.TCanvas("","",1000,800)
	#c1.Draw()

	xframe.Draw()


	hist_mctruth.SetLineColor(4)
	hist_datafake.SetLineColor(2)




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
	legend.AddEntry(hist_mctruth,'Weighted True photons (from MC)')
	legend.AddEntry(hist_datafake,'Weighted Fake photons (from MC)')
	legend.Draw("SAME")

	textChi2 = ROOT.TLatex()
	textChi2.SetNDC()
	textChi2.SetTextSize(0.02)
	textChi2.DrawLatex(0.6, 0.55, "#chi^{2}/n="+str("%.2f" % chi2ToNDF))
	#textChi2.DrawLatex(0.6, 0.50, str(ptrange[0])+" GeV < #gamma P_{T} < "+str(ptrange[1])+" GeV")

	textChi2.DrawLatex(0.6, 0.45, "Fake Fraction: "+ str("%.3f" % fake_fraction) + "#pm " + str("%.3f" % fake_fraction_err)) 


	CMS_lumi(c1, 0, 0)
	c1.Print(name+ '/image/' + IsoChg + '.png')





if __name__ == "__main__":

	# Multi-thread On
	ROOT.ROOT.EnableImplicitMT()


	# --Read data
	parser = argparse.ArgumentParser()
	parser.add_argument("infile_name", type=str, help="python Fit.py PT_1_eta_1.npy")
	parser.add_argument("bins", type=int, help="python Fit.py PT_1_eta_1.npy 200")
	parser.add_argument("IsoChg", type=str, help="python Fit.py PT_1_eta_1.npy 200 from_3_to_12")
	args = parser.parse_args()

	infile_name = args.infile_name + '.npy'
	name = infile_name.split('.')[0]
	Eta_index = int(infile_name.split(".")[0].split("_")[-1])

	
	IsoChg = args.IsoChg
	pathlib.Path(name + '/image').mkdir(exist_ok=True,parents=True)
	data_template, Fake_template, Real_template = read_data(infile_name,IsoChg)



	# --Numpy hist to ROOT hist
	h_data, h_fake, h_real = HisttoRoot(
		Extract_data, args.bins, data_template, Fake_template, Real_template,Eta_index
	)

	fit(h_data, h_real, h_fake, Eta_index,name,IsoChg)


	

