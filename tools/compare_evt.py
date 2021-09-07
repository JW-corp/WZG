import glob
import numpy as np
import pandas as pd

Egamma	   = 'data_after_trigger/Egamm*.npy'
DoubleMuon = 'data_after_trigger/DoubleMuon*.npy'
SingleMuon = 'data_after_trigger/SingleMuon*.npy'
MuonEG	   = 'data_after_trigger/MuonEG*.npy'


DoubleMuon_list = glob.glob(DoubleMuon)
SingleMuon_list = glob.glob(SingleMuon)
MuonEG_list		= glob.glob(MuonEG)
Egamma_list		= glob.glob(Egamma)


print("--> Single Muon ")
SingleMuon_arr = []
SingleMuon_run_arr = []
SingleMuon_lumi_arr = []

for f in SingleMuon_list:
	tree = np.load(f,allow_pickle=True)[()]
	SingleMuon_arr += tree['event']
	SingleMuon_run_arr += tree['run']
	SingleMuon_lumi_arr += tree['lumiblock']
	print(len(tree['event']),len(tree['run']),len(tree['lumiblock']))

print("--> Double Muon ")
DoubleMuon_arr = []
DoubleMuon_run_arr = []
DoubleMuon_lumi_arr = []
for f in DoubleMuon_list:
	tree = np.load(f,allow_pickle=True)[()]
	DoubleMuon_arr += tree['event']
	DoubleMuon_run_arr += tree['run']
	DoubleMuon_lumi_arr += tree['lumiblock']
	print(len(tree['event']),len(tree['run']),len(tree['lumiblock']))

print("--> Egamma ")
Egamma_arr = []
Egamma_run_arr = []
Egamma_lumi_arr = []
for f in Egamma_list:
	tree = np.load(f,allow_pickle=True)[()]
	Egamma_arr += tree['event']
	Egamma_run_arr += tree['run']
	Egamma_lumi_arr += tree['lumiblock']
	print(len(tree['event']),len(tree['run']),len(tree['lumiblock']))

print("--> MuonEG ")
MuonEG_arr = []
MuonEG_run_arr = []
MuonEG_lumi_arr = []
for f in MuonEG_list:
	tree = np.load(f,allow_pickle=True)[()]
	MuonEG_arr += tree['event']
	MuonEG_run_arr += tree['run']
	MuonEG_lumi_arr += tree['lumiblock']
	print(len(tree['event']),len(tree['run']),len(tree['lumiblock']))

print("DoubleMu: ",len(DoubleMuon_arr),len(DoubleMuon_run_arr),len(DoubleMuon_lumi_arr))
print("SingleMu: ",len(SingleMuon_arr),len(SingleMuon_run_arr),len(SingleMuon_lumi_arr))
print("Egamma: ",len(Egamma_arr),len(Egamma_run_arr),len(Egamma_lumi_arr))
print("MuonEG: ",len(MuonEG_arr),len(MuonEG_run_arr),len(MuonEG_lumi_arr))


#@numba.njit
def show_duplicate(arr_evtnum1,arr_evtnum2,arr_run1,arr_run2,arr_lumi1,arr_lumi2):

	evt_arr  = np.concatenate([arr_evtnum1,arr_evtnum2])
	run_arr  = np.concatenate([arr_run1,arr_run2])
	lumi_arr = np.concatenate([arr_lumi1,arr_lumi2])

	evt_df = pd.Series(evt_arr)
	run_df = pd.Series(run_arr)
	lumi_df = pd.Series(lumi_arr)

	
	evt_dup_mask  = evt_df.duplicated(keep=False)
	
	evt_df  = evt_df[evt_dup_mask]
	run_df  = run_df[evt_dup_mask]
	lumi_df = lumi_df[evt_dup_mask]
	
	run_dup_mask = run_df.duplicated(keep=False)
	
	evt_df  = evt_df[run_dup_mask]
	run_df  = run_df[run_dup_mask]
	lumi_df = lumi_df[run_dup_mask]
	
	lumi_dup_mask = lumi_df.duplicated(keep=False)

	evt_df  = evt_df[lumi_dup_mask]
	run_df  = run_df[lumi_dup_mask]
	lumi_df = lumi_df[lumi_dup_mask]


	return evt_df.values, run_df.values, lumi_df.values

	



DM_SM,_,_ = show_duplicate(DoubleMuon_arr,SingleMuon_arr,DoubleMuon_run_arr,SingleMuon_run_arr,DoubleMuon_lumi_arr,SingleMuon_lumi_arr)
print("DM_SM",len(set(DM_SM)))

DM_MEG,_,_  = show_duplicate(DoubleMuon_arr,MuonEG_arr,DoubleMuon_run_arr,MuonEG_run_arr,DoubleMuon_lumi_arr,MuonEG_lumi_arr)
print("DM_MEG",len(set(DM_MEG)))

SM_MEG,_,_ = show_duplicate(SingleMuon_arr,MuonEG_arr,SingleMuon_run_arr,MuonEG_run_arr,SingleMuon_lumi_arr,MuonEG_lumi_arr)
print("SM_MEG",len(set(SM_MEG)))

EG_DM,_,_  = show_duplicate(Egamma_arr,DoubleMuon_arr,Egamma_run_arr,DoubleMuon_run_arr,Egamma_lumi_arr,DoubleMuon_lumi_arr)
print("EG_DM",len(set(EG_DM)))

EG_SM,_,_  = show_duplicate(Egamma_arr,SingleMuon_arr,Egamma_run_arr,SingleMuon_run_arr,Egamma_lumi_arr,SingleMuon_lumi_arr)
print("EG_SM",len(set(EG_SM)))

EG_MEG,_,_ = show_duplicate(Egamma_arr,MuonEG_arr,Egamma_run_arr,MuonEG_run_arr,Egamma_lumi_arr,MuonEG_lumi_arr)
print("EG_MEG",len(set(EG_MEG)))


#np.save("DM_SM.npy",DM_SM)
#np.save("DM_MEG.npy",DM_MEG)
#np.save("SM_MEG.npy",SM_MEG)
#np.save("EG_DM.npy",EG_DM)
#np.save("EG_SM.npy",EG_SM)
#np.save("EG_MEG.npy",EG_MEG)
