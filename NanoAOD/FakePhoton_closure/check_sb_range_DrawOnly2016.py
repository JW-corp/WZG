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

from Lumi_16 import *
from Ratio_Plot import *
from TDR_Style import *
import data_dict_FakeFrac_2016


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

filelist_data = data_dict_FakeFrac_2016.filelist_data
filelist_MC	  = data_dict_FakeFrac_2016.filelist_MC
pt_dicts	  = data_dict_FakeFrac_2016.pt_dicts


if __name__ == "__main__":



	parser = argparse.ArgumentParser()
	parser.add_argument('region', type=str,
				help="EB_PT1 ~ EB_PT5 EE_PT1 ~ EE_PT2")
	parser.add_argument('sb', type=str,
				help="from_4_to_10 .." )
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

	with open('pickle_dict_sample/fake_IsoChg_dict_16.pickle','rb') as fr:
		hist_datafake_pickle   = pickle.load(fr)
		

	# fake template
	hist_datafake  = hist_datafake_pickle[sb][region]
	
	
	
	xbins = hist_datafake.GetNbinsX()
	print("bins :", xbins)
	
	ndata = hist_datafake.GetSumOfWeights()
	
	middle_contents = ndata/2.
	tmp=[]
	for i,bin in enumerate(range(1,xbins+1)):
		tmp.append(hist_datafake.Integral(1,bin))

	minValue   = min(tmp,key=lambda x:abs(x-middle_contents))
	center_bin = tmp.index(minValue)
	center_x   = hist_datafake.GetBinCenter(center_bin)


	print(f"Center X: {center_x} Center bin {center_bin}")
	l1 = ROOT.TGraph(2)
	l1.SetPoint(0,center_x,0)
	l1.SetPoint(1,center_x,1000000)
	l1.SetLineColor(kBlue)

	# -- Before Fit 

	c1 = ROOT.TCanvas("","",1000,800)

	print("bins :", xbins)
	
	hist_datafake.SetStats(False)
	c1.Draw()
	hist_datafake.GetXaxis().SetTitle("Photon IsoChg")
	hist_datafake.GetYaxis().SetTitle("events/bin")
	hist_datafake.Draw("ep")
	
	
	hist_datafake.SetMarkerStyle(0)
	hist_datafake.SetLineColor(2)
	hist_datafake.SetLineWidth(3)
	hist_datafake.Draw("HiST SAME e")
	
	l1.Draw("l same")
	
	legend = ROOT.TLegend(0.65, 0.65, 0.80, 0.85)
	legend.SetBorderSize(0)
	legend.SetFillColor(0)
	legend.SetTextSize(0.020)
	legend.SetLineWidth(1)
	legend.SetLineStyle(0)
	legend.AddEntry(hist_datafake,f'IsoChg middle = {center_x}')
	legend.Draw("SAME")
	
	# ROOT.gPad.SetLogy()
	# ROOT.gPad.SetGrid()
	CMS_lumi(c1, 0, 0)
	c1.Update()

	outname = region + '_Iso16.png'
	outdir='check_IsoChg_for_SBUnv'
	Path(outdir).mkdir(exist_ok=True,parents=True)
	outpath = outdir + '/' + outname
	c1.Print(outpath)

	closure_out_name = outdir + '/' + 'centerX_16.csv'
	f = open(closure_out_name,'a')
	f.write("{0} {1}  \n".format(region,center_x))
	f.close()


