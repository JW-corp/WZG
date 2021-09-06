import awkward as ak
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import numpy as np
import matplotlib.pyplot as plt
import glob
from tqdm import tqdm
import argparse




def pass_triggers(infile,sample_name,year):
	
	#print(infile)
	events = NanoEventsFactory.from_root(infile, schemaclass=NanoAODSchema).events()
	
	
	triggers = {
		'Egamma':{
		"2018":["Ele23_Ele12_CaloIdL_TrackIdL_IsoVL","Ele32_WPTight_Gsf"]
		},
		'SingleMuon':{
		"2018":["IsoMu24"]
		},
		'DoubleMuon':{
		"2018":["Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8"]
		},
		'MuonEG':{
		"2018":["Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ","Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL"]
		},
	}
	
	triggers_mask = np.ones(len(events),dtype=np.bool)

	# --Trigger-mask for SingleMuon
	if sample_name == 'SingleMuon':
		triggers_mask = triggers_mask & events.HLT[triggers['SingleMuon'][year][0]]

	# --Trigger-mask for DoubleMuon
	elif sample_name == 'DoubleMuon':
		triggers_mask = triggers_mask & (~events.HLT[triggers['SingleMuon'][year][0]])\
						& events.HLT[triggers['DoubleMuon'][year][0]]

	# --Trigger-maks for Egamma
	elif sample_name == 'Egamma':
		triggers_mask = triggers_mask & (~events.HLT[triggers['SingleMuon'][year][0]])\
						& (~events.HLT[triggers['DoubleMuon'][year][0]])\
						& (events.HLT[triggers['Egamma'][year][0]] | events.HLT[triggers['Egamma'][year][1]])
			
	# --Trigger-maks for MuonEG
	elif sample_name == 'MuonEG':
		triggers_mask = triggers_mask & (~events.HLT[triggers['SingleMuon'][year][0]])\
						& (events.HLT[triggers['Egamma'][year][0]] | events.HLT[triggers['Egamma'][year][1]])\
						& (events.HLT[triggers['MuonEG'][year][0]] | events.HLT[triggers['MuonEG'][year][1]])
	
	events = events[triggers_mask]

	'''
	Electron = events.Electron
	EleSelmask = (
		(Electron.pt >= 10)
		& (np.abs(Electron.eta + Electron.deltaEtaSC) < 1.479)
		& (Electron.cutBased > 2)
		& (abs(Electron.dxy) < 0.05)
		& (abs(Electron.dz) < 0.1)
	) | (
		(Electron.pt >= 10)
		& (np.abs(Electron.eta + Electron.deltaEtaSC) > 1.479)
		& (np.abs(Electron.eta + Electron.deltaEtaSC) <= 2.5)
		& (Electron.cutBased > 2)
		& (abs(Electron.dxy) < 0.1)
		& (abs(Electron.dz) < 0.2)
	)


	Electron = Electron[EleSelmask]
	
	# Apply flow2
	Tri_electron_mask = ak.num(Electron) == 3
	events = events[Tri_electron_mask]
	'''

	return ak.to_numpy(events.event)


def Loop(flist,sample_name,year):
	evt_arr=[]
	for f in tqdm(flist):
		evt_arr		+= list(set(pass_triggers(f,sample_name,year)))
		evt_arr		 = list(set(evt_arr))
	

	return evt_arr

if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument(nargs='+' ,help='input files', dest='flist')
	parser.add_argument('--outname', '-o', help='outname')
	args  =parser.parse_args()
	
	year = '2018'
	sample_name = args.outname.split('_')[0]
	flist = args.flist
	evt_number_arr = Loop(flist,sample_name,year)

	np.save(args.outname,evt_number_arr)



