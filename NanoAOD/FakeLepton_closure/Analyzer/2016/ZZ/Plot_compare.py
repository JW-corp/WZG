from typing import Set
import ROOT
import os,sys
from array import array
import time

sys.path.append(os.getcwd())
from Control_pad import channel_map
from Control_pad import channel
from Control_pad import UpDown_map
#from Control_pad import filelist_MC
from Control_pad import filelist_pseudo_data


#filelist_pseudo_data_Ele = {
from Control_pad import branch
from Control_pad import UpDown
sys.path.append('..')
import tdr as tdrStyle
from lumi import CMS_lumi
#from AddHist_help import SetHistStyle
from ratio import createRatio
import numpy as np


def SetHistStyle(hist, color):

	hist.SetLineWidth(4)
	hist.SetLineColor(color)
	hist.SetMarkerStyle(20)
	hist.SetMarkerColor(color)
	hist.SetYTitle('events/bin')
	hist.SetStats(0)
	# hist.Sumw2()
		

	# Adjust y-axis settings
	# hist.GetYaxis().SetNdivisions(105)
	hist.GetYaxis().SetTitleSize(45)
	hist.GetYaxis().SetTitleFont(43)
	hist.GetYaxis().SetTitleOffset(1.65)
	hist.GetYaxis().SetLabelFont(43)
	hist.GetYaxis().SetLabelSize(38)
	hist.GetYaxis().SetLabelOffset(0.015)

	# Adjust x-axis settings
	hist.GetXaxis().SetTitleSize(45)
	hist.GetXaxis().SetTitleFont(40)
	hist.GetXaxis().SetTitleOffset(3.3)
	hist.GetXaxis().SetLabelFont(43)
	hist.GetXaxis().SetLabelSize(38)
	hist.GetXaxis().SetLabelOffset(0.015)


def Plot():

	time_total_init = time.time()
	file_hist = ROOT.TFile(f'closure/FakeLepton_closure_2016.root',"OPEN")



	# Get Histogram
	for file in filelist_pseudo_data:
		hist_True ={}
		hist_Estimated ={}
		for branch_name in branch:
			plot_branch 				= branch[branch_name]["name"]
			hist_Estimated[plot_branch] 		= file_hist.Get(f'ZZ_{plot_branch}_FakeLepEstimated_{filelist_pseudo_data[file]["name"]}')
			hist_True[plot_branch] 				= file_hist.Get(f'ZZ_{plot_branch}_FakeLepTrue_{filelist_pseudo_data[file]["name"]}')

			
	

		filelist_pseudo_data[file]["hist_True"] 		= hist_True
		filelist_pseudo_data[file]["hist_Estimated"] 	= hist_Estimated

		
	tdrStyle.setTDRStyle()
	tdrStyle.gtdr()
	
	for branch_name in branch:


			if not branch_name == "ZZ_trileptonmass":
				continue
			
			plot_branch = branch[branch_name]["name"]
			c1 = ROOT.TCanvas("","",1000,1000)

			## -- True Fake Lepton --##
			if branch[branch_name].__contains__("bin_array"):
				MC_err_T   = ROOT.TH1D("","",len(branch[plot_branch]["bin_array"])-1,array('d', branch[plot_branch]["bin_array"]))
			else:
				MC_err_T   = ROOT.TH1D("","",branch[plot_branch]["xbins"],branch[plot_branch]["xleft"],branch[plot_branch]["xright"])


			MC_err_T.Sumw2()

			# Loop samples
			for file in filelist_pseudo_data:

				# Fill stack
				MC_err_T.Add(filelist_pseudo_data[file]["hist_True"][plot_branch])


			## -- Estimated Fake Lepton --##
			if branch[branch_name].__contains__("bin_array"):
				MC_err_E   = ROOT.TH1D("","",len(branch[plot_branch]["bin_array"])-1,array('d', branch[plot_branch]["bin_array"]))
			else:
				MC_err_E   = ROOT.TH1D("","",branch[plot_branch]["xbins"],branch[plot_branch]["xleft"],branch[plot_branch]["xright"])

			MC_err_E.Sumw2()

			# Loop samples
			for file in filelist_pseudo_data:
				# Skip empty histogram
				#if filelist_pseudo_data[file]["hist_Estimated"][plot_branch].Integral() < 0.0001:
				#	continue

				# Fill stack
				MC_err_E.Add(filelist_pseudo_data[file]["hist_Estimated"][plot_branch])


			legend = ROOT.TLegend(0.20, 0.75, 0.90, 0.85)
			legend.SetNColumns(2)
			legend.SetBorderSize(0)
			legend.SetFillColor(0)
			legend.SetTextSize(0.035)
			legend.SetLineWidth(1)
			legend.SetLineStyle(0)

			# Add legend entries for ggZZ and WZG if weight is not zero
			legend.AddEntry(MC_err_T, f'True: {format(MC_err_T.GetSumOfWeights(), ".2f")}','l')
			legend.AddEntry(MC_err_E, f'Estimated: {format(MC_err_E.GetSumOfWeights(), ".2f")}','l')		
			Stat_Unc_Total_T = sum([MC_err_T.GetBinError(Bin) for Bin in range(1, MC_err_T.GetNbinsX()+1)])
			Stat_Unc_Total_E = sum([MC_err_E.GetBinError(Bin) for Bin in range(1, MC_err_E.GetNbinsX()+1)])

			#legend.AddEntry(MC_err_T, f'Stat Unc.: {format(Stat_Unc_Total_T, ".2f")}', 'F')
			#legend.AddEntry(MC_err_E, f'Stat Unc.: {format(Stat_Unc_Total_E, ".2f")}', 'F')


			c1.Draw()
			pad1 = ROOT.TPad("pad1", "pad1", 0, 0.30, 1, 1.00)
			pad1.SetTopMargin(0.1)  # joins upper and lower plot
			pad1.SetBottomMargin(0.035)  # joins upper and lower plot
			# pad1.SetGridx()
			pad1.Draw()
			# Lower ratio plot is pad2
			c1.cd()  # returns to main canvas before defining pad2
			pad2 = ROOT.TPad("pad2", "pad2", 0, 0.00, 1, 0.30)
			pad2.SetTopMargin(0.040)  # joins upper and lower plot
			pad2.SetBottomMargin(0.40)  # joins upper and lower plot
			#pad2.SetBottomMargin(0.80)  # joins upper and lower plot
			pad2.SetGridy()
			pad2.Draw()

			# draw everything
			pad1.cd()



			MC_err_T.SetMarkerColor(2)
			MC_err_T.SetLineWidth(2)
			MC_err_T.SetLineColor(2)
			MC_err_T.SetStats(0)
			MC_err_T.SetXTitle(f'{branch[plot_branch]["axis_name"]}')
			MC_err_T.SetYTitle(f'events / bin')
			SetHistStyle(MC_err_T, 2)
			MC_err_T.GetXaxis().SetLabelSize(0)

			MC_err_E.SetMarkerColor(4)
			MC_err_E.SetLineWidth(2)
			MC_err_E.SetLineColor(4)
			MC_err_E.SetStats(0)
			MC_err_E.SetXTitle(f'{branch[plot_branch]["axis_name"]}')
			MC_err_E.SetYTitle(f'events / bin')
			SetHistStyle(MC_err_E, 4)



			# -- Draw True
			#MC_err_T.SetMaximum(4.0 * MC_err_E.GetMaximum())
			MC_err_T.SetMaximum(0.8)
			MC_err_T.SetMinimum(-0.05)
			# -- Draw Estimated
			MC_err_T.Draw()
			MC_err_E.Draw("SAME")


			legend.Draw("SAME") # commented out temporarily
			# ROOT.gPad.SetLogy()
			ROOT.gPad.RedrawAxis()


			pad2.cd()

			# Scan all bin contents calculate error and save
			evt_dict={}
			for i in range(1, MC_err_T.GetNbinsX()+1):
				print("Bin: ",i)
				print("True: ",MC_err_T.GetBinContent(i))
				print("Estimated: ",MC_err_E.GetBinContent(i))
				print("Error: ",abs((MC_err_E.GetBinContent(i)-MC_err_T.GetBinContent(i)) / MC_err_T.GetBinContent(i)))
				print("")

				
				evt_dict[f"bin{i}"] = {
					"True": MC_err_T.GetBinContent(i),
					"Estimated": MC_err_E.GetBinContent(i),
					"Error": abs((MC_err_E.GetBinContent(i)-MC_err_T.GetBinContent(i)) / MC_err_T.GetBinContent(i))
				}
			np.save(f'./closure/event_contents.npy',evt_dict)

			print("Dict ./closure/event_contents.npy is saved.")
			print(evt_dict)

			h3 = createRatio(MC_err_E, MC_err_T)
			SetHistStyle(h3, 1)
			h3.SetYTitle("(E-T)/T")
			y=h3.GetYaxis()
			y.SetTitleSize(30)

			#YMAX = abs(h3.GetMaximum()) * 2
			#YMIN = -1 * YMAX

			YMAX=2
			YMIN=-2

			null2d = ROOT.TH2D("null2d", "null2d",len(branch[plot_branch]["bin_array"])-1,array('d', branch[plot_branch]["bin_array"]), 2, YMIN, YMAX)
			null2d.GetXaxis().SetTitle(f'{branch[plot_branch]["axis_name"]}')
			# Adjust y-axis settings
			y = null2d.GetYaxis()
			#y.SetNdivisions(103)
			y.SetTitle("(E-T)/T")
			y.SetNdivisions(4)
			y.SetTitleSize(35)
			y.SetTitleFont(43)
			y.SetTitleOffset(1.50)
			y.SetLabelFont(43)
			y.SetLabelSize(35)
			# Adjust x-axis settings
			x = null2d.GetXaxis()
			x.SetTitleSize(35)
			x.SetTitleFont(43)
			x.SetTitleOffset(4.5)
			x.SetLabelFont(43)
			x.SetLabelSize(35)

			null2d.Draw()		
			if not (channel in [0,1,2,3,4]):
				h3.Draw("E0X0p SAME")
			else:
				h3.Draw("E0X0p SAME")
			ROOT.gPad.RedrawAxis()
			ROOT.gStyle.SetPadLeftMargin(0.15)


			CMS_lumi(pad1, 0, 0)
			c1.Update()
			c1.SaveAs(f'./closure/True_vs_E_{channel_map[channel]}_{plot_branch}_{str(UpDown_map[UpDown])}.pdf')
			c1.SaveAs(f'./closure/True_vs_E_{channel_map[channel]}_{plot_branch}_{str(UpDown_map[UpDown])}.png')

			del c1,pad1,pad2
			print(time.time()-time_total_init)


if __name__ == "__main__":
	sys.exit(Plot())
