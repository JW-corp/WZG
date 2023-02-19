from typing import Set
import ROOT
import os,sys
from array import array
import time

sys.path.append(os.getcwd())
from Control_pad import channel_map
from Control_pad import channel
from Control_pad import UpDown_map
from Control_pad import filelist_MC
from Control_pad import branch
from Control_pad import UpDown
from AddHist_help_aQGC import SetHistStyle

sys.path.append('..')
import tdr as tdrStyle
from lumi import CMS_lumi
from ratio import createRatio
import argparse
		
def Plot():

	idx=0

	time_total_init = time.time()

	file_hist = ROOT.TFile(f'./test/{channel_map[channel]}.root',"OPEN")
	hist_data = {}

	# --Data
	for branch_name in branch:
		plot_branch = branch[branch_name]["name"]
		hist_data[plot_branch] = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_data_{str(UpDown_map[0])}')

	# --MC

	
	hist_aQGC = {}
	for file in filelist_MC:
		hist_MC = {}
		file_basename = file.split('/')[-1]
		
		
		# -- only for the aQGC reweight
		if file_basename == "aQGC":
		
			#FM0s=['-4e-10','-3e-10','-2e-10','-1e-10','-5e-11','2e-11','2e-11','5e-11','1e-10','2e-10','3e-10','4e-10']
			for branch_name in branch:

				# >> only for MlllA
				if branch_name != "WZG_mllla":
					continue
				# <<

				plot_branch = branch[branch_name]["name"]
				#hist_MC[plot_branch] = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{str(UpDown_map[UpDown])}_Rwt{idx}')
				hist_aQGC['All_zero'] = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{str(UpDown_map[UpDown])}_Rwt0')
				hist_aQGC['m4e-10']   = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{str(UpDown_map[UpDown])}_Rwt1')
				hist_aQGC['m3e-10']   = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{str(UpDown_map[UpDown])}_Rwt2')
				hist_aQGC['m2e-10']   = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{str(UpDown_map[UpDown])}_Rwt3')
				hist_aQGC['m1e-10']   = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{str(UpDown_map[UpDown])}_Rwt4')
				hist_aQGC['m5e-11']   = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{str(UpDown_map[UpDown])}_Rwt5')
				





		
		
		# -- Non-reweight
		else:

			for branch_name in branch:
				# >> only for MlllA
				if branch_name != "WZG_mllla":
					continue
				# <<
				plot_branch = branch[branch_name]["name"]
				hist_MC[plot_branch] = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{str(UpDown_map[UpDown])}')
			
		filelist_MC[file]["hist"] = hist_MC

	# -- FakeLep
	hist_FakeLep = {}
	for branch_name in branch:
		# >> only for MlllA
		if branch_name != "WZG_mllla":
			continue
		# <<
		plot_branch = branch[branch_name]["name"]
		hist_FakeLep[plot_branch] = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_FakeLep_{str(UpDown_map[0])}')

	# -- FakePho
	hist_FakePho= {}
	for branch_name in branch:
		# >> only for MlllA
		if branch_name != "WZG_mllla":
			continue
		# <<
		plot_branch = branch[branch_name]["name"]
		hist_FakePho[plot_branch] = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_FakePho_{str(UpDown_map[0])}')

	tdrStyle.setTDRStyle()
	tdrStyle.gtdr()

	for branch_name in branch:

		# >> only for MlllA
		if branch_name != "WZG_mllla":
			continue
		# <<

		plot_branch = branch[branch_name]["name"]
		c1 = ROOT.TCanvas("","",1000,1000)

		if branch[branch_name].__contains__("bin_array"):
			MC_err	  = ROOT.TH1D("","",len(branch[plot_branch]["bin_array"])-1,array('d', branch[plot_branch]["bin_array"]))
			MC_bkgs	= ROOT.TH1D("","",len(branch[plot_branch]["bin_array"])-1,array('d', branch[plot_branch]["bin_array"]))
		else:
			MC_err = ROOT.TH1D("","",branch[plot_branch]["xbins"],branch[plot_branch]["xleft"],branch[plot_branch]["xright"])
			MC_bkgs = ROOT.TH1D("","",branch[plot_branch]["xbins"],branch[plot_branch]["xleft"],branch[plot_branch]["xright"])

		SetHistStyle(MC_bkgs, filelist_MC["ggZZ_4e"]["color"])
		MC_err.Sumw2()
		MC_err.SetFillColor(ROOT.kGray+2)
		MC_err.SetFillStyle(3345)
		MC_err.SetMarkerSize(0.)
		MC_err.SetMarkerColor(ROOT.kGray+2)
		MC_err.SetLineWidth(2)
		MC_err.SetLineColor(0)
		MC_err.SetStats(0)
		MC_err.SetXTitle(f'{branch[plot_branch]["axis_name"]}')
		MC_err.SetYTitle(f'events / bin')

		stack_mc = ROOT.THStack("","")


		MC_err.Add(hist_FakeLep[plot_branch])
		stack_mc.Add(hist_FakeLep[plot_branch])
		for file in filelist_MC:
			
			if 'WZG' in file:
				continue

			if 'aQGC' in file:
				continue
	

			MC_bkgs.Add(filelist_MC[file]["hist"][plot_branch])			
			SetHistStyle(filelist_MC[file]["hist"][plot_branch], filelist_MC[file]["color"])
			#stack_mc.Add(filelist_MC[file]["hist"][plot_branch])
			MC_err.Add(filelist_MC[file]["hist"][plot_branch])


			
		stack_mc.Add(MC_bkgs)
		MC_err.Add(MC_bkgs)

		MC_err.Add(hist_FakePho[plot_branch])
		stack_mc.Add(hist_FakePho[plot_branch])
		#stack_mc.Add(filelist_MC['WZG']["hist"][plot_branch])
		#MC_err.Add(filelist_MC['WZG']["hist"][plot_branch])

		# >> Add aQGC hist
		#aQGC_hist = filelist_MC['aQGC']["hist"][plot_branch]
		#MC_err.Add(filelist_MC['aQGC']["hist"][plot_branch])
		# <<




		c1.Draw()
		pad1 = ROOT.TPad("pad1", "pad1", 0, 0.30, 1, 1.00)
		pad1.SetTopMargin(0.1)  # joins upper and lower plot
		#pad1.SetBottomMargin(0.035)  # joins upper and lower plot
		pad1.SetBottomMargin(0.065)  # joins upper and lower plot
		# pad1.SetGridx()
		pad1.Draw()
		# Lower ratio plot is pad2
		c1.cd()  # returns to main canvas before defining pad2
		pad2 = ROOT.TPad("pad2", "pad2", 0, 0.00, 1, 0.30)
		#pad2.SetTopMargin(0.040)  # joins upper and lower plot
		pad2.SetTopMargin(0.060)  # joins upper and lower plot
		pad2.SetBottomMargin(0.40)  # joins upper and lower plot
		pad2.SetGridy()
		pad2.Draw()

		# draw everything
		pad1.cd()



		# >> aQGC

		print(hist_aQGC)
		hist_aQGC['All_zero'].SetLineColor(2)
		hist_aQGC['All_zero'].SetFillColor(0)
		hist_aQGC['All_zero'].SetLineWidth(4)

		hist_aQGC['m4e-10'].SetLineColor(3)
		hist_aQGC['m4e-10'].SetFillColor(0)
		hist_aQGC['m4e-10'].SetLineWidth(4)

		hist_aQGC['m3e-10'].SetLineColor(4)
		hist_aQGC['m3e-10'].SetFillColor(0)
		hist_aQGC['m3e-10'].SetLineWidth(4)

		hist_aQGC['m2e-10'].SetLineColor(5)
		hist_aQGC['m2e-10'].SetFillColor(0)
		hist_aQGC['m2e-10'].SetLineWidth(4)

		hist_aQGC['m1e-10'].SetLineColor(6)
		hist_aQGC['m1e-10'].SetFillColor(0)
		hist_aQGC['m1e-10'].SetLineWidth(4)

		legend = ROOT.TLegend(0.20, 0.65, 0.85, 0.85)
		legend.SetNColumns(2)
		legend.SetBorderSize(0)
		legend.SetFillColor(0)
		legend.SetTextSize(0.035)
		legend.SetLineWidth(1)
		legend.SetLineStyle(0)
		#for file in filelist_MC:
		#	if 'WZG' in file:
		#		continue
		#	if 'aQGC' in file:
		#		continue
		#	legend.AddEntry(filelist_MC[file]["hist"][plot_branch], f'{filelist_MC[file]["name"]}: {format(filelist_MC[file]["hist"][plot_branch].GetSumOfWeights(), ".2f")}','F')


		bin=2

		MC_bkg_lastbin = MC_bkgs.GetBinContent(bin)
		FakeLep_lastbin= hist_FakeLep[plot_branch].GetBinContent(bin)
		FakePho_lastbin= hist_FakePho[plot_branch].GetBinContent(bin)
		

		#SM_WZG_lastbin = 0 if SM_WZG_lastbin  < 0 else SM_WZG_lastbin
		MC_bkg_lastbin = 0 if MC_bkg_lastbin  < 0 else MC_bkg_lastbin
		FakeLep_lastbin= 0 if FakeLep_lastbin < 0 else FakeLep_lastbin 
		FakePho_lastbin= 0 if FakePho_lastbin < 0 else FakePho_lastbin


		aQGC_All_zero	=	hist_aQGC['All_zero'].GetBinContent(bin)
		aQGC_m4e10		=	hist_aQGC['m4e-10'].GetBinContent(bin)
		aQGC_m3e10		=	hist_aQGC['m3e-10'].GetBinContent(bin)
		aQGC_m2e10		=	hist_aQGC['m2e-10'].GetBinContent(bin)
		aQGC_m1e10		=	hist_aQGC['m1e-10'].GetBinContent(bin)
		

		
		stat_unc =  hist_FakeLep[plot_branch].GetBinError(bin)
		nominal  =  hist_FakeLep[plot_branch].GetBinContent(bin)
		print(f"stat unc : {stat_unc}, nominal: {nominal}, ratio: {stat_unc/nominal}")







			
		#legend.AddEntry(filelist_MC["WZG"]["hist"][plot_branch], f'{filelist_MC["WZG"]["name"]}: {format(SM_WZG_lastbin, ".4f")}','F')
		legend.AddEntry( hist_aQGC['All_zero'],f'SM WZG : {format(aQGC_All_zero, ".3f")}','L')
		legend.AddEntry( hist_aQGC['m4e-10']  ,f'aQGC FM0 -4e-10 : {format(aQGC_m4e10,".3f")}','L')
		legend.AddEntry( hist_aQGC['m3e-10']  ,f'aQGC FM0 -3e-10: {format(aQGC_m3e10,".3f")}','L')
		legend.AddEntry( hist_aQGC['m2e-10']  ,f'aQGC FM0 -2e-10: {format(aQGC_m2e10,".3f")}','L')
		legend.AddEntry( hist_aQGC['m1e-10']  ,f'aQGC FM0 -1e-10 {format(aQGC_m1e10,".3f")}','L')

		legend.AddEntry(MC_bkgs,f'other MC bkgs: {format(MC_bkg_lastbin, ".4f")}', 'F')
		legend.AddEntry(hist_FakeLep[plot_branch],f'Nonprompt l: {format(FakeLep_lastbin, ".4f")}', 'F')
		if not (channel in [0,1,2,3,4]):
			legend.AddEntry(hist_data[plot_branch], f'data: {format(hist_data[plot_branch].GetBinContent(bin), ".4f")}')
		if channel in [0,1,2,3,4,30,31,32,20,21,22,23,24]:
			legend.AddEntry(hist_FakePho[plot_branch],f'Nonprompt #gamma: {format(FakePho_lastbin, ".4f")}', 'F')
		#Stat_Unc_Total = sum([MC_err.GetBinError(Bin) for Bin in range(1, MC_err.GetNbinsX()+1)])
		Stat_Unc_Total = MC_err.GetBinError(bin) 
		legend.AddEntry(MC_err, f'Stat Unc.: {format(Stat_Unc_Total, ".2f")}', 'F')

		
		print("HERE"*20)
		#print(filelist_MC['WZG']["hist"][plot_branch].GetBinContent(bin))
		print("LastBin aQGC All_zero	: ",hist_aQGC['All_zero'].GetBinContent(bin))
		print("LastBin aQGC m4e-10: ",hist_aQGC['m4e-10'].GetBinContent(bin))
		print("LastBin aQGC m3e-10 : ",hist_aQGC['m3e-10'].GetBinContent(bin))
		print("LastBin aQGC m2e-10 : ",hist_aQGC['m2e-10'].GetBinContent(bin))
		print("LastBin aQGC m1e-10 : ",hist_aQGC['m1e-10'].GetBinContent(bin))
		print("LastBin FakeLepton: ",hist_FakeLep[plot_branch].GetBinContent(bin))
		print("LastBin FakePhoton: ",hist_FakePho[plot_branch].GetBinContent(bin))
		print("LastBin Other MC bkgs: ",MC_bkgs.GetBinContent(bin))

		
		#aQGC_hist.SetLineColor(2)
		#aQGC_hist.SetFillColor(0)
		#aQGC_hist.SetLineWidth(4)
		# <<

		if not (channel in [0,1,2,3,4]):
			hist_data[plot_branch].SetXTitle(f'{branch[plot_branch]["axis_name"]}')
			SetHistStyle(hist_data[plot_branch], 1)
			
			
			hist_data[plot_branch].Draw("E0X0p")
			# hist_data.SetMinimum(10)
			hist_data[plot_branch].SetMaximum(5*hist_data[plot_branch].GetMaximum())
			stack_mc.Draw("HIST SAME")
			MC_err.Draw("e2 SAME")
			hist_data[plot_branch].Draw("E0X0p SAME")
			hist_data[plot_branch].GetXaxis().SetLabelSize(0)
		else:
			#MC_err.Draw("e2")
			#MC_err.GetXaxis().SetLabelSize(0)
			#MC_err.SetMaximum(3.5 * MC_err.GetMaximum())

			# >> aQGC
			#aQGC_hist.SetMaximum(8 * aQGC_hist.GetMaximum())
			#aQGC_hist.Draw("HIST")
			

			#hist_aQGC['All_zero'].Scale(1000)
			#hist_aQGC['m4e-10'].Scale(1000)
			#hist_aQGC['m3e-10'].Scale(1000)
			#hist_aQGC['m2e-10'].Scale(1000)
			#hist_aQGC['m1e-10'].Scale(1000)


			#hist_aQGC['All_zero'].SetMaximum(100*hist_aQGC['m4e-10'].GetMaximum())
			stack_mc.SetMaximum(7*hist_aQGC['m4e-10'].GetMaximum())
			stack_mc.Draw("HIST")
			hist_aQGC['All_zero'].Draw("HIST SAME")
			hist_aQGC['m4e-10'].Draw("HIST SAME")
			hist_aQGC['m3e-10'].Draw("HIST SAME")
			hist_aQGC['m2e-10'].Draw("HIST SAME")
			hist_aQGC['m1e-10'].Draw("HIST SAME")
			# <<

			#MC_err.Draw("e2 SAME")
		legend.Draw("SAME")
		ROOT.gPad.SetLogy()
		ROOT.gPad.RedrawAxis()
		#pad1.SetLogy()
	

		# h1.GetXaxis().SetLabelSize(0)
		pad2.cd()
		h3 = createRatio(hist_data[plot_branch], MC_err)
		SetHistStyle(h3, 1)
		h3.SetYTitle("Data/Pred.")
		h4 = createRatio(MC_err, MC_err)
		SetHistStyle(h4, 1)
		if not (channel in [0,1,2,3,4]):
			h3.Draw("E0X0p")
			h4.Draw("e2 SAME")
		else:
			h4.Draw("e2")
		ROOT.gPad.RedrawAxis()
		ROOT.gStyle.SetPadLeftMargin(0.15)

		CMS_lumi(pad1, 0, 0)
		c1.Update()
		c1.SaveAs(f'./test/{channel_map[channel]}_{plot_branch}_{str(UpDown_map[UpDown])}.pdf')
		c1.SaveAs(f'./test/{channel_map[channel]}_{plot_branch}_{str(UpDown_map[UpDown])}.png')
		del c1,pad1,pad2
		print (time.time()-time_total_init)

if __name__ == "__main__":
	sys.exit(Plot())
