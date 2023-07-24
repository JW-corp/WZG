import sys,os
import ROOT
import json
import argparse
import pandas as pd
from decimal import Decimal
import shutil


parser = argparse.ArgumentParser(description='prepare combined cards')
parser.add_argument('-f', dest='file', default='./combine.json', help='input json with configuration')
parser.add_argument('infile',default='aqgc_root_for_HC/FT0_WZG_2016.root', help='python Combine_help.py aqgc_root_for_HC/FT0_WZG_2016.root')
parser.add_argument('-idx',default=0,type=str,help='Reweight indx for aQGC')
args = parser.parse_args()

def GetHist(region, file, variable, process,idx=None):

	print str(region + '_' +  variable + '_' + process+ '_None')
	hist = file.Get(str(region + '_' +  variable + '_' + process+ '_None'))

	hist.SetDirectory(0)
	return hist

def valid_unc(cal_unc):
	if cal_unc < 1 or cal_unc < 0:
		print "Not enough accuracy for:", file, process, variable, ' bin: ', bin, ", Unc Set to 1"
		cal_unc = 1
	return cal_unc	


def process_unc(name, nominal, up, down):
	cal_unc = 1.0
	if nominal <= 0:
		print name, 'nominal equals zero in: ', process, variable, ' bin: ', bin
		cal_unc = 1
	else:
		cal_unc = 1 + (max(abs(up-nominal), abs(down-nominal)) / nominal)
	return Decimal(valid_unc(cal_unc)).quantize(Decimal("1e-06"), rounding="ROUND_HALF_UP")



def auto_cal(region, file, variable, process, uncertainty, bin,idx=None):

	cal_unc = 1.0
	hist_name = str(region + '_' +  variable + '_' + process)
	
	if 'jestotal_17' in uncertainty.lower():
		
		JES_nominal = file.Get(str(hist_name + '_None')).GetBinContent(bin)
		JES_up = file.Get(str(hist_name + '_jesTotal_17Up')).GetBinContent(bin)
		JES_down = file.Get(str(hist_name + '_jesTotal_17Down')).GetBinContent(bin)
		return process_unc('jes', JES_nominal, JES_up, JES_down)		

	elif 'jer_17' in uncertainty.lower():
		
		JER_nominal = file.Get(str(hist_name + '_None')).GetBinContent(bin)
		JER_up = file.Get(str(hist_name + '_jer_17Up')).GetBinContent(bin)
		JER_down = file.Get(str(hist_name + '_jer_17Down')).GetBinContent(bin)
		return process_unc('jer', JER_nominal, JER_up, JER_down)	


	#elif 'fakelepton_stat' in uncertainty.lower():
	#	print("##"*20)
	#	print(str(hist_name + 'FakeLep_None'))
	#	FakeLep_nominal   = file.Get(str(hist_name + '_None')).GetBinContent(bin)
	#	FakeLep_stat_up   = file.Get(str(hist_name + '_stat_up')).GetBinContent(bin)
	#	FakeLep_stat_down = file.Get(str(hist_name + '_stat_down')).GetBinContent(bin)
	#	return process_unc('FakeLepton Stat', FakeLep_nominal, FakeLep_stat_up, FakeLep_stat_down)

	#elif 'fakelepton_sys' in uncertainty.lower():
	#	
	#	FakeLep_nominal   = file.Get(str(hist_name + '_None')).GetBinContent(bin)
	#	FakeLep_sys_up    = file.Get(str(hist_name + '_sys_up')).GetBinContent(bin)
	#	FakeLep_sys_down  = file.Get(str(hist_name + '_sys_down')).GetBinContent(bin)
	#	return process_unc('FakeLepton Sys', FakeLep_nominal, FakeLep_sys_up, FakeLep_sys_down)
	
	
	elif 'fakefraction_17' in uncertainty.lower():
		
		nominal = file.Get(str(hist_name + '_None')).GetBinContent(bin)
		up = file.Get(str(hist_name + '_fakefraction_17Up')).GetBinContent(bin)
		down = file.Get(str(hist_name + '_fakefraction_17Down')).GetBinContent(bin)
		return process_unc('fakefraction_17', nominal, up, down)	

	elif 'fakerate_17' in uncertainty.lower():
		
		nominal = file.Get(str(hist_name + '_None')).GetBinContent(bin)
		up = file.Get(str(hist_name + '_fakerate_17Up')).GetBinContent(bin)
		down = file.Get(str(hist_name + '_fakerate_17Down')).GetBinContent(bin)
		return process_unc('fakerate_17', nominal, up, down)	


	elif 'stat' in uncertainty.lower() and (not 'hlt' in uncertainty.lower()):
		stat_unc = file.Get(str(hist_name + '_None')).GetBinError(bin)
		nominal = file.Get(str(hist_name + '_None')).GetBinContent(bin)
	
		if not nominal==0:
			print("######>>>>> Nominal, Error, Error/Nominal: ",process,nominal, stat_unc,stat_unc/nominal)
		if nominal == 0:
			print 'stat counts equals zero in: ', file, process, variable, ' bin: ', bin
			cal_unc = 1
		else:
			cal_unc = 1 + abs(stat_unc/nominal)
		return Decimal(valid_unc(cal_unc)).quantize(Decimal("1e-06"), rounding="ROUND_HALF_UP")
	
	elif 'photon_id' in uncertainty.lower():
		
		PhotonID_nominal = file.Get(str(hist_name + '_None')).GetBinContent(bin)
		PhotonID_up = file.Get(str(hist_name + '_Photon_ID_WeightUp')).GetBinContent(bin)
		PhotonID_down = file.Get(str(hist_name + '_Photon_ID_WeightDown')).GetBinContent(bin)
		return process_unc('photon_id', PhotonID_nominal, PhotonID_up, PhotonID_down)	

	elif 'muon_id' in uncertainty.lower():
		
		MuonID_nominal = file.Get(str(hist_name + '_None')).GetBinContent(bin)
		MuonID_up = file.Get(str(hist_name + '_Muon_ID_WeightUp')).GetBinContent(bin)
		MuonID_down = file.Get(str(hist_name + '_Muon_ID_WeightDown')).GetBinContent(bin)
		return process_unc('muon_id', MuonID_nominal, MuonID_up, MuonID_down)	

	elif 'ele_id' in uncertainty.lower():
		
		ElectronID_nominal = file.Get(str(hist_name + '_None')).GetBinContent(bin)
		ElectronID_up = file.Get(str(hist_name + '_Electron_ID_WeightUp')).GetBinContent(bin)
		ElectronID_down = file.Get(str(hist_name + '_Electron_ID_WeightDown')).GetBinContent(bin)
		return process_unc('ele_id', ElectronID_nominal, ElectronID_up, ElectronID_down)	


	elif 'ele_reco' in uncertainty.lower():
		
		ElectronRECO_nominal = file.Get(str(hist_name + '_None')).GetBinContent(bin)
		ElectronRECO_up = file.Get(str(hist_name + '_Electron_RECO_WeightUp')).GetBinContent(bin)
		ElectronRECO_down = file.Get(str(hist_name + '_Electron_RECO_WeightDown')).GetBinContent(bin)
		return process_unc('ele_reco', ElectronRECO_nominal, ElectronRECO_up, ElectronRECO_down)	

	elif 'pileup' in uncertainty.lower():
		
		nominal = file.Get(str(hist_name + '_None')).GetBinContent(bin)
		up = file.Get(str(hist_name + '_puWeightUp')).GetBinContent(bin)
		down = file.Get(str(hist_name + '_puWeightDown')).GetBinContent(bin)
		return process_unc('pileup', nominal, up, down)

	# -- only for 16 & 17	
	elif 'l1pref' in uncertainty.lower():
		
		nominal = file.Get(str(hist_name + '_None')).GetBinContent(bin)
		up = file.Get(str(hist_name + '_l1prefUp')).GetBinContent(bin)
		down = file.Get(str(hist_name + '_l1prefDown')).GetBinContent(bin)
		return process_unc('l1pref', nominal, up, down)



	# -- theory WZG
	elif 'wzg_pdf' in uncertainty.lower():
		
		nominal = file.Get(str(hist_name + '_None')).GetBinContent(bin)
		up = file.Get(str(hist_name + '_WZG_pdfUp')).GetBinContent(bin)
		down = file.Get(str(hist_name + '_WZG_pdfDown')).GetBinContent(bin)
		return process_unc('wzg_pdf', nominal, up, down)

	elif 'wzg_scale' in uncertainty.lower():
		
		nominal = file.Get(str(hist_name + '_None')).GetBinContent(bin)
		up = file.Get(str(hist_name + '_WZG_scaleUp')).GetBinContent(bin)
		down = file.Get(str(hist_name + '_WZG_scaleDown')).GetBinContent(bin)
		return process_unc('wzg_scale', nominal, up, down)

	elif 'wzg_psweight_isr' in uncertainty.lower():
		
		nominal = file.Get(str(hist_name + '_None')).GetBinContent(bin)
		up = file.Get(str(hist_name + '_WZG_PSWeight_IsrUp')).GetBinContent(bin)
		down = file.Get(str(hist_name + '_WZG_PSWeight_IsrDown')).GetBinContent(bin)
		return process_unc('wzg_psweight_isr', nominal, up, down)

	elif 'wzg_psweight_fsr' in uncertainty.lower():
		
		nominal = file.Get(str(hist_name + '_None')).GetBinContent(bin)
		up = file.Get(str(hist_name + '_WZG_PSWeight_FsrUp')).GetBinContent(bin)
		down = file.Get(str(hist_name + '_WZG_PSWeight_FsrDown')).GetBinContent(bin)
		return process_unc('wzg_psweight_fsr', nominal, up, down)


	# -- theory Top
	elif 'top_pdf' in uncertainty.lower():
		
		nominal = file.Get(str(hist_name + '_None')).GetBinContent(bin)
		up = file.Get(str(hist_name + '_Top_pdfUp')).GetBinContent(bin)
		down = file.Get(str(hist_name + '_Top_pdfDown')).GetBinContent(bin)
		return process_unc('top_pdf', nominal, up, down)

	elif 'top_scale' in uncertainty.lower():
		
		nominal = file.Get(str(hist_name + '_None')).GetBinContent(bin)
		up = file.Get(str(hist_name + '_Top_scaleUp')).GetBinContent(bin)
		down = file.Get(str(hist_name + '_Top_scaleDown')).GetBinContent(bin)
		return process_unc('top_scale', nominal, up, down)

	elif 'top_psweight_isr' in uncertainty.lower():
		
		nominal = file.Get(str(hist_name + '_None')).GetBinContent(bin)
		up = file.Get(str(hist_name + '_Top_PSWeight_IsrUp')).GetBinContent(bin)
		down = file.Get(str(hist_name + '_Top_PSWeight_IsrDown')).GetBinContent(bin)
		return process_unc('top_psweight_isr', nominal, up, down)

	elif 'top_psweight_fsr' in uncertainty.lower():
		
		nominal = file.Get(str(hist_name + '_None')).GetBinContent(bin)
		up = file.Get(str(hist_name + '_Top_PSWeight_FsrUp')).GetBinContent(bin)
		down = file.Get(str(hist_name + '_Top_PSWeight_FsrDown')).GetBinContent(bin)
		return process_unc('top_psweight_fsr', nominal, up, down)


	# -- theory VV
	elif 'vv_pdf' in uncertainty.lower():
		
		nominal = file.Get(str(hist_name + '_None')).GetBinContent(bin)
		up = file.Get(str(hist_name + '_VV_pdfUp')).GetBinContent(bin)
		down = file.Get(str(hist_name + '_VV_pdfDown')).GetBinContent(bin)
		return process_unc('vv_pdf', nominal, up, down)

	elif 'vv_scale' in uncertainty.lower():
		
		nominal = file.Get(str(hist_name + '_None')).GetBinContent(bin)
		up = file.Get(str(hist_name + '_VV_scaleUp')).GetBinContent(bin)
		down = file.Get(str(hist_name + '_VV_scaleDown')).GetBinContent(bin)
		return process_unc('vv_scale', nominal, up, down)

	elif 'vv_psweight_isr' in uncertainty.lower():
		
		nominal = file.Get(str(hist_name + '_None')).GetBinContent(bin)
		up = file.Get(str(hist_name + '_VV_PSWeight_IsrUp')).GetBinContent(bin)
		down = file.Get(str(hist_name + '_VV_PSWeight_IsrDown')).GetBinContent(bin)
		return process_unc('vv_psweight_isr', nominal, up, down)

	elif 'vv_psweight_fsr' in uncertainty.lower():
		
		nominal = file.Get(str(hist_name + '_None')).GetBinContent(bin)
		up = file.Get(str(hist_name + '_VV_PSWeight_FsrUp')).GetBinContent(bin)
		down = file.Get(str(hist_name + '_VV_PSWeight_FsrDown')).GetBinContent(bin)
		return process_unc('vv_psweight_fsr', nominal, up, down)

	# -- theory VVV
	elif 'vvv_pdf' in uncertainty.lower():
		
		nominal = file.Get(str(hist_name + '_None')).GetBinContent(bin)
		up = file.Get(str(hist_name + '_VVV_pdfUp')).GetBinContent(bin)
		down = file.Get(str(hist_name + '_VVV_pdfDown')).GetBinContent(bin)
		return process_unc('vvv_pdf', nominal, up, down)

	elif 'vvv_scale' in uncertainty.lower():
		
		nominal = file.Get(str(hist_name + '_None')).GetBinContent(bin)
		up = file.Get(str(hist_name + '_VVV_scaleUp')).GetBinContent(bin)
		down = file.Get(str(hist_name + '_VVV_scaleDown')).GetBinContent(bin)
		return process_unc('vvv_scale', nominal, up, down)

	elif 'vvv_psweight_isr' in uncertainty.lower():
		
		nominal = file.Get(str(hist_name + '_None')).GetBinContent(bin)
		up = file.Get(str(hist_name + '_VVV_PSWeight_IsrUp')).GetBinContent(bin)
		down = file.Get(str(hist_name + '_VVV_PSWeight_IsrDown')).GetBinContent(bin)
		return process_unc('vvv_psweight_isr', nominal, up, down)

	elif 'vvv_psweight_fsr' in uncertainty.lower():
		
		nominal = file.Get(str(hist_name + '_None')).GetBinContent(bin)
		up = file.Get(str(hist_name + '_VVV_PSWeight_FsrUp')).GetBinContent(bin)
		down = file.Get(str(hist_name + '_VVV_PSWeight_FsrDown')).GetBinContent(bin)
		return process_unc('vvv_psweight_fsr', nominal, up, down)


	# -- theory VG
	elif 'vg_pdf' in uncertainty.lower():
		
		nominal = file.Get(str(hist_name + '_None')).GetBinContent(bin)
		up = file.Get(str(hist_name + '_VG_pdfUp')).GetBinContent(bin)
		down = file.Get(str(hist_name + '_VG_pdfDown')).GetBinContent(bin)
		return process_unc('vg_pdf', nominal, up, down)

	elif 'vg_scale' in uncertainty.lower():
		
		nominal = file.Get(str(hist_name + '_None')).GetBinContent(bin)
		up = file.Get(str(hist_name + '_VG_scaleUp')).GetBinContent(bin)
		down = file.Get(str(hist_name + '_VG_scaleDown')).GetBinContent(bin)
		return process_unc('vg_scale', nominal, up, down)

	elif 'vg_psweight_isr' in uncertainty.lower():
		
		nominal = file.Get(str(hist_name + '_None')).GetBinContent(bin)
		up = file.Get(str(hist_name + '_VG_PSWeight_IsrUp')).GetBinContent(bin)
		down = file.Get(str(hist_name + '_VG_PSWeight_IsrDown')).GetBinContent(bin)
		return process_unc('vg_psweight_isr', nominal, up, down)

	elif 'vg_psweight_fsr' in uncertainty.lower():
		
		nominal = file.Get(str(hist_name + '_None')).GetBinContent(bin)
		up = file.Get(str(hist_name + '_VG_PSWeight_FsrUp')).GetBinContent(bin)
		down = file.Get(str(hist_name + '_VG_PSWeight_FsrDown')).GetBinContent(bin)
		return process_unc('vg_psweight_fsr', nominal, up, down)



	# -- btag
	elif 'btagweight_bc_corr' in uncertainty.lower():
		nominal = file.Get(str(hist_name + '_None')).GetBinContent(bin)
		up = file.Get(str(hist_name + '_btagWeight_bc_corrUp')).GetBinContent(bin)
		down = file.Get(str(hist_name + '_btagWeight_bc_corrDown')).GetBinContent(bin)
		return process_unc('btagWeight_bc_corr', nominal, up, down)

	elif 'btagweight_l_corr' in uncertainty.lower():
		nominal = file.Get(str(hist_name + '_None')).GetBinContent(bin)
		up = file.Get(str(hist_name + '_btagWeight_l_corrUp')).GetBinContent(bin)
		down = file.Get(str(hist_name + '_btagWeight_l_corrDown')).GetBinContent(bin)
		return process_unc('btagWeight_l_corr', nominal, up, down)

	elif 'btagweight_bc_uncorr_17' in uncertainty.lower():
		nominal = file.Get(str(hist_name + '_None')).GetBinContent(bin)
		up = file.Get(str(hist_name + '_btagWeight_bc_uncorr_17Up')).GetBinContent(bin)
		down = file.Get(str(hist_name + '_btagWeight_bc_uncorr_17Down')).GetBinContent(bin)
		return process_unc('btagWeight_bc_uncorr', nominal, up, down)

	elif 'btagweight_l_uncorr_17' in uncertainty.lower():
		nominal = file.Get(str(hist_name + '_None')).GetBinContent(bin)
		up = file.Get(str(hist_name + '_btagWeight_l_uncorr_17Up')).GetBinContent(bin)
		down = file.Get(str(hist_name + '_btagWeight_l_uncorr_17Down')).GetBinContent(bin)
		return process_unc('btagWeight_l_uncorr', nominal, up, down)



	else:
		print "Unknown nuissance parameters: ", uncertainty, " ,Set to 1.0"
		return 1.0


	



if __name__ == '__main__':

	# reweight idx >>
	idx = str(args.idx)
	# <<
	with open(args.file, "r") as f:
		jsons = json.load(f)
		f.close()
	imax = jsons['utils']['imax']
	nrateParam = jsons['utils']['nrateParam']

	for region in jsons['regions']:
		region_name = jsons['regions'][region]['file_name']
		region_plotname = jsons['regions'][region]['final_name']
		tag = jsons['regions'][region]['tag']
		variable = jsons['regions'][region]['variable']
		variable_plotname = jsons['regions'][region]['variable_plotname']

		# Get All Process >>  Order: aQGC,FakeLep,FakePho,Top,VV,VVV,VG
		df = pd.read_csv(jsons['regions'][region]['csv'])
		processes = []
		for process in df.columns:
			# skip type and uncertainty columns
			if ('type' in process) or ('uncertainty' in process):
				continue
			processes.append(process)
		print region_name + '_' + str(tag) + '.root'
		print "processes: ", processes, "\n"

		# Get all histogram
		file_region = ROOT.TFile.Open(args.infile, 'READ') # automated


		hist_region = {}
		for process in processes:
			hist_region[process] = GetHist(region_name, file_region, variable, process,idx)
		hist_region['data'] = GetHist(region_name, file_region, variable, 'data')
		
		print 'preparing cards for: ', str(region_plotname + '_' + str(tag))
		path_region = str('cards_' + region_plotname + '_' + str(tag))


		# does not remove for aQGC
		if os.path.exists(path_region):
			pass
		else:
			os.mkdir(path_region)

		
		# for aQGC --> Only consider the last bin
		lastbin= jsons['regions'][region]['bins']
		
		fname=args.infile.split('/')[-1].split('_')[0]
		#for bin in range(1, jsons['regions'][region]['bins']+1):
		for bin in [lastbin]:
			bin_content = region_plotname + '_' + variable_plotname + '_bin' + str(bin)
			#with open(path_region + '/card_' + bin_content + '.txt', 'w+') as f: # hard code
			with open(path_region + '/' + fname + '_card_' + bin_content + '.txt', 'w+') as f: # automated
				f.write('imax \t' + str(imax) + '\tnumber of channels\n')
				f.write('jmax \t' + str(len(df.columns)-2-imax) + '\tnumber of bkgs\n')
				f.write('kmax \t' + str(len(df.index)-nrateParam) + '\tnumber of NPs\n')
				f.write('----------------\n')

				f.write('bin \t' + bin_content + '\n')
				if 'SR' in region:
					# f.write('observation\t' + str(0) + '\n')
					observation = Decimal(sum([hist_region[process].GetBinContent(bin) for process in processes])).quantize(Decimal("1e-06"), rounding="ROUND_HALF_UP")
					f.write('observation\t' + str(observation) + '\n')
				else:
					observation = Decimal(sum([hist_region[process].GetBinContent(bin) for process in processes])).quantize(Decimal("1e-06"), rounding="ROUND_HALF_UP")
					# observation = Decimal(hist_region['data'].GetBinContent(bin)).quantize(Decimal("1e-06"), rounding="ROUND_HALF_UP")
					f.write('observation\t' + str(observation) + '\n')
					# f.write('observation\t' + str(hist_region['data'].GetBinContent(bin)) + '\n')
				f.write('----------------\n')

				print_length_1 = 15
				for unc in df.iloc[:,0]:
					print_length_1 = max(print_length_1, len(str(unc))+10+len("t_enriched"))

				print_length_2 = 15
				f.write('bin'.ljust(print_length_2,' '))
				f.write(' '.ljust(print_length_2,' '))
				for process in processes:
					print_length_2 = max(print_length_2, len(str(process))+1) 
					f.write(bin_content.ljust(max(print_length_2,len(bin_content))+1,' '))
				f.write('\n')

				f.write('process'.ljust(print_length_1,' '))
				f.write(' '.ljust(print_length_1,' '))
				for process in processes:
					f.write(process.ljust(print_length_2, ' '))
				f.write('\n')

				f.write('process'.ljust(print_length_1,' '))
				f.write(' '.ljust(print_length_1,' '))
				for i in range(len(processes)):
					f.write(str(i).ljust(print_length_2,' '))
				f.write('\n')

				f.write('rate'.ljust(print_length_1,' '))
				f.write(' '.ljust(print_length_1,' '))
				for process in processes:
					rate = Decimal(hist_region[process].GetBinContent(bin)).quantize(Decimal("1e-06"), rounding="ROUND_HALF_UP")
					if rate <= 0:
						print region, process, bin, "rate < 0, set to 0"
						f.write(str(0.00).ljust(print_length_2, ' '))
					else:   
						f.write(str(rate).ljust(print_length_2, ' '))
				f.write('\n')
				f.write('----------------\n')

				for row in df.index:
					# print uncertainty source 
					if "stat" in str(df.iloc[row,0]):
						f.write((str(region_plotname) + '_' + str(df.iloc[row,0])+"_bin"+str(bin)).ljust(print_length_1,' '))
					else:
						f.write(str(df.iloc[row,0]).ljust(print_length_1,' '))
					# print uncertainty type
					f.write(str(df.iloc[row,1]).ljust(print_length_1,' '))

					

					if str(df.iloc[row,1]) == 'rateParam':
						for i in range(len(df.iloc[row,2:])):
							para = df.iloc[row,i+2]
							if str(para) == 'nan':
								pass
							elif str(para) != 'auto_cal':
	
								f.write(str(para).ljust(print_length_2,' '))
					else:
						# cal and print rest
						# ---> Process Loop
						for i in range(len(df.iloc[row,2:])):
							para = df.iloc[row,i+2]
							if str(para) == 'nan':
								f.write('-'.ljust(print_length_2,' '))
							elif str(para) != 'auto_cal':
								f.write(str(para).ljust(print_length_2,' '))
							elif str(para) == 'auto_cal':
								f.write(str(auto_cal(region_name, file_region, variable, processes[i], str(df.iloc[row,0]), bin,idx)).ljust(print_length_2,' '))
					# <--
					f.write('\n')

			if observation == 0:
				print "no obs_data in path_%s/card_%s.txt, cleaning..." % (path_region, bin_content)
				#os.remove(path_region + '/card_' + bin_content + '.txt')
				pass
			
		file_region.Close()

