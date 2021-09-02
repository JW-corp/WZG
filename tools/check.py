import awkward as ak
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import numpy as np
import matplotlib.pyplot as plt
import glob
from tqdm import tqdm
import argparse




def pass_triggers(infile,sample_name):
	events = NanoEventsFactory.from_root(infile, schemaclass=NanoAODSchema).events()
	
	
	triggers = {
		'Egamma':{
		"2018":["Ele23_Ele12_CaloIdL_TrackIdL_IsoVL","Ele32_WPTight_Gsf"]
		},
		'DoubleMuon':{
		"2018":["IsoMu24"]
		},
		'MuonEG':{
		"2018":["Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8"]
		},
		'SingleMuon':{
		"2018":["Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ","Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL"]
		},
	}
	
	
	# double lepton trigger
	year='2018'
	do_trigger = True
	if not do_trigger:
		triggers_mask = np.ones(len(events), dtype=np.bool)
	else:
		triggers_mask = np.zeros(len(events), dtype=np.bool)
		for path in triggers[sample_name][year]:
			if path not in events.HLT.fields:
				continue
			triggers_mask = triggers_mask | events.HLT[path]
	
	
	events = events[triggers_mask]
	return ak.to_numpy(events.event)



def Loop(flist,sample_name):
	evt_arr=[]
	for f in tqdm(flist):
		evt_arr		+= list(set(pass_triggers(f,sample_name)))
		evt_arr		 = list(set(evt_arr))
	

	return evt_arr

if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument(nargs='+' ,help='input files', dest='flist')
	parser.add_argument('--outname', '-o', help='outname')
	args  =parser.parse_args()
	
	
	sample_name = args.outname.split('_')[0]
	flist = args.flist
	evt_number_arr = Loop(flist,sample_name)

	np.save(args.outname,evt_number_arr)


#evt_DoubleMuon  = pass_triggers(sample_dict,'DoubleMuon')
#evt_MuonEG		= pass_triggers(sample_dict,'MuonEG')
#evt_SingleMuon  = pass_triggers(sample_dict,'SingleMuon')

#print(evt_Egamma)
#print(evt_DoubleMuon)
#print(evt_MuonEG)
#print(evt_SingleMuon)
#
#a = np.concatenate([evt_Egamma,evt_DoubleMuon,evt_MuonEG,evt_SingleMuon])
#unq, unq_idx, unq_cnt = np.unique(a, return_inverse=True, return_counts=True)
#cnt_mask = unq_cnt > 1
#dup_ids = unq[cnt_mask]
#print("duplicated: ",dup_ids)


