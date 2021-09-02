import glob
import numpy as np
from tqdm import tqdm

Egamma	   = 'data_after_trigger/Egamm*.npy'
DoubleMuon = 'data_after_trigger/DoubleMuon*.npy'
SingleMuon = 'data_after_trigger/SingleMuon*.npy'
MuonEG	   = 'data_after_trigger/MuonEG*.npy'


DoubleMuon_list = glob.glob(DoubleMuon)
SingleMuon_list = glob.glob(SingleMuon)
MuonEG_list		= glob.glob(MuonEG)
Egamma_list		= glob.glob(Egamma)


DoubleMuon_arr = []
for f in tqdm(DoubleMuon_list):
	DoubleMuon_arr = np.concatenate([DoubleMuon_arr,np.load(f)[()]])
print(len(DoubleMuon_arr))

SingleMuon_arr = []
for f in tqdm(SingleMuon_list):
	SingleMuon_arr = np.concatenate([SingleMuon_arr,np.load(f)[()]])
print(len(SingleMuon_arr))

MuonEG_arr = []
for f in tqdm(MuonEG_list):
	MuonEG_arr = np.concatenate([MuonEG_arr,np.load(f)[()]])
print(len(MuonEG_arr))

Egamma_arr = []
for f in tqdm(Egamma_list):
	Egamma_arr = np.concatenate([Egamma_arr,np.load(f)[()]])
print(len(Egamma_arr))

print("Double Muon ")
print(len(DoubleMuon_arr))

print("Single Muon")
print(len(SingleMuon_arr))

print("Muon EG")
print(len(MuonEG_arr))

def show_duplicate(arr1,arr2):
	a = np.concatenate([arr1,arr2])
	unq, unq_idx, unq_cnt = np.unique(a, return_inverse=True, return_counts=True)
	cnt_mask = unq_cnt > 1
	dup_ids = unq[cnt_mask]
	#print("duplicated: ",dup_ids)
	
	return dup_ids


DM_SM  = show_duplicate(DoubleMuon_arr,SingleMuon_arr)
print("DM_SM",len(DM_SM),DM_SM)

DM_MEG  = show_duplicate(DoubleMuon_arr,MuonEG_arr)
print("DM_MEG",len(DM_MEG),DM_MEG)

SM_MEG = show_duplicate(SingleMuon_arr,MuonEG_arr)
print("SM_MEG",len(SM_MEG),SM_MEG)

EG_DM  = show_duplicate(Egamma_arr,DoubleMuon_arr)
print("EG_DM",len(EG_DM),EG_DM)

EG_SM  = show_duplicate(Egamma_arr,SingleMuon_arr)
print("EG_SM",len(EG_SM),EG_SM)

EG_MEG = show_duplicate(Egamma_arr,MuonEG_arr)
print("EG_MEG",len(EG_MEG),EG_MEG)

#np.save("DM_SM.npy",DM_SM)
#np.save("DM_MEG.npy",DM_MEG)
#np.save("SM_MEG.npy",SM_MEG)
#np.save("EG_DM.npy",EG_DM)
#np.save("EG_SM.npy",EG_SM)
#np.save("EG_MEG.npy",EG_MEG)
