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
	file_hist = ROOT.TFile(f'closure/FakeLepton_closure_2017.root',"OPEN")



	# Get Histogram
	for file in filelist_pseudo_data:
		hist_True ={}
		hist_Estimated ={}
		for branch_name in branch:
			plot_branch 				= branch[branch_name]["name"]
			hist_True[plot_branch] 		= file_hist.Get(f'WZG_{plot_branch}_FakeLepEstimated_{filelist_pseudo_data[file]["name"]}')
			hist_Estimated[plot_branch] = file_hist.Get(f'WZG_{plot_branch}_FakeLepTrue_{filelist_pseudo_data[file]["name"]}')

			
	

		filelist_pseudo_data[file]["hist_True"] 		= hist_True
		filelist_pseudo_data[file]["hist_Estimated"] 	= hist_Estimated

		
	tdrStyle.setTDRStyle()
	tdrStyle.gtdr()
	
	for branch_name in branch:

			plot_branch = branch[branch_name]["name"]
			c1 = ROOT.TCanvas("","",1000,800)

			## -- True Fake Lepton --##
			if branch[branch_name].__contains__("bin_array"):
				MC_err_T   = ROOT.TH1D("","",len(branch[plot_branch]["bin_array"])-1,array('d', branch[plot_branch]["bin_array"]))
				ggZZ_sum_T = ROOT.TH1D("","",len(branch[plot_branch]["bin_array"])-1,array('d', branch[plot_branch]["bin_array"]))
				QCD_T 	   = ROOT.TH1D("","",len(branch[plot_branch]["bin_array"])-1,array('d', branch[plot_branch]["bin_array"]))
			else:
				MC_err_T   = ROOT.TH1D("","",branch[plot_branch]["xbins"],branch[plot_branch]["xleft"],branch[plot_branch]["xright"])
				ggZZ_sum_T = ROOT.TH1D("","",branch[plot_branch]["xbins"],branch[plot_branch]["xleft"],branch[plot_branch]["xright"])
				QCD_T      = ROOT.TH1D("","",branch[plot_branch]["xbins"],branch[plot_branch]["xleft"],branch[plot_branch]["xright"])

			SetHistStyle(ggZZ_sum_T, ROOT.kAzure)
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
			cidx=0
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

				# Skim	empty histogram
				if filelist_pseudo_data[file]["hist_True"][plot_branch].Integral() < 0.0001:
					continue					

				# Fill stack

				SetHistStyle(filelist_pseudo_data[file]["hist_True"][plot_branch],41+cidx)
				#SetHistStyle(filelist_pseudo_data[file]["hist_True"][plot_branch], ROOT.kAzure-(i+1))
				stack_mc_T.Add(filelist_pseudo_data[file]["hist_True"][plot_branch])
				MC_err_T.Add(filelist_pseudo_data[file]["hist_True"][plot_branch])
				cidx += 2

			# Add ggZZ and WZG and QCD
			stack_mc_T.Add(ggZZ_sum_T)
			MC_err_T.Add(ggZZ_sum_T)
			stack_mc_T.Add(QCD_T)
			MC_err_T.Add(QCD_T)
			stack_mc_T.Add(filelist_pseudo_data['WZG']["hist_True"][plot_branch])
			MC_err_T.Add(filelist_pseudo_data['WZG']["hist_True"][plot_branch])


			## -- Estimated Fake Lepton --##
			if branch[branch_name].__contains__("bin_array"):
				MC_err_E   = ROOT.TH1D("","",len(branch[plot_branch]["bin_array"])-1,array('d', branch[plot_branch]["bin_array"]))
				ggZZ_sum_E = ROOT.TH1D("","",len(branch[plot_branch]["bin_array"])-1,array('d', branch[plot_branch]["bin_array"]))
				QCD_E = ROOT.TH1D("","",len(branch[plot_branch]["bin_array"])-1,array('d', branch[plot_branch]["bin_array"]))
			else:
				MC_err_E   = ROOT.TH1D("","",branch[plot_branch]["xbins"],branch[plot_branch]["xleft"],branch[plot_branch]["xright"])
				ggZZ_sum_E = ROOT.TH1D("","",branch[plot_branch]["xbins"],branch[plot_branch]["xleft"],branch[plot_branch]["xright"])
				QCD_E = ROOT.TH1D("","",branch[plot_branch]["xbins"],branch[plot_branch]["xleft"],branch[plot_branch]["xright"])

			SetHistStyle(ggZZ_sum_E, ROOT.kPink+10)
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
			cidx=0
			for file in filelist_pseudo_data:
				# Skip ggZZ -- Combine ggZZ_4e, ggZZ_4mu, ggZZ_2e2mu
				if 'ggZZ' in file:
					ggZZ_sum_E.Add(filelist_pseudo_data[file]["hist_Estimated"][plot_branch])
					continue

				# Skip QCD
				if 'QCD' in file:
					QCD_E.Add(filelist_pseudo_data[file]["hist_Estimated"][plot_branch])
					continue

				# Skip WZG
				if 'WZG' in file:
					continue

				# Skip empty histogram
				if filelist_pseudo_data[file]["hist_Estimated"][plot_branch].Integral() < 0.0001:
					continue

				# Fill stack
				#SetHistStyle(filelist_pseudo_data[file]["hist_Estimated"][plot_branch], ROOT.kPink-cidx)
				SetHistStyle(filelist_pseudo_data[file]["hist_Estimated"][plot_branch], 41+cidx)
				stack_mc_E.Add(filelist_pseudo_data[file]["hist_Estimated"][plot_branch])
				MC_err_E.Add(filelist_pseudo_data[file]["hist_Estimated"][plot_branch])
				cidx +=2

			# Add ggZZ and WZG and QCD
			stack_mc_E.Add(QCD_E)
			MC_err_E.Add(QCD_E)
			stack_mc_E.Add(ggZZ_sum_E)
			MC_err_E.Add(ggZZ_sum_E)
			stack_mc_E.Add(filelist_pseudo_data['WZG']["hist_Estimated"][plot_branch])
			MC_err_E.Add(filelist_pseudo_data['WZG']["hist_Estimated"][plot_branch])


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

				# Skip if weight is zero
				if filelist_pseudo_data[file]["hist_True"][plot_branch].GetSumOfWeights() < 0.0001:
					continue

				legend.AddEntry(filelist_pseudo_data[file]["hist_True"][plot_branch], f'{filelist_pseudo_data[file]["name"]}: {format(filelist_pseudo_data[file]["hist_True"][plot_branch].GetSumOfWeights(), ".2f")}','F')
				#legend.AddEntry(filelist_pseudo_data[file]["hist_Estimated"][plot_branch], f'{filelist_pseudo_data[file]["name"]}: {format(filelist_pseudo_data[file]["hist_Estimated"][plot_branch].GetSumOfWeights(), ".2f")}','F')
				


			# Add legend entries for ggZZ and WZG if weight is not zero
			legend.AddEntry(filelist_pseudo_data["WZG"]["hist_True"][plot_branch], f'{filelist_pseudo_data["WZG"]["name"]}: {format(filelist_pseudo_data[file]["hist_True"][plot_branch].GetSumOfWeights(), ".2f")}','F')
			#legend.AddEntry(filelist_pseudo_data["WZG"]["hist_Estimated"][plot_branch], f'{filelist_pseudo_data["WZG"]["name"]}: {format(filelist_pseudo_data[file]["hist_Estimated"][plot_branch].GetSumOfWeights(), ".2f")}','F')
		
			if ggZZ_sum_T.GetSumOfWeights() != 0:	
				legend.AddEntry(ggZZ_sum_T,f'ggZZ: {format(ggZZ_sum_T.GetSumOfWeights(), ".2f")}', 'F')
				#legend.AddEntry(ggZZ_sum_E,f'ggZZ: {format(ggZZ_sum_E.GetSumOfWeights(), ".2f")}', 'F')

			if QCD_T.GetSumOfWeights() != 0:
				legend.AddEntry(QCD_T,f'QCD: {format(QCD_T.GetSumOfWeights(), ".2f")}', 'F')
				#legend.AddEntry(QCD_E,f'QCD: {format(QCD_E.GetSumOfWeights(), ".2f")}', 'F')

			Stat_Unc_Total_T = sum([MC_err_T.GetBinError(Bin) for Bin in range(1, MC_err_T.GetNbinsX()+1)])
			#Stat_Unc_Total_E = sum([MC_err_E.GetBinError(Bin) for Bin in range(1, MC_err_E.GetNbinsX()+1)])

			legend.AddEntry(MC_err_T, f'Stat Unc.: {format(Stat_Unc_Total_T, ".2f")}', 'F')
			#legend.AddEntry(MC_err_E, f'Stat Unc.: {format(Stat_Unc_Total_E, ".2f")}', 'F')


			c1.Draw()
			pad1 = ROOT.TPad("pad1", "pad1", 0, 0.30, 1, 1.00)
			pad1.SetTopMargin(0.1)  # joins upper and lower plot
			pad1.SetBottomMargin(0.018)  # joins upper and lower plot
			# pad1.SetGridx()
			pad1.Draw()
			# Lower ratio plot is pad2
			c1.cd()  # returns to main canvas before defining pad2
			pad2 = ROOT.TPad("pad2", "pad2", 0, 0.01, 1, 0.29)
			pad2.SetTopMargin(0)  # joins upper and lower plot
			pad2.SetBottomMargin(0.30)  # joins upper and lower plot
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
			MC_err_T.Draw("e2")
			MC_err_T.SetMaximum(3.0 * MC_err_T.GetMaximum())
			stack_mc_T.Draw("HIST SAME")
			MC_err_T.Draw("e2 SAME")
			
			# -- Draw Estimated
			#MC_err_E.Draw("e2")
			#MC_err_E.SetMaximum(3.0 * MC_err_E.GetMaximum())
			#stack_mc_E.Draw("HIST SAME")
			#MC_err_E.Draw("e2 SAME")



			legend.Draw("SAME") # commented out temporarily
			# ROOT.gPad.SetLogy()
			ROOT.gPad.RedrawAxis()

			# h1.GetXaxis().SetLabelSize(0)
			pad2.cd()
			h3 = createRatio(MC_err_T, MC_err_E)
			SetHistStyle(h3, 1)
			h3.SetYTitle("Data/Pred.")
			h4 = createRatio(MC_err_T, MC_err_T)
			SetHistStyle(h4, 1)
			if not (channel in [0,1,2,3,4]):
				h3.Draw("E0X0p")
				h4.Draw("e2 SAME")
			else:
				h4.Draw("e2")
			ROOT.gPad.RedrawAxis()

			CMS_lumi(pad1, 0, 0)
			c1.Update()
			c1.SaveAs(f'./closure/{channel_map[channel]}_{plot_branch}_{str(UpDown_map[UpDown])}.pdf')
			c1.SaveAs(f'./closure/{channel_map[channel]}_{plot_branch}_{str(UpDown_map[UpDown])}.png')
			del c1,pad1,pad2
			print (time.time()-time_total_init)






		# Old draw hist
		#c1 = ROOT.TCanvas("","",1000,1000)



		##SetHistStyle(hist_FakeLep_E, 2) #SR thesis fakeLep color  
		##SetHistStyle(hist_FakeLep_T, 4) #SR thesis fakeLep color  



		#hist_FakeLep_E.SetMarkerColor(2)
		#hist_FakeLep_T.SetMarkerColor(4)

		#hist_FakeLep_E.SetLineColor(2)
		#hist_FakeLep_T.SetLineColor(4)

		#hist_FakeLep_E.SetFillColor(2)
		#hist_FakeLep_T.SetFillColor(4)

		#hist_FakeLep_E.SetYTitle('events/bin')


		#legend = ROOT.TLegend(0.20, 0.75, 0.85, 0.95)
		##legend.SetNColumns(2)
		#legend.SetBorderSize(0)
		#legend.SetFillColor(0)
		#legend.SetTextSize(0.035)
		#legend.SetLineWidth(1)
		#legend.SetLineStyle(0)
		#legend.AddEntry(hist_FakeLep_E,f'Estimated: {format(hist_FakeLep_E.GetSumOfWeights(), ".2f")}', 'l')
		#legend.AddEntry(hist_FakeLep_T,f'True: {format(hist_FakeLep_T.GetSumOfWeights(), ".2f")}', 'l')


		#print("E: ",hist_FakeLep_E.GetSumOfWeights())
		#print("T: ",hist_FakeLep_T.GetSumOfWeights())
		#print("Unc: ",(hist_FakeLep_E.GetSumOfWeights() - hist_FakeLep_T.GetSumOfWeights()) / hist_FakeLep_T.GetSumOfWeights())

		#E1 = hist_FakeLep_E.GetBinContent(1)
		#E2 = hist_FakeLep_E.GetBinContent(2)
		#E3 = hist_FakeLep_E.GetBinContent(3)

		#T1 = hist_FakeLep_T.GetBinContent(1)
		#T2 = hist_FakeLep_T.GetBinContent(2)
		#T3 = hist_FakeLep_T.GetBinContent(3)

		#print("Error bin 1: ",(E1-T1) / T1)
		#print("Error bin 1: ",(E2-T2) / T2)
		#print("Error bin 1: ",(E3-T3) / T3)

		#c1.Draw()
		#c1.cd()  # returns to main canvas before defining pad2


		#MAX=3.0 * hist_FakeLep_T.GetMaximum()
		#hist_FakeLep_E.SetMaximum(MAX)
		#hist_FakeLep_E.SetMinimum(0)

		#hist_FakeLep_E.SetXTitle('$M_{lll}$')
		#hist_FakeLep_E.SetYTitle(f'events / bin')


		#hist_FakeLep_E.Draw()
		#hist_FakeLep_T.Draw("SAME")
		##hist_FakeLep_E.Draw("E0X0p")
		##hist_FakeLep_T.Draw("E0X0p SAME")
		#legend.Draw("SAME")

		##CMS_lumi(pad1, 0, 0)
		#c1.Update()
		#c1.SaveAs(f'./closure/FakeLepton_closure_2017.root.pdf')
		#c1.SaveAs(f'./closure/FakeLepton_closure_2017.root.png')
		##del c1,pad1,pad2
		#del c1
		#print (time.time()-time_total_init)

if __name__ == "__main__":
	sys.exit(Plot())
