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

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('mode', type=str,
			help="python Plot.py E (or T)")
args = parser.parse_args()
mode = args.mode

def SetHistStyle(hist, color):

	#hist.SetLineWidth(2)
	hist.SetLineColor(color)
	hist.SetFillColor(color)
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
	file_hist = ROOT.TFile(f'closure/FakeLepton_closure_2018.root',"OPEN")



	# Get Histogram
	for file in filelist_pseudo_data:
		hist_True ={}
		hist_Estimated ={}
		for branch_name in branch:
			plot_branch 				= branch[branch_name]["name"]
			hist_True[plot_branch] 		= file_hist.Get(f'WZG_{plot_branch}_FakeLepTrue_{filelist_pseudo_data[file]["name"]}')
			hist_Estimated[plot_branch] = file_hist.Get(f'WZG_{plot_branch}_FakeLepEstimated_{filelist_pseudo_data[file]["name"]}')

			
	

		filelist_pseudo_data[file]["hist_True"] 		= hist_True
		filelist_pseudo_data[file]["hist_Estimated"] 	= hist_Estimated

		
	tdrStyle.setTDRStyle()
	tdrStyle.gtdr()
	
	for branch_name in branch:



			if not branch_name == "WZG_mlla":
				continue

			plot_branch = branch[branch_name]["name"]
			c1 = ROOT.TCanvas("","",1000,1000)

			## -- True Fake Lepton --##
			if branch[branch_name].__contains__("bin_array"):
				MC_err_T   = ROOT.TH1D("","",len(branch[plot_branch]["bin_array"])-1,array('d', branch[plot_branch]["bin_array"]))
				ggZZ_sum_T = ROOT.TH1D("","",len(branch[plot_branch]["bin_array"])-1,array('d', branch[plot_branch]["bin_array"]))
				QCD_T 	   = ROOT.TH1D("","",len(branch[plot_branch]["bin_array"])-1,array('d', branch[plot_branch]["bin_array"]))
				DYJets_T   = ROOT.TH1D("","",len(branch[plot_branch]["bin_array"])-1,array('d', branch[plot_branch]["bin_array"]))
			else:
				MC_err_T   = ROOT.TH1D("","",branch[plot_branch]["xbins"],branch[plot_branch]["xleft"],branch[plot_branch]["xright"])
				ggZZ_sum_T = ROOT.TH1D("","",branch[plot_branch]["xbins"],branch[plot_branch]["xleft"],branch[plot_branch]["xright"])
				QCD_T  = ROOT.TH1D("","",branch[plot_branch]["xbins"],branch[plot_branch]["xleft"],branch[plot_branch]["xright"])
				DYJets_T   = ROOT.TH1D("","",branch[plot_branch]["xbins"],branch[plot_branch]["xleft"],branch[plot_branch]["xright"])

			MC_err_T.Sumw2()
			MC_err_T.SetFillColor(ROOT.kGray+2)
			MC_err_T.SetFillStyle(3345)
			MC_err_T.SetMarkerSize(0.)
			MC_err_T.SetMarkerColor(ROOT.kGray+2)
			MC_err_T.SetLineWidth(2)
			MC_err_T.SetLineColor(0)
			MC_err_T.SetStats(0)

			MC_err_T.SetXTitle(f'{branch[plot_branch]["axis_name"]}')
			MC_err_T.SetYTitle(f'events / bin')

			# Define stack True
			stack_mc_T = ROOT.THStack("","")



			# Loop samples
			for file in filelist_pseudo_data:
			
				# Skip ggZZ -- Combine ggZZ_4e, ggZZ_4mu, ggZZ_2e2mu
				if 'ggZZ' in file:
					ggZZ_sum_T.Add(filelist_pseudo_data[file]["hist_True"][plot_branch])
					continue
				# Skip WZG
				if 'WZG' in file:
					continue
				# Skip QCD
				if 'QCD' in file:
					QCD_T.Add(filelist_pseudo_data[file]["hist_True"][plot_branch])
					continue
				if 'DY' in file:
					DYJets_T.Add(filelist_pseudo_data[file]["hist_True"][plot_branch])
					continue
				if 'ZG' in file:
					continue

				# Fill stack
				SetHistStyle(filelist_pseudo_data[file]["hist_True"][plot_branch],filelist_pseudo_data[file]["color"])
				stack_mc_T.Add(filelist_pseudo_data[file]["hist_True"][plot_branch])
				MC_err_T.Add(filelist_pseudo_data[file]["hist_True"][plot_branch])

			# Add WZG
			SetHistStyle(filelist_pseudo_data['WZG']["hist_True"][plot_branch],filelist_pseudo_data['WZG']["color"])
			stack_mc_T.Add(filelist_pseudo_data['WZG']["hist_True"][plot_branch])
			MC_err_T.Add(filelist_pseudo_data['WZG']["hist_True"][plot_branch])



			# Add ZG
			SetHistStyle(filelist_pseudo_data['ZGToLLG']["hist_True"][plot_branch],filelist_pseudo_data['ZGToLLG']["color"])
			stack_mc_T.Add(filelist_pseudo_data['ZGToLLG']["hist_True"][plot_branch])
			MC_err_T.Add(filelist_pseudo_data['ZGToLLG']["hist_True"][plot_branch])

			# Add QCD
			SetHistStyle(QCD_T,filelist_pseudo_data['QCD_Pt-15to20_EMEnriched']['color'])
			stack_mc_T.Add(QCD_T)
			MC_err_T.Add(QCD_T)

			# Add ggZZ
			SetHistStyle(ggZZ_sum_T,filelist_pseudo_data['ggZZ_2e2mu']['color'])
			stack_mc_T.Add(ggZZ_sum_T)
			MC_err_T.Add(ggZZ_sum_T)

			# Add DYJets
			SetHistStyle(DYJets_T,filelist_pseudo_data['DYJetsToLL_M10to50']["color"])
			stack_mc_T.Add(DYJets_T)
			MC_err_T.Add(DYJets_T)


			## -- Estimated Fake Lepton --##
			if branch[branch_name].__contains__("bin_array"):
				MC_err_E   = ROOT.TH1D("","",len(branch[plot_branch]["bin_array"])-1,array('d', branch[plot_branch]["bin_array"]))
				ggZZ_sum_E = ROOT.TH1D("","",len(branch[plot_branch]["bin_array"])-1,array('d', branch[plot_branch]["bin_array"]))
				QCD_E 	   = ROOT.TH1D("","",len(branch[plot_branch]["bin_array"])-1,array('d', branch[plot_branch]["bin_array"]))
				DYJets_E   = ROOT.TH1D("","",len(branch[plot_branch]["bin_array"])-1,array('d', branch[plot_branch]["bin_array"]))
				
			else:
				MC_err_E   = ROOT.TH1D("","",branch[plot_branch]["xbins"],branch[plot_branch]["xleft"],branch[plot_branch]["xright"])
				ggZZ_sum_E = ROOT.TH1D("","",branch[plot_branch]["xbins"],branch[plot_branch]["xleft"],branch[plot_branch]["xright"])
				QCD_E 	   = ROOT.TH1D("","",branch[plot_branch]["xbins"],branch[plot_branch]["xleft"],branch[plot_branch]["xright"])
				DYJets_E   = ROOT.TH1D("","",branch[plot_branch]["xbins"],branch[plot_branch]["xleft"],branch[plot_branch]["xright"])

			MC_err_E.Sumw2()
			MC_err_E.SetFillColor(ROOT.kGray+2)
			MC_err_E.SetFillStyle(3345)
			MC_err_E.SetMarkerSize(0.)
			MC_err_E.SetMarkerColor(ROOT.kGray+2)
			MC_err_E.SetLineWidth(2)
			MC_err_E.SetLineColor(0)
			MC_err_E.SetStats(0)
			MC_err_E.SetXTitle(f'{branch[plot_branch]["axis_name"]}')
			MC_err_E.SetYTitle(f'events / bin')

			# Define stack Estimated
			stack_mc_E = ROOT.THStack("","")


			# Loop samples
			for file in filelist_pseudo_data:
				# Skip ggZZ -- Combine ggZZ_4e, ggZZ_4mu, ggZZ_2e2mu
				if 'ggZZ' in file:
					ggZZ_sum_E.Add(filelist_pseudo_data[file]["hist_Estimated"][plot_branch])
					continue

				# Skim ZG
				if 'ZG' in file:
					continue

				# Skip QCD
				if 'QCD' in file:
					QCD_E.Add(filelist_pseudo_data[file]["hist_Estimated"][plot_branch])
					continue

				# Skip WZG
				if 'WZG' in file:
					continue

				# Skip DYJets
				if 'DY' in file:
					DYJets_E.Add(filelist_pseudo_data[file]["hist_Estimated"][plot_branch])
					continue


				# Fill stack
				SetHistStyle(filelist_pseudo_data[file]["hist_Estimated"][plot_branch], filelist_pseudo_data[file]["color"])
				stack_mc_E.Add(filelist_pseudo_data[file]["hist_Estimated"][plot_branch])
				MC_err_E.Add(filelist_pseudo_data[file]["hist_Estimated"][plot_branch])


			# Add WZG
			SetHistStyle(filelist_pseudo_data['WZG']["hist_Estimated"][plot_branch],filelist_pseudo_data['WZG']["color"])
			stack_mc_E.Add(filelist_pseudo_data['WZG']["hist_Estimated"][plot_branch])
			MC_err_E.Add(filelist_pseudo_data['WZG']["hist_Estimated"][plot_branch])

			# Add ZGToLLG
			SetHistStyle(filelist_pseudo_data['ZGToLLG']["hist_Estimated"][plot_branch],filelist_pseudo_data['ZGToLLG']["color"])
			stack_mc_E.Add(filelist_pseudo_data['ZGToLLG']["hist_Estimated"][plot_branch])
			MC_err_E.Add(filelist_pseudo_data['ZGToLLG']["hist_Estimated"][plot_branch])

			# Add QCD
			SetHistStyle(QCD_E,filelist_pseudo_data['QCD_Pt-15to20_EMEnriched']['color'])
			stack_mc_E.Add(QCD_E)
			MC_err_E.Add(QCD_E)

			# Add ggZZ
			SetHistStyle(ggZZ_sum_E,filelist_pseudo_data['ggZZ_2e2mu']['color'])
			stack_mc_E.Add(ggZZ_sum_E)
			MC_err_E.Add(ggZZ_sum_E)

			# Add DYJets
			SetHistStyle(DYJets_E,filelist_pseudo_data['DYJetsToLL_M10to50']["color"])
			stack_mc_E.Add(DYJets_E)
			MC_err_E.Add(DYJets_E)






			# -- Commented out -- #
			legend = ROOT.TLegend(0.20, 0.45, 0.90, 0.85)
			legend.SetNColumns(2)
			legend.SetBorderSize(0)
			legend.SetFillColor(0)
			legend.SetTextSize(0.035)
			legend.SetLineWidth(1)
			legend.SetLineStyle(0)

			# Add legend entries without ggZZ and WZG
			for file in filelist_pseudo_data:
				if 'ggZZ' in file:
					continue
				if 'QCD' in file:
					continue
				if 'WZG' in file:
					continue
				if 'DY' in file:
					continue

				if mode == "T":
					legend.AddEntry(filelist_pseudo_data[file]["hist_True"][plot_branch], f'{filelist_pseudo_data[file]["name"]}: {format(filelist_pseudo_data[file]["hist_True"][plot_branch].GetSumOfWeights(), ".2f")}','F')
				elif mode == "E":
					legend.AddEntry(filelist_pseudo_data[file]["hist_Estimated"][plot_branch], f'{filelist_pseudo_data[file]["name"]}: {format(filelist_pseudo_data[file]["hist_Estimated"][plot_branch].GetSumOfWeights(), ".2f")}','F')
				else:
					print("Wrong argument")
					exit()

			# Add legend entries for ggZZ and WZG if weight is not zero

			if mode == "T":
				legend.AddEntry(filelist_pseudo_data["WZG"]["hist_True"][plot_branch], f'{filelist_pseudo_data["WZG"]["name"]}: {format(filelist_pseudo_data[file]["hist_True"][plot_branch].GetSumOfWeights(), ".2f")}','F')
				legend.AddEntry(ggZZ_sum_T,f'ggZZ: {format(ggZZ_sum_T.GetSumOfWeights(), ".2f")}', 'F')
				legend.AddEntry(QCD_T,f'QCD: {format(QCD_T.GetSumOfWeights(), ".2f")}', 'F')
				legend.AddEntry(DYJets_T,f'DYJets: {format(DYJets_T.GetSumOfWeights(), ".2f")}', 'F')
				Stat_Unc_Total_T = sum([MC_err_T.GetBinError(Bin) for Bin in range(1, MC_err_T.GetNbinsX()+1)])
				legend.AddEntry(MC_err_T, f'Stat Unc.: {format(Stat_Unc_Total_T, ".2f")}', 'F')
			
			elif mode == "E":
				legend.AddEntry(filelist_pseudo_data["WZG"]["hist_Estimated"][plot_branch], f'{filelist_pseudo_data["WZG"]["name"]}: {format(filelist_pseudo_data[file]["hist_Estimated"][plot_branch].GetSumOfWeights(), ".2f")}','F')
				legend.AddEntry(ggZZ_sum_E,f'ggZZ: {format(ggZZ_sum_E.GetSumOfWeights(), ".2f")}', 'F')
				legend.AddEntry(QCD_E,f'QCD: {format(QCD_E.GetSumOfWeights(), ".2f")}', 'F')
				legend.AddEntry(DYJets_E,f'DYJets: {format(DYJets_E.GetSumOfWeights(), ".2f")}', 'F')
				Stat_Unc_Total_E = sum([MC_err_E.GetBinError(Bin) for Bin in range(1, MC_err_E.GetNbinsX()+1)])
				legend.AddEntry(MC_err_E, f'Stat Unc.: {format(Stat_Unc_Total_E, ".2f")}', 'F')
			else:
				print("Wrong argument")
				exit()
						

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
			pad2.SetGridy()
			pad2.Draw()

			# draw everything
			pad1.cd()
			#if not (channel in [0,1,2,3,4]):
			#	hist_data[plot_branch].SetXTitle(f'{branch[plot_branch]["axis_name"]}')
			#	SetHistStyle(hist_data[plot_branch], 1)
			#	hist_data[plot_branch].Draw("E0X0p")
			#	# hist_data.SetMinimum(10)
			#	hist_data[plot_branch].SetMaximum(2.5*hist_data[plot_branch].GetMaximum())
			#	stack_mc.Draw("HIST SAME")
			#	MC_err.Draw("e2 SAME")
			#	hist_data[plot_branch].Draw("E0X0p SAME")
			#	hist_data[plot_branch].GetXaxis().SetLabelSize(0)
			#else:

			
			# -- Draw True
			if mode == "T":
				MC_err_T.SetXTitle(f'{branch[plot_branch]["axis_name"]}')
				MC_err_T.GetXaxis().SetLabelSize(0)
				MC_err_T.Draw("e2")
				#MC_err_T.SetMaximum(6.0 * MC_err_T.GetMaximum())
				MC_err_T.SetMaximum(21.0)
				MC_err_T.SetMinimum(-0.3)
				stack_mc_T.Draw("HIST SAME")
				MC_err_T.Draw("e2 SAME")
			elif mode == "E":
				MC_err_E.SetXTitle(f'{branch[plot_branch]["axis_name"]}')
				MC_err_E.GetXaxis().SetLabelSize(0)
				MC_err_E.Draw("e2")
				#MC_err_E.SetMaximum(6.0 * MC_err_E.GetMaximum())
				MC_err_E.SetMaximum(21.0)
				MC_err_E.SetMinimum(-0.3)
				stack_mc_E.Draw("HIST SAME")
				MC_err_E.Draw("e2 SAME")
			else:
				print("Wrong argument")
				exit()

			legend.Draw("SAME") # commented out temporarily
			# ROOT.gPad.SetLogy()
			ROOT.gPad.RedrawAxis()

			# h1.GetXaxis().SetLabelSize(0)
			pad2.cd()
			h3 = createRatio(MC_err_T, MC_err_E)
			SetHistStyle(h3, 1)

			h4 = createRatio(MC_err_T, MC_err_T)
			SetHistStyle(h4, 1)

			h3.SetYTitle("Data/Pred.")
			h4.SetYTitle("Data/Pred.")
			h3.SetXTitle(f'{branch[plot_branch]["axis_name"]}')
			h4.SetXTitle(f'{branch[plot_branch]["axis_name"]}')

		
			if not (channel in [0,1,2,3,4]):
				h3.Draw("E0X0p")
				h4.Draw("e2 SAME")
			else:
				h4.Draw("e2")
			ROOT.gPad.RedrawAxis()
			ROOT.gStyle.SetPadLeftMargin(0.15)

			CMS_lumi(pad1, 0, 0)
			c1.Update()

			if mode == "T":
				c1.SaveAs(f'./closure/T_{channel_map[channel]}_{plot_branch}_{str(UpDown_map[UpDown])}.pdf')
				c1.SaveAs(f'./closure/T_{channel_map[channel]}_{plot_branch}_{str(UpDown_map[UpDown])}.png')
			elif mode == "E":
				c1.SaveAs(f'./closure/E_{channel_map[channel]}_{plot_branch}_{str(UpDown_map[UpDown])}.pdf')
				c1.SaveAs(f'./closure/E_{channel_map[channel]}_{plot_branch}_{str(UpDown_map[UpDown])}.png')
			else:
				print("Wrong argument")
				exit()

			del c1,pad1,pad2
			print (time.time()-time_total_init)


if __name__ == "__main__":
	sys.exit(Plot())
