import matplotlib
import uproot
import numpy
import awkward as ak
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
import pandas as pd
from tqdm import trange
import ROOT
import os,sys
from array import array
import time
import vector



def Make4Vec(target_arrays):
	lep1_pt  = target_arrays["WZG_lepton1_pt"]
	lep1_eta = target_arrays["WZG_lepton1_eta"]
	lep1_phi = target_arrays["WZG_lepton1_phi"]
	lep1_m   = target_arrays["WZG_lepton1_mass"]
	lep2_pt  = target_arrays["WZG_lepton2_pt"]
	lep2_eta = target_arrays["WZG_lepton2_eta"]
	lep2_phi = target_arrays["WZG_lepton2_phi"]
	lep2_m   = target_arrays["WZG_lepton2_mass"]
	lep3_pt  = target_arrays["WZG_lepton3_pt"]
	lep3_eta = target_arrays["WZG_lepton3_eta"]
	lep3_phi = target_arrays["WZG_lepton3_phi"]
	lep3_m   = target_arrays["WZG_lepton3_mass"]
	pho_pt   = target_arrays["WZG_photon_pt"]
	pho_eta  = target_arrays["WZG_photon_eta"]
	pho_phi  = target_arrays["WZG_photon_phi"]
	pho_m= target_arrays["WZG_photon_mass"]

	Ele1vec =  vector.array({"pt":lep1_pt ,"eta":lep1_eta ,"phi":lep1_phi ,"M":lep1_m})
	Ele2vec =  vector.array({"pt":lep2_pt ,"eta":lep2_eta ,"phi":lep2_phi ,"M":lep2_m})
	Ele3vec =  vector.array({"pt":lep3_pt ,"eta":lep3_eta ,"phi":lep3_phi ,"M":lep3_m})
	Phovec  =  vector.array({"pt":pho_pt  ,"eta":pho_eta  ,"phi":pho_phi  ,"M":pho_m})
	lllA_vec = Ele1vec + Ele2vec + Ele3vec + Phovec

	# Please modify here to output other 4vectors
	return lllA_vec


def HLT_cut(file, arrays):
	HLT_SingleMuon = arrays['HLT_IsoTkMu24'] == True
	HLT_DoubleMuon = arrays['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL']
	HLT_SingleElectron = arrays['HLT_Ele27_WPTight_Gsf'] == True
	HLT_DoubleEG = arrays['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'] == True
	HLT_MuonEG1  = arrays['HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL'] == True
	HLT_MuonEG2  = arrays['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL'] == True

	if 'SingleMuon' in file:
		arrays = arrays[HLT_SingleMuon]
	elif 'DoubleMuon' in file:
		arrays = arrays[~HLT_SingleMuon & HLT_DoubleMuon]
	elif 'SingleElectron' in file:
		arrays = arrays[~HLT_SingleMuon & ~HLT_DoubleMuon & HLT_SingleElectron]
	elif 'DoubleEG' in file:
		arrays = arrays[~HLT_SingleMuon & ~HLT_DoubleMuon & ~HLT_SingleElectron & HLT_DoubleEG]
	elif 'MuonEG' in file:
		arrays = arrays[~HLT_SingleMuon & ~HLT_DoubleMuon & ~HLT_SingleElectron & ~HLT_DoubleEG & (HLT_MuonEG1 | HLT_MuonEG2)]
	else:
		arrays = arrays[HLT_SingleMuon | HLT_DoubleMuon |  HLT_SingleElectron | HLT_DoubleEG | HLT_MuonEG1 | HLT_MuonEG2]
	return arrays

def channel_cut(channel, arrays):
	mark = {
		0 : (arrays['channel_mark'] >= 1)  & (arrays['channel_mark'] <= 4),
		10: (arrays['channel_mark'] >= 11) & (arrays['channel_mark'] <= 14),
		9 : (arrays['channel_mark'] >= 5)  & (arrays['channel_mark'] <= 8),
		20: (arrays['channel_mark'] >= 21) & (arrays['channel_mark'] <= 24),
		30: (arrays['channel_mark'] >= 31) & (arrays['channel_mark'] <= 32)
	}
	if channel in mark.keys():
		arrays = arrays[mark[channel]]
	else:
		cut = arrays['channel_mark'] == channel
		arrays = arrays[cut]

	# SR final cut
	if channel in [0,1,2,3,4]:


		sel = ((arrays['mwa'] < 75) | (arrays['mwa'] > 105))\
			  & (arrays['WZG_trileptonmass'] > 100)\
			  & ((arrays['WZG_dileptonmass'] > 75) & (arrays['WZG_dileptonmass'] < 105))
		arrays = arrays[sel]
		

	# FakeLep CR final cut	
	if channel in [10,11,12,1314]:

		sel = (arrays['ttZ_trileptonmass'] > 100) \
				& ((arrays['ttZ_dileptonmass'] < 75) | (arrays['ttZ_dileptonmass'] > 105))
		arrays = arrays[sel]

	# ZZ CR final cut
	if channel in [5,6,7,8,9]:
		sel = (arrays['ZZ_mllz2'] > 75) & (arrays['ZZ_mllz2'] < 105) & (arrays['nbJets'] ==0)
		arrays = arrays[sel]

	# FakePho CR final cut
	if channel in [30,31,32]:

		sel = ((arrays['ZGJ_mlla'] + arrays['ZGJ_dileptonmass']) > 182) \
		& (arrays['ZGJ_dileptonmass'] > 75) & (arrays['ZGJ_dileptonmass'] < 105)

		arrays = arrays[sel]

	return arrays

def lep_gen_cut(channel, arrays):
	lep_gen_cut_WZG =	((arrays['WZG_lepton1_genPartFlav'] == 1) | (arrays['WZG_lepton1_genPartFlav'] == 15)) &\
						((arrays['WZG_lepton2_genPartFlav'] == 1) | (arrays['WZG_lepton2_genPartFlav'] == 15)) &\
						((arrays['WZG_lepton3_genPartFlav'] == 1) | (arrays['WZG_lepton3_genPartFlav'] == 15))

	lep_gen_cut_ttG =   ((arrays['ttG_lepton1_genPartFlav'] == 1) | (arrays['ttG_lepton1_genPartFlav'] == 15)) &\
						((arrays['ttG_lepton2_genPartFlav'] == 1) | (arrays['ttG_lepton2_genPartFlav'] == 15)) &\
						((arrays['ttG_lepton3_genPartFlav'] == 1) | (arrays['ttG_lepton3_genPartFlav'] == 15))

	lep_gen_cut_ZGJ =	((arrays['ZGJ_lepton1_genPartFlav'] == 1) | (arrays['ZGJ_lepton1_genPartFlav'] == 15)) &\
						((arrays['ZGJ_lepton2_genPartFlav'] == 1) | (arrays['ZGJ_lepton2_genPartFlav'] == 15)) 

	if channel in [10,11,12,13,14,5,6,7,8,9]:
		lep_gen_cut_ttZ =   ((arrays['ttZ_lepton1_genPartFlav'] == 1) | (arrays['ttZ_lepton1_genPartFlav'] == 15)) &\
							((arrays['ttZ_lepton2_genPartFlav'] == 1) | (arrays['ttZ_lepton2_genPartFlav'] == 15)) &\
							((arrays['ttZ_lepton3_genPartFlav'] == 1) | (arrays['ttZ_lepton3_genPartFlav'] == 15))

		lep_gen_cut_ZZ =	((arrays['ZZ_lepton1_genPartFlav']  == 1) | (arrays['ZZ_lepton1_genPartFlav']  == 15)) &\
							((arrays['ZZ_lepton2_genPartFlav']  == 1) | (arrays['ZZ_lepton2_genPartFlav']  == 15)) &\
							((arrays['ZZ_lepton3_genPartFlav']  == 1) | (arrays['ZZ_lepton3_genPartFlav']  == 15)) &\
							((arrays['ZZ_lepton4_genPartFlav']  == 1) | (arrays['ZZ_lepton4_genPartFlav']  == 15))
	else:
		lep_gen_cut_ttZ = None
		lep_gen_cut_ZZ = None

	lep_gen_cut_map = {
					0:lep_gen_cut_WZG, 
					1:lep_gen_cut_WZG,
					2:lep_gen_cut_WZG,
					3:lep_gen_cut_WZG,
					4:lep_gen_cut_WZG,
					10:lep_gen_cut_ttZ,
					11:lep_gen_cut_ttZ,
					12:lep_gen_cut_ttZ,
					13:lep_gen_cut_ttZ,
					14:lep_gen_cut_ttZ,
					20:lep_gen_cut_ttG,
					21:lep_gen_cut_ttG,
					22:lep_gen_cut_ttG,
					23:lep_gen_cut_ttG,
					24:lep_gen_cut_ttG,
					5:lep_gen_cut_ZZ,
					6:lep_gen_cut_ZZ,
					7:lep_gen_cut_ZZ,
					8:lep_gen_cut_ZZ,
					9:lep_gen_cut_ZZ,
					30:lep_gen_cut_ZGJ,
					31:lep_gen_cut_ZGJ,
					32:lep_gen_cut_ZGJ
	}
	if channel in lep_gen_cut_map:
		return arrays[lep_gen_cut_map[channel]]
	else:
		return arrays

def pho_gen_cut(channel, arrays):
	pho_gen_cut_WZG = (arrays['WZG_photon_genPartFlav'] > 0)
	pho_gen_cut_ttG = (arrays['ttG_photon_genPartFlav'] > 0)
	pho_gen_cut_ZGJ = (arrays['ZGJ_photon_genPartFlav'] == 1)
	pho_gen_cut_map = {
					0:pho_gen_cut_WZG,
					1:pho_gen_cut_WZG,
					2:pho_gen_cut_WZG,
					3:pho_gen_cut_WZG,
					4:pho_gen_cut_WZG,
					20:pho_gen_cut_ttG,
					21:pho_gen_cut_ttG,
					22:pho_gen_cut_ttG,
					23:pho_gen_cut_ttG,
					24:pho_gen_cut_ttG,
					30:pho_gen_cut_ZGJ,
					31:pho_gen_cut_ZGJ,
					32:pho_gen_cut_ZGJ
	}
	if channel in pho_gen_cut_map:
		return arrays[pho_gen_cut_map[channel]]
	else:
		return arrays



def AddHist(file, hist, isData, xsec, lumi, channel, branch):
	
	UpDown_map={
		0:None,
		1:"jesTotalUp",
		2:"jesTotalDown",
		3:"jerUp",
		4:"jerDown"
	}

	init_time = time.time()
	init_branches = ['channel_mark',\
					'region_mark',\
					'mwa',
					'WZG_photon_pt',
					'WZG_lepton1_mass',
					'WZG_lepton2_mass',
					'WZG_lepton3_mass',
					'WZG_photon_mass',
					'WZG_trileptonmass',
					'WZG_dileptonmass',
					'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',\
					'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL',\
					'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL',\
					'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL',\
					'HLT_Ele27_WPTight_Gsf',\
					'HLT_IsoTkMu24'
					]


	if isData:
		print('is Data')
		for branch_name in branch:

			# >>>added by Jiwoong only for aQGC
			if branch_name == "WZG_mllla":
				continue
			# <<<

			if branch[branch_name]["name"] not in init_branches:
				init_branches.append(branch[branch_name]["name"])
	else:
		print('is MC')
		add_branches = ['Generator_weight']
		met_branches = uproot.open(file+':Events').keys(filter_name='MET_T1Smear*')
		gen_lepton_branches = uproot.open(file+':Events').keys(filter_name='*_lepton*genPartFlav')
		gen_photon_branches= uproot.open(file+':Events').keys(filter_name='*_photon*genPartFlav')
		lepID_weight_branches= uproot.open(file+':Events').keys(filter_name='*ID_Weight*')
		lepRECO_weight_branches= uproot.open(file+':Events').keys(filter_name='*RECO_Weight*')
		btag_weight_branches= uproot.open(file+':Events').keys(filter_name='*btagWeight*')
		l1_weight_branches = uproot.open(file+':Events').keys(filter_name='L1PreFiringWeight*')
		pu_branches = uproot.open(file+':Events').keys(filter_name='puWeight*')
		true_events = uproot.open(file)['nEventsGenWeighted'].values()[0]
		init_branches.extend(l1_weight_branches)
		init_branches.extend(add_branches)
		init_branches.extend(gen_lepton_branches)
		init_branches.extend(gen_photon_branches)
		init_branches.extend(met_branches)
		init_branches.extend(lepID_weight_branches)
		init_branches.extend(lepRECO_weight_branches)
		init_branches.extend(btag_weight_branches)
		init_branches.extend(pu_branches)


		# Added by Jiwoong for Reweight aQGC
		file_basename = file.split('/')[-1]
		if file_basename == "LLWA_aQGC_UL16Pre_Skim.root":
			init_branches.extend(['LHEReweightingWeight'])
			init_branches.extend(['LHEWeight_originalXWGTUP'])
		# <<<<<<<<<


			
		for branch_name in branch:


			# >>>added by Jiwoong
			if branch_name == "WZG_mllla":
				continue
			# <<<
			if branch[branch_name]["name"] not in init_branches:
				init_branches.append(branch[branch_name]["name"])
		
	arrays = uproot.open(file+':Events').arrays(init_branches)

	print("##"*20)
	print("Initial events: ",len(arrays))
	print("##"*20)

	arrays = HLT_cut(file, arrays)
	print("Cut1 HLT: ",len(arrays))

	arrays = channel_cut(channel, arrays)
	print("Cut2 channel: ",len(arrays))


	# -----> aQGC photonPT cuts are added
	aQGC_photon_pt_cut = arrays['WZG_photon_pt'] > 60
	arrays = arrays[aQGC_photon_pt_cut]
	print("Cut3: Photon pT: ",len(arrays))
	# <-----  -JiWoong-

	# >> Add lllA mass calculation
	lllA_vec = Make4Vec(arrays)
	arrays["WZG_mllla"] = lllA_vec.mass
	# <<--- Added my Jiwoong

	region_cut = arrays['region_mark'] == 1
	arrays = arrays[region_cut]
	print("Cut4: Region mark: ",len(arrays))

	# -- Processing and Filling hist if Data	
	if isData:
		if channel in [0,1,2,3,4, 10,11,12,13,14, 20,21,22,23,24, 30,31,32]:
			MET_cut = (arrays['MET'] > 30)
		elif channel in [5,6,7,8,9]:
			MET_cut = (arrays['MET'] <= 30)
		else:
			MET_cut = (arrays['MET'] >= 0)
		arrays = arrays[MET_cut]


		for branch_name in branch:


			# >> Add this k to only fill WZG mllla
			if branch_name != "WZG_mllla":
				continue
			# <<<			

			for i in trange(0, len(arrays[branch[branch_name]["name"]]), desc=f'fill {branch[branch_name]["name"]} for {file}'):
				hist[branch_name].Fill(float(arrays[branch[branch_name]["name"]][i]))
			print (f"SumOfWeights for {branch_name}: ", hist[branch_name].GetSumOfWeights())
	
	# -- Processing and Filling hist if MC
	else:
		print("Applying lep_gen_cut and pho_gen_cut to MC files")
		arrays = lep_gen_cut(channel, arrays)
		arrays = pho_gen_cut(channel, arrays)
		print("Cut5: gen-cut: ",len(arrays))

		arrays['Generator_weight_sgn'] = ak.where(arrays['Generator_weight'] >=0,1,-1)


		arrays['Photon_ID_Weight']			= ak.where(arrays['Photon_ID_Weight'] ==0,1,arrays['Photon_ID_Weight'])
		arrays['Photon_ID_Weight_UP']		= ak.where(arrays['Photon_ID_Weight_UP'] ==0,1,arrays['Photon_ID_Weight_UP'])
		arrays['Photon_ID_Weight_DOWN']		= ak.where(arrays['Photon_ID_Weight_DOWN']==0,1,arrays['Photon_ID_Weight_DOWN'])
		arrays['Muon_ID_Weight']			= ak.where(arrays['Muon_ID_Weight'] ==0,1,arrays['Muon_ID_Weight'])
		arrays['Muon_ID_Weight_UP']			= ak.where(arrays['Muon_ID_Weight_UP'] ==0,1,arrays['Muon_ID_Weight_UP'])
		arrays['Muon_ID_Weight_DOWN']		= ak.where(arrays['Muon_ID_Weight_DOWN']==0,1,arrays['Muon_ID_Weight_DOWN'])
		arrays['Electron_ID_Weight']		= ak.where(arrays['Electron_ID_Weight']==0,1,arrays['Electron_ID_Weight'])
		arrays['Electron_ID_Weight_UP']		= ak.where(arrays['Electron_ID_Weight_UP']==0,1,arrays['Electron_ID_Weight_UP'])
		arrays['Electron_ID_Weight_DOWN']	= ak.where(arrays['Electron_ID_Weight_DOWN']==0,1,arrays['Electron_ID_Weight_DOWN'])
		arrays['Electron_RECO_Weight']		= ak.where(arrays['Electron_RECO_Weight']==0,1,arrays['Electron_RECO_Weight'])
		arrays['Electron_RECO_Weight_UP']	= ak.where(arrays['Electron_RECO_Weight_UP']==0,1,arrays['Electron_RECO_Weight_UP'])
		arrays['Electron_RECO_Weight_DOWN'] = ak.where(arrays['Electron_RECO_Weight_DOWN']==0,1,arrays['Electron_RECO_Weight_DOWN'])

		
		# >> for only aQGC
		file_basename = file.split('/')[-1]
	
		#------------->  Reweight
		if file_basename == "LLWA_aQGC_UL16Pre_Skim.root":
		
			print("Start reweighting-----------------------------------")
			# number of reweight per events
			#len_weight = len(uproot.open(file+':Events')["LHEReweightingWeight"].array()[0])
			len_weight = 1

			print(f"threre are {len_weight} reweights")
			for i in range(len_weight):
				print(f"processing reweight {i}")
				arrays['xsec'] = arrays["LHEReweightingWeight"][:,i] * arrays["LHEWeight_originalXWGTUP"]
		
				# Note that there are 3 filling methods which means 3 different weights and arrays. We should do deep copy for each array
				# Actually the ID RECO up and down is okay but JES and JET needs different cuts so I apply deepcopy.
				## --- 1. Fill nominal
				print("Filling nominal:")
				# Note that: Make additional array because of applying MET cuts for each array and sync dimension
				arrays[f'true_weight_Rwt{i}'] = arrays['puWeight'] * arrays['Muon_ID_Weight'] * arrays['Electron_ID_Weight'] * arrays['Electron_RECO_Weight'] * lumi * arrays['xsec'] * 1000 * arrays['Generator_weight_sgn'] * arrays["Photon_ID_Weight"] * arrays['L1PreFiringWeight_Nom']  / true_events
				if channel in [0,1,2,3,4, 10,11,12,13,14, 20,21,22,23,24, 30,31,32]:
					MET_cut = (arrays['MET_T1Smear_pt'] > 30)
					arrays_copy_nominal = ak.copy(arrays[MET_cut]) # deep copy
				elif channel in [5,6,7,8,9]:
					MET_cut = (arrays['MET_T1Smear_pt'] <= 30)
					arrays_copy_nominal = ak.copy(arrays[MET_cut])
				else:
					arrays_copy_nominal = ak.copy(arrays)
	
				for branch_name in branch:

					# only for aQGC variable WZG_mllla
					if branch_name != "WZG_mllla":
						continue

					# Fill it!
					for j in trange(0, len(arrays_copy_nominal[branch[branch_name]["name"]]), desc=f'fill {branch[branch_name]["name"]} for {file} in {UpDown_map[0]}_Rwt{i}'):
						#print("Final Check: ",float(arrays_copy_nominal[branch[branch_name]["name"]][j]),float(arrays_copy_nominal[f'true_weight_Rwt{i}'][j]))
						hist[branch_name+f"_{UpDown_map[0]}_Rwt{i}"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]][j]), float(arrays_copy_nominal[f'true_weight_Rwt{i}'][j]))
				print("\n")

				## --- 2. Fill lep ID RECO up down
				print("Filling up down:")

				arrays_copy_nominal['true_weight_PhotonIDup_Rwt{i}']		= arrays_copy_nominal['puWeight'] 	 * arrays_copy_nominal['L1PreFiringWeight_Nom']	* arrays_copy_nominal['Muon_ID_Weight'] 	* arrays_copy_nominal['Photon_ID_Weight_UP'] 		* arrays_copy_nominal['Electron_ID_Weight'] * arrays_copy_nominal['Electron_RECO_Weight'] * lumi * arrays_copy_nominal['xsec'] * 1000 * arrays_copy_nominal['Generator_weight_sgn'] / true_events
				arrays_copy_nominal['true_weight_PhotonIDdown_Rwt{i}']	 	= arrays_copy_nominal['puWeight'] 	 * arrays_copy_nominal['L1PreFiringWeight_Nom']	* arrays_copy_nominal['Muon_ID_Weight']		* arrays_copy_nominal['Photon_ID_Weight_DOWN'] 	* arrays_copy_nominal['Electron_ID_Weight'] * arrays_copy_nominal['Electron_RECO_Weight'] * lumi * arrays_copy_nominal['xsec'] * 1000 * arrays_copy_nominal['Generator_weight_sgn'] / true_events

				arrays_copy_nominal['true_weight_MuonIDup_Rwt{i}']		 	= arrays_copy_nominal['puWeight'] 	 * arrays_copy_nominal['L1PreFiringWeight_Nom']	* arrays_copy_nominal['Muon_ID_Weight_UP'] 	* arrays_copy_nominal['Photon_ID_Weight'] 		* arrays_copy_nominal['Electron_ID_Weight'] * arrays_copy_nominal['Electron_RECO_Weight'] * lumi * arrays_copy_nominal['xsec'] * 1000 * arrays_copy_nominal['Generator_weight_sgn'] / true_events
				arrays_copy_nominal['true_weight_MuonIDdown_Rwt{i}']	 	= arrays_copy_nominal['puWeight'] 	 * arrays_copy_nominal['L1PreFiringWeight_Nom']	* arrays_copy_nominal['Muon_ID_Weight_DOWN']* arrays_copy_nominal['Photon_ID_Weight'] 	* arrays_copy_nominal['Electron_ID_Weight'] * arrays_copy_nominal['Electron_RECO_Weight'] * lumi * arrays_copy_nominal['xsec'] * 1000 * arrays_copy_nominal['Generator_weight_sgn'] / true_events
				arrays_copy_nominal['true_weight_ElectronIDup_Rwt{i}'] 		= arrays_copy_nominal['puWeight'] 	 * arrays_copy_nominal['L1PreFiringWeight_Nom']	* arrays_copy_nominal['Muon_ID_Weight'] 	* arrays_copy_nominal['Photon_ID_Weight'] 		* arrays_copy_nominal['Electron_ID_Weight_UP'] * arrays_copy_nominal['Electron_RECO_Weight'] * lumi * arrays_copy_nominal['xsec'] * 1000 * arrays_copy_nominal['Generator_weight_sgn'] / true_events
				arrays_copy_nominal['true_weight_ElectronIDdown_Rwt{i}'] 	= arrays_copy_nominal['puWeight'] 	 * arrays_copy_nominal['L1PreFiringWeight_Nom']	* arrays_copy_nominal['Muon_ID_Weight'] 	* arrays_copy_nominal['Photon_ID_Weight'] 		* arrays_copy_nominal['Electron_ID_Weight_DOWN'] * arrays_copy_nominal['Electron_RECO_Weight'] * lumi * arrays_copy_nominal['xsec'] * 1000 * arrays_copy_nominal['Generator_weight_sgn'] / true_events
				arrays_copy_nominal['true_weight_ElectronRECOup_Rwt{i}'] 	= arrays_copy_nominal['puWeight'] 	 * arrays_copy_nominal['L1PreFiringWeight_Nom']	* arrays_copy_nominal['Muon_ID_Weight'] 	* arrays_copy_nominal['Photon_ID_Weight'] 		* arrays_copy_nominal['Electron_ID_Weight'] * arrays_copy_nominal['Electron_RECO_Weight_UP'] * lumi * arrays_copy_nominal['xsec'] * 1000 * arrays_copy_nominal['Generator_weight_sgn'] / true_events
				arrays_copy_nominal['true_weight_ElectronRECOdown_Rwt{i}'] 	= arrays_copy_nominal['puWeight'] 	 * arrays_copy_nominal['L1PreFiringWeight_Nom']	* arrays_copy_nominal['Muon_ID_Weight'] 	* arrays_copy_nominal['Photon_ID_Weight'] 		* arrays_copy_nominal['Electron_ID_Weight'] * arrays_copy_nominal['Electron_RECO_Weight_DOWN'] * lumi * arrays_copy_nominal['xsec'] * 1000 * arrays_copy_nominal['Generator_weight_sgn'] / true_events
				arrays_copy_nominal['true_weight_l1up_Rwt{i}'] 				= arrays_copy_nominal['puWeight']    * arrays_copy_nominal['L1PreFiringWeight_Up']	* arrays_copy_nominal['Muon_ID_Weight'] 	* arrays_copy_nominal['Photon_ID_Weight'] 		* arrays_copy_nominal['Electron_ID_Weight'] * arrays_copy_nominal['Electron_RECO_Weight'] * lumi * arrays_copy_nominal['xsec'] * 1000 * arrays_copy_nominal['Generator_weight_sgn'] / true_events
				arrays_copy_nominal['true_weight_l1down_Rwt{i}'] 			= arrays_copy_nominal['puWeight']	 * arrays_copy_nominal['L1PreFiringWeight_Dn']	* arrays_copy_nominal['Muon_ID_Weight'] 	* arrays_copy_nominal['Photon_ID_Weight'] 		* arrays_copy_nominal['Electron_ID_Weight'] * arrays_copy_nominal['Electron_RECO_Weight'] * lumi * arrays_copy_nominal['xsec'] * 1000 * arrays_copy_nominal['Generator_weight_sgn'] / true_events
				arrays_copy_nominal['true_weight_puup_Rwt{i}'] 				= arrays_copy_nominal['puWeightUp']  * arrays_copy_nominal['L1PreFiringWeight_Nom']	* arrays_copy_nominal['Muon_ID_Weight'] 	* arrays_copy_nominal['Photon_ID_Weight'] 		* arrays_copy_nominal['Electron_ID_Weight'] * arrays_copy_nominal['Electron_RECO_Weight'] * lumi * arrays_copy_nominal['xsec'] * 1000 * arrays_copy_nominal['Generator_weight_sgn'] / true_events
				arrays_copy_nominal['true_weight_pudown_Rwt{i}'] 			= arrays_copy_nominal['puWeightDown']* arrays_copy_nominal['L1PreFiringWeight_Nom']	* arrays_copy_nominal['Muon_ID_Weight'] 	* arrays_copy_nominal['Photon_ID_Weight'] 		* arrays_copy_nominal['Electron_ID_Weight'] * arrays_copy_nominal['Electron_RECO_Weight'] * lumi * arrays_copy_nominal['xsec'] * 1000 * arrays_copy_nominal['Generator_weight_sgn'] / true_events
				
				
				
				for branch_name in branch:

					# >> Add this k to only fill WZG mllla
					if branch_name != "WZG_mllla":
						continue
					# <<<			

					# Fill it!
					for j in trange(0, len(arrays_copy_nominal[branch[branch_name]["name"]]), desc=f'fill {branch[branch_name]["name"]} for {file} in {UpDown_map[0]}_Rwt{i}'):
						hist[branch_name+f"_PhotonIDup_Rwt{i}"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]][j]), float(arrays_copy_nominal['true_weight_PhotonIDup_Rwt{i}'][j]))
						hist[branch_name+f"_PhotonIDdown_Rwt{i}"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]][j]), float(arrays_copy_nominal['true_weight_PhotonIDdown_Rwt{i}'][j]))
						hist[branch_name+f"_MuonIDup_Rwt{i}"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]][j]), float(arrays_copy_nominal['true_weight_MuonIDup_Rwt{i}'][j]))
						hist[branch_name+f"_MuonIDdown_Rwt{i}"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]][j]), float(arrays_copy_nominal['true_weight_MuonIDdown_Rwt{i}'][j]))
						hist[branch_name+f"_ElectronIDup_Rwt{i}"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]][j]), float(arrays_copy_nominal['true_weight_ElectronIDup_Rwt{i}'][j]))
						hist[branch_name+f"_ElectronIDdown_Rwt{i}"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]][j]), float(arrays_copy_nominal['true_weight_ElectronIDdown_Rwt{i}'][j]))
						hist[branch_name+f"_ElectronRECOup_Rwt{i}"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]][j]), float(arrays_copy_nominal['true_weight_ElectronRECOup_Rwt{i}'][j]))
						hist[branch_name+f"_ElectronRECOdown_Rwt{i}"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]][j]), float(arrays_copy_nominal['true_weight_ElectronRECOdown_Rwt{i}'][j]))
						hist[branch_name+f"_l1up_Rwt{i}"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]][j]), float(arrays_copy_nominal['true_weight_l1up_Rwt{i}'][j]))
						hist[branch_name+f"_l1down_Rwt{i}"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]][j]), float(arrays_copy_nominal['true_weight_l1down_Rwt{i}'][j]))
						hist[branch_name+f"_puup_Rwt{i}"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]][j]), float(arrays_copy_nominal['true_weight_puup_Rwt{i}'][j]))
						hist[branch_name+f"_pudown_Rwt{i}"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]][j]), float(arrays_copy_nominal['true_weight_pudown_Rwt{i}'][j]))
				print("\n")
	
				## --- 3. Fill JES JER up down


				# Applying different MET cut 
				for UpDown in range(1,5):
					print(f"Filling JES {str(UpDown_map[UpDown])}:")
					if channel in [0,1,2,3,4, 10,11,12,13,14, 20,21,22,23,24, 30,31,32]:
						MET_cut = (arrays[f'MET_T1Smear_pt_{UpDown_map[UpDown]}'] > 30)
						arrays_copy = ak.copy(arrays[MET_cut])
					elif channel in [5,6,7,8,9]:
						MET_cut = (arrays[f'MET_T1Smear_pt_{UpDown_map[UpDown]}'] <= 30)
						arrays_copy = ak.copy(arrays[MET_cut])
					else:
						arrays_copy = ak.copy(arrays)
					
					for branch_name in branch:

						# >> Add this k to only fill WZG mllla
						if branch_name != "WZG_mllla":
							continue
						# <<<		

						# Fill it!
						for j in trange(0, len(arrays_copy[branch[branch_name]["name"]]), desc=f'fill {branch[branch_name]["name"]} for {file} in {UpDown_map[UpDown]}_Rwt{i}'):
							#print("Final check: ",arrays_copy[branch[branch_name]["name"]][j], arrays_copy[f'true_weight_Rwt{i}'][j])
							hist[branch_name+f"_{UpDown_map[UpDown]}_Rwt{i}"].Fill(float(arrays_copy[branch[branch_name]["name"]][j]), float(arrays_copy[f'true_weight_Rwt{i}'][j]))
						# print (f"SumOfWeights for {branch_name}: ", hist[branch_name+f"_{UpDown_map[UpDown]}"].GetSumOfWeights())
					print("\n")




		#------------->  Non-Reweight
		else:



			## --- 1. Fill nominal
			print("Filling nominal:")
			arrays['true_weight'] = arrays['puWeight'] * arrays['Muon_ID_Weight'] * arrays['Electron_ID_Weight'] * arrays['Electron_RECO_Weight'] *  arrays["Photon_ID_Weight"] * arrays['L1PreFiringWeight_Nom'] * lumi * xsec * 1000 * arrays['Generator_weight_sgn'] / true_events

			if channel in [0,1,2,3,4, 10,11,12,13,14, 20,21,22,23,24, 30,31,32]:
				MET_cut = (arrays[f'MET_T1Smear_pt'] > 30)
				arrays_copy_nominal = ak.copy(arrays[MET_cut])
			elif channel in [5,6,7,8,9]:
				MET_cut = (arrays[f'MET_T1Smear_pt'] <= 30)
				arrays_copy_nominal = ak.copy(arrays[MET_cut])
			else:
				arrays_copy_nominal = ak.copy(arrays)

			for branch_name in branch:

				if branch_name != "WZG_mllla":
					continue

				for i in trange(0, len(arrays_copy_nominal[branch[branch_name]["name"]]), desc=f'fill {branch[branch_name]["name"]} for {file} in {UpDown_map[0]}'):
					hist[branch_name+f"_{UpDown_map[0]}"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]][i]), float(arrays_copy_nominal['true_weight'][i]))
			
			

			## --- 2.Fill lep ID RECO up down	
			print("Filling up down:")
			arrays_copy_nominal['true_weight_PhotonIDup'] 		= arrays_copy_nominal['puWeight'] 		* arrays_copy_nominal['L1PreFiringWeight_Nom'] *  arrays_copy_nominal['Photon_ID_Weight_UP']   * arrays_copy_nominal['Muon_ID_Weight'] * arrays_copy_nominal['Electron_ID_Weight'] * arrays_copy_nominal['Electron_RECO_Weight'] * lumi * xsec * 1000 * arrays_copy_nominal['Generator_weight_sgn'] / true_events
			arrays_copy_nominal['true_weight_PhotonIDdown'] 	= arrays_copy_nominal['puWeight'] 		* arrays_copy_nominal['L1PreFiringWeight_Nom'] *  arrays_copy_nominal['Photon_ID_Weight_DOWN'] * arrays_copy_nominal['Muon_ID_Weight'] * arrays_copy_nominal['Electron_ID_Weight'] * arrays_copy_nominal['Electron_RECO_Weight'] * lumi * xsec * 1000 * arrays_copy_nominal['Generator_weight_sgn'] / true_events
			arrays_copy_nominal['true_weight_MuonIDup'] 		= arrays_copy_nominal['puWeight'] 		* arrays_copy_nominal['L1PreFiringWeight_Nom'] *  arrays_copy_nominal['Photon_ID_Weight'] 	   * arrays_copy_nominal['Muon_ID_Weight_UP'] * arrays_copy_nominal['Electron_ID_Weight'] * arrays_copy_nominal['Electron_RECO_Weight'] * lumi * xsec * 1000 * arrays_copy_nominal['Generator_weight_sgn'] / true_events
			arrays_copy_nominal['true_weight_MuonIDdown'] 		= arrays_copy_nominal['puWeight'] 		* arrays_copy_nominal['L1PreFiringWeight_Nom'] *  arrays_copy_nominal['Photon_ID_Weight'] 	   * arrays_copy_nominal['Muon_ID_Weight_DOWN'] * arrays_copy_nominal['Electron_ID_Weight'] * arrays_copy_nominal['Electron_RECO_Weight'] * lumi * xsec * 1000 * arrays_copy_nominal['Generator_weight_sgn'] / true_events
			arrays_copy_nominal['true_weight_ElectronIDup'] 	= arrays_copy_nominal['puWeight'] 		* arrays_copy_nominal['L1PreFiringWeight_Nom'] *  arrays_copy_nominal['Photon_ID_Weight'] 	   * arrays_copy_nominal['Muon_ID_Weight'] * arrays_copy_nominal['Electron_ID_Weight_UP'] * arrays_copy_nominal['Electron_RECO_Weight'] * lumi * xsec * 1000 * arrays_copy_nominal['Generator_weight_sgn'] / true_events
			arrays_copy_nominal['true_weight_ElectronIDdown'] 	= arrays_copy_nominal['puWeight'] 		* arrays_copy_nominal['L1PreFiringWeight_Nom'] *  arrays_copy_nominal['Photon_ID_Weight'] 	   * arrays_copy_nominal['Muon_ID_Weight'] * arrays_copy_nominal['Electron_ID_Weight_DOWN'] * arrays_copy_nominal['Electron_RECO_Weight'] * lumi * xsec * 1000 * arrays_copy_nominal['Generator_weight_sgn'] / true_events
			arrays_copy_nominal['true_weight_ElectronRECOup'] 	= arrays_copy_nominal['puWeight'] 		* arrays_copy_nominal['L1PreFiringWeight_Nom'] *  arrays_copy_nominal['Photon_ID_Weight'] 	   * arrays_copy_nominal['Muon_ID_Weight'] * arrays_copy_nominal['Electron_ID_Weight'] * arrays_copy_nominal['Electron_RECO_Weight_UP'] * lumi * xsec * 1000 * arrays_copy_nominal['Generator_weight_sgn'] / true_events
			arrays_copy_nominal['true_weight_ElectronRECOdown'] = arrays_copy_nominal['puWeight'] 		* arrays_copy_nominal['L1PreFiringWeight_Nom'] *  arrays_copy_nominal['Photon_ID_Weight'] 	   * arrays_copy_nominal['Muon_ID_Weight'] * arrays_copy_nominal['Electron_ID_Weight'] * arrays_copy_nominal['Electron_RECO_Weight_DOWN'] * lumi * xsec * 1000 * arrays_copy_nominal['Generator_weight_sgn'] / true_events
			arrays_copy_nominal['true_weight_l1up'] 			= arrays_copy_nominal['puWeight']    	* arrays_copy_nominal['L1PreFiringWeight_Up']  * arrays_copy_nominal['Muon_ID_Weight'] 		   * arrays_copy_nominal['Photon_ID_Weight'] * arrays_copy_nominal['Electron_ID_Weight'] * arrays_copy_nominal['Electron_RECO_Weight'] * lumi * xsec * 1000 * arrays_copy_nominal['Generator_weight_sgn'] / true_events
			arrays_copy_nominal['true_weight_l1down'] 			= arrays_copy_nominal['puWeight']	 	* arrays_copy_nominal['L1PreFiringWeight_Dn']  * arrays_copy_nominal['Muon_ID_Weight'] 		   * arrays_copy_nominal['Photon_ID_Weight'] * arrays_copy_nominal['Electron_ID_Weight'] * arrays_copy_nominal['Electron_RECO_Weight'] * lumi * xsec * 1000 * arrays_copy_nominal['Generator_weight_sgn'] / true_events
			arrays_copy_nominal['true_weight_puup'] 			= arrays_copy_nominal['puWeightUp'] 	* arrays_copy_nominal['L1PreFiringWeight_Nom'] *  arrays_copy_nominal['Photon_ID_Weight'] 	   * arrays_copy_nominal['Muon_ID_Weight'] * arrays_copy_nominal['Electron_ID_Weight'] * arrays_copy_nominal['Electron_RECO_Weight'] * lumi * xsec * 1000 * arrays_copy_nominal['Generator_weight_sgn'] / true_events
			arrays_copy_nominal['true_weight_pudown'] 			= arrays_copy_nominal['puWeightDown'] 	* arrays_copy_nominal['L1PreFiringWeight_Nom'] *  arrays_copy_nominal['Photon_ID_Weight'] 	   * arrays_copy_nominal['Muon_ID_Weight'] * arrays_copy_nominal['Electron_ID_Weight'] * arrays_copy_nominal['Electron_RECO_Weight'] * lumi * xsec * 1000 * arrays_copy_nominal['Generator_weight_sgn'] / true_events

			for branch_name in branch:

				if branch_name != "WZG_mllla":
					continue

				for i in trange(0, len(arrays_copy_nominal[branch[branch_name]["name"]]), desc=f'fill {branch[branch_name]["name"]} for {file} in {UpDown_map[0]}'):
					hist[branch_name+f"_PhotonIDup"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]][i]), float(arrays_copy_nominal['true_weight_PhotonIDup'][i]))
					hist[branch_name+f"_PhotonIDdown"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]][i]), float(arrays_copy_nominal['true_weight_PhotonIDdown'][i]))
					hist[branch_name+f"_MuonIDup"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]][i]), float(arrays_copy_nominal['true_weight_MuonIDup'][i]))
					hist[branch_name+f"_MuonIDdown"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]][i]), float(arrays_copy_nominal['true_weight_MuonIDdown'][i]))
					hist[branch_name+f"_ElectronIDup"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]][i]), float(arrays_copy_nominal['true_weight_ElectronIDup'][i]))
					hist[branch_name+f"_ElectronIDdown"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]][i]), float(arrays_copy_nominal['true_weight_ElectronIDdown'][i]))
					hist[branch_name+f"_ElectronRECOup"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]][i]), float(arrays_copy_nominal['true_weight_ElectronRECOup'][i]))
					hist[branch_name+f"_ElectronRECOdown"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]][i]), float(arrays_copy_nominal['true_weight_ElectronRECOdown'][i]))
					hist[branch_name+f"_l1up"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]][i]), float(arrays_copy_nominal['true_weight_l1up'][i]))
					hist[branch_name+f"_l1down"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]][i]), float(arrays_copy_nominal['true_weight_l1down'][i]))
					hist[branch_name+f"_puup"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]][i]), float(arrays_copy_nominal['true_weight_puup'][i]))
					hist[branch_name+f"_pudown"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]][i]), float(arrays_copy_nominal['true_weight_pudown'][i]))
			print("\n")
	
			#Fill JES JER up down
			for UpDown in range(1,5):
				print(f"Filling JES {str(UpDown_map[UpDown])}:")
				if channel in [0,1,2,3,4, 10,11,12,13,14, 20,21,22,23,24, 30,31,32]:
					MET_cut = (arrays[:,f'MET_T1Smear_pt_{UpDown_map[UpDown]}'] > 30)
					arrays_copy = ak.copy(arrays[MET_cut])
				elif channel in [5,6,7,8,9]:
					MET_cut = (arrays[:,f'MET_T1Smear_pt_{UpDown_map[UpDown]}'] <= 30)
					arrays_copy = ak.copy(arrays[MET_cut])
				else:
					arrays_copy = ak.copy(arrays)
			
				for branch_name in branch:
					# >> Add this k to only fill WZG mllla
					if branch_name != "WZG_mllla":
						continue
					# <<<			
					for i in trange(0, len(arrays_copy[branch[branch_name]["name"]]), desc=f'fill {branch[branch_name]["name"]} for {file} in {UpDown_map[UpDown]}'):
						hist[branch_name+f"_{UpDown_map[UpDown]}"].Fill(float(arrays_copy[branch[branch_name]["name"]][i]), float(arrays_copy['true_weight'][i]))
					# print (f"SumOfWeights for {branch_name}: ", hist[branch_name+f"_{UpDown_map[UpDown]}"].GetSumOfWeights())
				print("\n")

	end_time = time.time()
	print ('Time cost: %.2f\n' %(end_time-init_time))
	return True



def AddHist_FakeLepton(file, hist, isData, xsec, lumi, channel, branch):
	
	init_time = time.time()
	init_branches = ['fake_lepton_weight',\
					'fake_lepton_weight_up',\
					'fake_lepton_weight_down',\
					'fake_lepton_weight_sys_up',\
					'fake_lepton_weight_sys_down',\
					'channel_mark',\
					'region_mark',\
					'WZG_photon_pt',
					'WZG_lepton1_mass',
					'WZG_lepton2_mass',
					'WZG_lepton3_mass',
					'WZG_photon_mass',
					'mwa',
					'WZG_trileptonmass',
					'WZG_dileptonmass',
					'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',\
					'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL',\
					'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL',\
					'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL',\
					'HLT_Ele27_WPTight_Gsf',\
					'HLT_IsoTkMu24'
					]
	
	if isData:
		print('is Data')
		for branch_name in branch:

			# >>>added by Jiwoong
			if branch_name == "WZG_mllla":
				continue
			# <<<


			if branch[branch_name]["name"] not in init_branches:
				init_branches.append(branch[branch_name]["name"])
	else:
		print('is MC')
		add_branches = ['Generator_weight']
		gen_branches = uproot.open(file+':Events').keys(filter_name='*_lepton*genPartFlav')
		true_events = uproot.open(file)['nEventsGenWeighted'].values()[0]
		init_branches.extend(add_branches)
		init_branches.extend(gen_branches)
		for branch_name in branch:

			# >>>added by Jiwoong
			if branch_name == "WZG_mllla":
				continue
			# <<<


			if branch[branch_name]["name"] not in init_branches:
				init_branches.append(branch[branch_name]["name"])
		
	arrays = uproot.open(file+':Events').arrays(init_branches)
	arrays = HLT_cut(file, arrays)
	arrays = channel_cut(channel, arrays)

	# -----> aQGC photonPT cuts are added
	aQGC_photon_pt_cut = arrays['WZG_photon_pt'] > 60
	arrays = arrays[aQGC_photon_pt_cut]
	# <-----  -JiWoong-

	# >> Add lllA mass calculation
	lllA_vec = Make4Vec(arrays)
	arrays["WZG_mllla"] = lllA_vec.mass
	# <<--- Added my Jiwoong

	region_cut = arrays['region_mark'] == 2
	arrays = arrays[region_cut]
	
	if isData:
		if channel in [0,1,2,3,4, 10,11,12,13,14, 20,21,22,23,24, 30,31,32]:
			MET_cut = (arrays['MET'] > 30)
		elif channel in [5,6,7,8,9]:
			MET_cut = (arrays['MET'] <= 30)
		else:
			MET_cut = (arrays['MET'] >= 0)
		arrays = arrays[MET_cut]
		for branch_name in branch:




			if branch_name != "WZG_mllla":
				continue

			for i in trange(0, len(arrays[branch[branch_name]["name"]]), desc=f'fill {branch[branch_name]["name"]} for {file}'):
				hist[branch_name].Fill(float(arrays[branch[branch_name]["name"]][i]), float(arrays['fake_lepton_weight'][i]))
				hist[branch_name+f"_FakeLep_sys_up"].Fill(float(arrays[branch[branch_name]["name"]][i]), float(arrays['fake_lepton_weight_sys_up'][i]))
				hist[branch_name+f"_FakeLep_sys_down"].Fill(float(arrays[branch[branch_name]["name"]][i]), float(arrays['fake_lepton_weight_sys_down'][i]))
				hist[branch_name+f"_FakeLep_stat_up"].Fill(float(arrays[branch[branch_name]["name"]][i]), float(arrays['fake_lepton_weight_up'][i]))
				hist[branch_name+f"_FakeLep_stat_down"].Fill(float(arrays[branch[branch_name]["name"]][i]), float(arrays['fake_lepton_weight_down'][i]))
			print (f"SumOfWeights for {branch_name}: ", hist[branch_name].GetSumOfWeights())
	else:
		arrays = lep_gen_cut(channel, arrays)
		if channel in [0,1,2,3,4, 10,11,12,13,14, 20,21,22,23,24, 30,31,32]:
			MET_cut = (arrays['MET'] > 30)
		elif channel in [5,6,7,8,9]:
			MET_cut = (arrays['MET'] <= 30)
		else:
			MET_cut = (arrays['MET'] >= 0)
		arrays = arrays[MET_cut]
	
		arrays['Generator_weight_sgn'] = ak.where(arrays['Generator_weight'] >=0,1,-1)
		arrays['true_weight'] = lumi * xsec * 1000 * arrays['Generator_weight_sgn'] / true_events

		for branch_name in branch:

			# >> Add this block to only fill WZG mllla
			if branch_name != "WZG_mllla":
				continue
			# <<<			

			for i in trange(0, len(arrays[branch[branch_name]["name"]]), desc=f'fill {branch[branch_name]["name"]} for {file}'):
				hist[branch_name].Fill(float(arrays[branch[branch_name]["name"]][i]), -1 * float(arrays['fake_lepton_weight'][i]) * float(arrays['true_weight'][i]))
				hist[branch_name+f"_FakeLep_sys_up"].Fill(float(arrays[branch[branch_name]["name"]][i]), -1 * float(arrays['fake_lepton_weight_sys_up'][i]) * float(arrays['true_weight'][i]))
				hist[branch_name+f"_FakeLep_sys_down"].Fill(float(arrays[branch[branch_name]["name"]][i]), -1 * float(arrays['fake_lepton_weight_sys_down'][i]) * float(arrays['true_weight'][i]))
				hist[branch_name+f"_FakeLep_stat_up"].Fill(float(arrays[branch[branch_name]["name"]][i]), -1 * float(arrays['fake_lepton_weight_up'][i]) * float(arrays['true_weight'][i]))
				hist[branch_name+f"_FakeLep_stat_down"].Fill(float(arrays[branch[branch_name]["name"]][i]), -1 * float(arrays['fake_lepton_weight_down'][i]) * float(arrays['true_weight'][i]))
			print (f"SumOfWeights for {branch_name}: ", hist[branch_name].GetSumOfWeights())
	
	end_time = time.time()
	print ('Time cost: %.2f\n' %(end_time-init_time))




def AddHist_FakePhoton(file, hist, isData, xsec, lumi, channel, branch):
	
	init_time = time.time()
	init_branches = ['fake_photon_weight','channel_mark',\
					'region_mark',\
					'WZG_photon_genPartFlav','WZG_photon_pt','WZG_photon_eta','WZG_photon_pfRelIso03_chg','WZG_photon_sieie',\
					'ttG_photon_genPartFlav','ttG_photon_pt','ttG_photon_eta','ttG_photon_pfRelIso03_chg','ttG_photon_sieie',\
					'ZGJ_photon_genPartFlav','ZGJ_photon_pt','ZGJ_photon_eta','ZGJ_photon_pfRelIso03_chg','ZGJ_photon_sieie',\
					'WZG_lepton1_mass',
					'WZG_lepton2_mass',
					'WZG_lepton3_mass',
					'WZG_photon_mass',
					'mwa',
					'WZG_trileptonmass',
					'WZG_dileptonmass',
					'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',\
					'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL',\
					'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL',\
					'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL',\
					'HLT_Ele27_WPTight_Gsf',\
					'HLT_IsoTkMu24']

	
	if isData:
		print('is Data')
		for branch_name in branch:

			# >>>added by Jiwoong
			if branch_name == "WZG_mllla":
				continue
			# <<<

			if branch[branch_name]["name"] not in init_branches:
				init_branches.append(branch[branch_name]["name"])
	else:
		print('is MC')
		add_branches = ['Generator_weight']
		gen_branches = uproot.open(file+':Events').keys(filter_name='*_lepton*genPartFlav')
		true_events = uproot.open(file)['nEventsGenWeighted'].values()[0]
		init_branches.extend(add_branches)
		init_branches.extend(gen_branches)
		for branch_name in branch:

			# >>>added by Jiwoong
			if branch_name == "WZG_mllla":
				continue
			# <<<

			if branch[branch_name]["name"] not in init_branches:
				init_branches.append(branch[branch_name]["name"])

	arrays = uproot.open(file+':Events').arrays(init_branches)
	arrays = HLT_cut(file, arrays)
	arrays = channel_cut(channel, arrays)

	# -----> aQGC photonPT cuts are added
	aQGC_photon_pt_cut = arrays['WZG_photon_pt'] > 60
	arrays = arrays[aQGC_photon_pt_cut]
	# <-----  -JiWoong-

	# >> Add lllA mass calculation
	lllA_vec = Make4Vec(arrays)
	arrays["WZG_mllla"] = lllA_vec.mass
	# <<--- Added my Jiwoong

	region_cut = arrays['region_mark'] == 3
	arrays 	   = arrays[region_cut]
	
	
	if ((channel >= 0) and (channel <=4)):
		chg_cut = ((arrays["WZG_photon_pfRelIso03_chg"]*arrays["WZG_photon_pt"]) > 4) &  ((arrays["WZG_photon_pfRelIso03_chg"]*arrays["WZG_photon_pt"]) < 10)
		sieie_cut = ((arrays['WZG_photon_sieie'] > 0.01015) & (arrays['WZG_photon_sieie'] < 0.05030) & (arrays['WZG_photon_eta'] < 1.4442)) | ((arrays['WZG_photon_sieie'] > 0.0272) & (arrays['WZG_photon_sieie'] < 0.1360) & (arrays['WZG_photon_eta'] > 1.566))

	elif ((channel >= 20) and (channel <=24)):
		chg_cut = ((arrays["ttG_photon_pfRelIso03_chg"]*arrays["ttG_photon_pt"]) > 4) & ((arrays["ttG_photon_pfRelIso03_chg"]*arrays["ttG_photon_pt"]) < 10)
		sieie_cut = ((arrays['ttG_photon_sieie'] > 0.01015) & (arrays['ttG_photon_sieie'] < 0.05030) & (arrays['ttG_photon_eta'] < 1.4442)) | ((arrays['ttG_photon_sieie'] > 0.0272) & (arrays['ttG_photon_sieie'] < 0.1360) & (arrays['ttG_photon_eta'] > 1.566))

	elif ((channel >= 30) and (channel <=32)):
		chg_cut = ((arrays["ZGJ_photon_pfRelIso03_chg"]*arrays["ZGJ_photon_pt"]) > 4) & ((arrays["ZGJ_photon_pfRelIso03_chg"]*arrays["ZGJ_photon_pt"]) < 10)
		sieie_cut = ((arrays['ZGJ_photon_sieie'] > 0.01015) & (arrays['ZGJ_photon_sieie'] < 0.05030) & (arrays['ZGJ_photon_eta'] < 1.4442)) | ((arrays['ZGJ_photon_sieie'] > 0.0272) & (arrays['ZGJ_photon_sieie'] < 0.1360) & (arrays['ZGJ_photon_eta'] > 1.566))


	if isData:
		if channel in [0,1,2,3,4, 10,11,12,13,14, 20,21,22,23,24, 30,31,32]:
			MET_cut = (arrays['MET'] > 30)
		elif channel in [5,6,7,8,9]:
			MET_cut = (arrays['MET'] <= 30)
		else:
			MET_cut = (arrays['MET'] >= 0)
		arrays = arrays[sieie_cut&chg_cut&MET_cut]

		for branch_name in branch:

			# >> Add this block to only fill WZG mllla
			if branch_name != "WZG_mllla":
				continue
			# <<<			

			for i in trange(0, len(arrays[branch[branch_name]["name"]]), desc=f'fill {branch[branch_name]["name"]} for {file}'):
				hist[branch_name].Fill(float(arrays[branch[branch_name]["name"]][i]), float(arrays['fake_photon_weight'][i]))
			print (f"SumOfWeights for {branch_name}: ", hist[branch_name].GetSumOfWeights())

	else:
		if channel in [0,1,2,3,4, 10,11,12,13,14, 20,21,22,23,24, 30,31,32]:
			MET_cut = (arrays['MET'] > 30)
		elif channel in [5,6,7,8,9]:
			MET_cut = (arrays['MET'] <= 30)
		else:
			MET_cut = (arrays['MET'] >= 0)
		arrays = arrays[sieie_cut&chg_cut & MET_cut]
		arrays = lep_gen_cut(channel, arrays)
		arrays = pho_gen_cut(channel, arrays)
	
		arrays['Generator_weight_sgn'] = ak.where(arrays['Generator_weight'] >=0,1,-1)
		arrays['true_weight'] = lumi * xsec * 1000 * arrays['Generator_weight_sgn'] / true_events
		for branch_name in branch:

			# >> Add this block to only fill WZG mllla
			if branch_name != "WZG_mllla":
				continue
			# <<<			

			for i in trange(0, len(arrays[branch[branch_name]["name"]]), desc=f'fill {branch[branch_name]["name"]} for {file}'):
				hist[branch_name].Fill(float(arrays[branch[branch_name]["name"]][i]), -1 * float(arrays['fake_photon_weight'][i]) * float(arrays['true_weight'][i]))
			print (f"SumOfWeights for {branch_name}: ", hist[branch_name].GetSumOfWeights())
	
	end_time = time.time()
	print ('Time cost: %.2f\n' %(end_time-init_time))








def SetHistStyle(hist, color):
	if color != 1:
		hist.SetFillColor(color)
		hist.SetLineColor(0)
		hist.SetLineWidth(0)
	else:
		hist.SetLineWidth(2)
		hist.SetLineColor(1)
	hist.SetMarkerStyle(20)
	hist.SetMarkerColor(1)
	hist.SetYTitle('events/bin')
	hist.SetStats(0)
	# hist.Sumw2()

	#hist.GetXaxis().SetRangeUser(300,600)
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
	hist.GetXaxis().SetTitleFont(43)
	hist.GetXaxis().SetTitleOffset(3.3)
	hist.GetXaxis().SetLabelFont(43)
	hist.GetXaxis().SetLabelSize(38)
	hist.GetXaxis().SetLabelOffset(0.015)
