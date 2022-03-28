import uproot
import matplotlib.pyplot as plt
import mplhep as hep
import numpy as np
import pandas as pd
import awkward as ak
import vector
from IPython.display import display

def Read_Tree(path):
	tree = uproot.open(path)['LHEF']
	Evt_num = tree.num_entries
	print('there are {0} numebr of events'.format(Evt_num))
	Particles = tree.arrays(filter_name='Particle*')
	
	is_Ele = abs(Particles['Particle.PID']) == 11
	is_Ele_ch = ak.num(Particles['Particle.PID'][is_Ele]) == 2
	
	is_Mu = abs(Particles['Particle.PID']) == 13
	is_Mu_ch = ak.num(Particles['Particle.PID'][is_Mu]) == 2
	
	Particles_ele_ch = Particles[is_Ele_ch ]
	Particles_mu_ch  = Particles[is_Mu_ch ]
	
	
	return Evt_num,Particles_ele_ch,Particles_mu_ch


def Make_Object_Array(Particles):	
	Photon_mask   = (Particles['Particle.PID'] == 22)
	Photon = ak.zip({
	"PT" :	Particles['Particle.PT'][Photon_mask],
	"Eta":	Particles['Particle.Eta'][Photon_mask],
	"Phi":	Particles['Particle.Phi'][Photon_mask],
	"E" :	Particles['Particle.E'][Photon_mask],
	"Px" : Particles['Particle.Px'][Photon_mask],
	"Py" : Particles['Particle.Py'][Photon_mask],  
	"Pz" : Particles['Particle.Pz'][Photon_mask],  
	})
	
	Electron_mask = abs(Particles['Particle.PID']) == 11
	Electron = ak.zip({
	"PT" :	Particles['Particle.PT'][Electron_mask],
	"Eta":	Particles['Particle.Eta'][Electron_mask],
	"Phi":	Particles['Particle.Phi'][Electron_mask],
	"E" :	Particles['Particle.E'][Electron_mask],
	"Px" : Particles['Particle.Px'][Electron_mask],
	"Py" : Particles['Particle.Py'][Electron_mask],  
	"Pz" : Particles['Particle.Pz'][Electron_mask],  
	})   
	
	Muon_mask = abs(Particles['Particle.PID']) == 13
	Muon = ak.zip({
	"PT" :	Particles['Particle.PT'][Muon_mask],
	"Eta":	Particles['Particle.Eta'][Muon_mask],
	"Phi":	Particles['Particle.Phi'][Muon_mask],
	"E" :	Particles['Particle.E'][Muon_mask],
	"Px" : Particles['Particle.Px'][Muon_mask],
	"Py" : Particles['Particle.Py'][Muon_mask],  
	"Pz" : Particles['Particle.Pz'][Muon_mask],  
	})
	
	W_mask = abs(Particles['Particle.PID']) ==24 
	Wboson = ak.zip({
	"PT" :	Particles['Particle.PT'][W_mask],
	"Eta":	Particles['Particle.Eta'][W_mask],
	"Phi":	Particles['Particle.Phi'][W_mask],
	"E" :	Particles['Particle.E'][W_mask],
	"Px" : Particles['Particle.Px'][W_mask],
	"Py" : Particles['Particle.Py'][W_mask],  
	"Pz" : Particles['Particle.Pz'][W_mask],  
	})

	
	return Electron,Muon,Photon,Wboson


def Analysis(chmark,Particles):
	
	print("Start analysis {0} channel".format(chmark))
	Electron,Muon,Photon,Wboson = Make_Object_Array(Particles)
	
	if chmark=='Electron':
		print("test -- contain muon? ",ak.sum(ak.num(Muon)))
		print("test -- does not have diele? ",ak.sum(ak.num(Electron) !=2))
		Lep1_vec = vector.obj(px=Electron[:,0].Px,py=Electron[:,0].Py,pz=Electron[:,0].Pz,E=Electron[:,0].E)
		Lep2_vec = vector.obj(px=Electron[:,1].Px,py=Electron[:,1].Py,pz=Electron[:,1].Pz,E=Electron[:,1].E)
		
	elif chmark=='Muon':
		print("test -- contain Electron? ",ak.sum(ak.num(Electron)))
		print("test -- does not have dimu? ",ak.sum(ak.num(Muon) !=2))
		Lep1_vec = vector.obj(px=Muon[:,0].Px,py=Muon[:,0].Py,pz=Muon[:,0].Pz,E=Muon[:,0].E)
		Lep2_vec = vector.obj(px=Muon[:,1].Px,py=Muon[:,1].Py,pz=Muon[:,1].Pz,E=Muon[:,1].E)
	else:
		raise NameError('unavailable channel name')

	W_vec	= vector.obj(px=Wboson[:,0].Px,py=Wboson[:,0].Py,pz=Wboson[:,0].Pz,E=Wboson[:,0].E)
	WZ_vec	= Lep1_vec + Lep2_vec + W_vec	
	
	Mwz   =  WZ_vec.M.to_numpy()
	phoPT =  ak.flatten(Photon.PT).to_numpy()
	return Mwz,phoPT 



def Process(path):
	Evt_num,Particles_ele_ch,Particles_mu_ch = Read_Tree(path)
	
	Nevt = Evt_num
	print("Elech + Much == Evtnum ? ",len(Particles_ele_ch) + len(Particles_mu_ch) == Evt_num)
	ele_Mwz,ele_phoPT   = Analysis("Electron",Particles_ele_ch)
	mu_Mwz,mu_phoPT   = Analysis("Muon",Particles_mu_ch)
	Mwz_arr   = np.concatenate((ele_Mwz, mu_Mwz), axis = 0)
	phoPT_arr = np.concatenate((ele_phoPT, mu_phoPT), axis = 0)
	
	return Nevt,Mwz_arr,phoPT_arr






def draw_hist(df,target,start,end,bin,hist):
	Nevt,arr_Mwz, arr_phoPT = Process(df.loc[target]['path'])
	arr_w = np.ones(len(arr_Mwz)) *  59.7*1000 *df.loc[target]['xsec'] / Nevt

	h_Mwz   = np.clip(arr_Mwz,start,end)
	h_phoPT = np.clip(arr_phoPT,start,end)

	bins = np.linspace(start, end, bin) 
	binwidth = (end - start) / bin

	if hist=='Mwz':
		h1 = plt.hist(h_Mwz, weights = arr_w, bins=bins, alpha=1, histtype='step', linewidth=2, label=target)
	elif hist=='phoPT':
		h1 = plt.hist(h_phoPT, weights = arr_w, bins=bins, alpha=1,	histtype='step', linewidth=2, label=target)
	else:
		print("no ..!")	

	plt.xlabel(hist, fontsize=16)  # Y-label
	plt.ylabel("Number of Events/(%d GeV)" % binwidth, fontsize=16)  # Y-label


	return 0




if __name__ == "__main__":

	df = pd.read_csv('aQGC_list_db.csv',delimiter=',')
	df.set_index('name',inplace=True)
	#display(df)

	plt.style.use(hep.style.ROOT)

	#variable,maxi = 'phoPT',500
	variable,maxi = 'Mwz',1500


	draw_hist(df,'sm',0,maxi,15,variable)
	draw_hist(df,'aQGC_all0',0,maxi,15,variable)
	#draw_hist(df,'FT0_1.00E-12',0,maxi,15,variable)
	#draw_hist(df,'FT0_2.00E-12',0,maxi,15,variable)
	#draw_hist(df,'FT0_5.00E-12',0,maxi,15,variable)
	#draw_hist(df,'FT0_1.00E-11',0,maxi,15,variable)
	#outname = 'FT0_mWZ.png'	


	#draw_hist(df,'FT1_1.00E-12',0,maxi,15,variable)
	#draw_hist(df,'FT1_2.00E-12',0,maxi,15,variable)
	#draw_hist(df,'FT1_3.00E-12',0,maxi,15,variable)
	#draw_hist(df,'FT1_4.00E-12',0,maxi,15,variable)
	#draw_hist(df,'FT1_6.00E-12',0,maxi,15,variable)
	#draw_hist(df,'FT1_8.00E-12',0,maxi,15,variable)
	#draw_hist(df,'FT1_1.00E-11',0,maxi,15,variable)
	#outname = 'FT1_mWZ.png'	

	#draw_hist(df,'FT2_1.00E-12',0,maxi,15,variable)
	#draw_hist(df,'FT2_3.00E-12',0,maxi,15,variable)
	#draw_hist(df,'FT2_5.00E-12',0,maxi,15,variable)
	#draw_hist(df,'FT2_7.00E-12',0,maxi,15,variable)
	#draw_hist(df,'FT2_1.00E-11',0,maxi,15,variable)
	#draw_hist(df,'FT2_3.00E-11',0,maxi,15,variable)
	#outname = 'FT2_mWZ.png'	

	#draw_hist(df,'FT5_1.00E-12',0,maxi,15,variable)
	#draw_hist(df,'FT5_3.00E-12',0,maxi,15,variable)
	#draw_hist(df,'FT5_5.00E-12',0,maxi,15,variable)
	#draw_hist(df,'FT5_7.00E-12',0,maxi,15,variable)
	#draw_hist(df,'FT5_1.00E-11',0,maxi,15,variable)
	#outname = 'FT5_mWZ.png'	

	#draw_hist(df,'FT6_1.00E-12',0,maxi,15,variable)
	#draw_hist(df,'FT6_3.00E-12',0,maxi,15,variable)
	#draw_hist(df,'FT6_5.00E-12',0,maxi,15,variable)
	#draw_hist(df,'FT6_1.00E-11',0,maxi,15,variable)
	#outname = 'FT6_mWZ.png'	

	#draw_hist(df,'FT7_1.00E-12',0,maxi,15,variable)
	#draw_hist(df,'FT7_3.00E-12',0,maxi,15,variable)
	#draw_hist(df,'FT7_5.00E-12',0,maxi,15,variable)
	#draw_hist(df,'FT7_7.00E-12',0,maxi,15,variable)
	#draw_hist(df,'FT7_1.00E-11',0,maxi,15,variable)
	#draw_hist(df,'FT7_3.00E-11',0,maxi,15,variable)
	#outname = 'FT7_mWZ.png'	

	#draw_hist(df,'FM0_1.00E-11',0,maxi,15,variable)
	#draw_hist(df,'FM0_2.00E-11',0,maxi,15,variable)
	#draw_hist(df,'FM0_4.00E-11',0,maxi,15,variable)
	#draw_hist(df,'FM0_6.00E-11',0,maxi,15,variable)
	#draw_hist(df,'FM0_2.00E-10',0,maxi,15,variable)
	#draw_hist(df,'FM0_1.00E-9',0,maxi,15,variable)
	#outname = 'FM0_mWZ.png'	

	#draw_hist(df,'FM1_1.00E-11',0,maxi,15,variable)
	#draw_hist(df,'FM1_3.00E-11',0,maxi,15,variable)
	#draw_hist(df,'FM1_5.00E-11',0,maxi,15,variable)
	#draw_hist(df,'FM1_7.00E-11',0,maxi,15,variable)
	#draw_hist(df,'FM1_1.00E-10',0,maxi,15,variable)
	#draw_hist(df,'FM1_5.00E-10',0,maxi,15,variable)
	#draw_hist(df,'FM1_1.00E-9',0,maxi,15,variable)
	#draw_hist(df,'FM1_5.00E-9',0,maxi,15,variable)
	#outname = 'FM1_mWZ.png'	

	#draw_hist(df,'FM2_5.00E-12',0,maxi,15,variable)
	#draw_hist(df,'FM2_1.00E-11',0,maxi,15,variable)
	#draw_hist(df,'FM2_2.00E-11',0,maxi,15,variable)
	#draw_hist(df,'FM2_4.00E-11',0,maxi,15,variable)
	#draw_hist(df,'FM2_1.00E-10',0,maxi,15,variable)
	#draw_hist(df,'FM2_5.00E-10',0,maxi,15,variable)
	#outname = 'FM2_mWZ.png'	

	#draw_hist(df,'FM3_1.00E-11',0,maxi,15,variable) 
	#draw_hist(df,'FM3_2.00E-11',0,maxi,15,variable) 
	#draw_hist(df,'FM3_4.00E-11',0,maxi,15,variable) 
	#draw_hist(df,'FM3_6.00E-11',0,maxi,15,variable) 
	#draw_hist(df,'FM3_1.00E-10',0,maxi,15,variable) 
	#draw_hist(df,'FM3_5.00E-10',0,maxi,15,variable) 
	#draw_hist(df,'FM3_7.00E-10',0,maxi,15,variable) 
	#draw_hist(df,'FM3_1.00E-9',0,maxi,15,variable) 
	#outname = 'FM3_mWZ.png'	

	#draw_hist(df,'FM4_5.00E-12',0,maxi,15,variable)   
	#draw_hist(df,'FM4_1.00E-11',0,maxi,15,variable)   
	#draw_hist(df,'FM4_1.50E-11',0,maxi,15,variable)   
	#draw_hist(df,'FM4_2.00E-11',0,maxi,15,variable)   
	#draw_hist(df,'FM4_4.00E-11',0,maxi,15,variable)   
	#draw_hist(df,'FM4_6.00E-11',0,maxi,15,variable)   
	#draw_hist(df,'FM4_8.00E-11',0,maxi,15,variable)   
	#draw_hist(df,'FM4_1.00E-10',0,maxi,15,variable)   
	#outname = 'FM4_mWZ.png'	

	#draw_hist(df,'FM5_3.00E-12',0,maxi,15,variable)     
	#draw_hist(df,'FM5_5.00E-12',0,maxi,15,variable)     
	#draw_hist(df,'FM5_7.00E-12',0,maxi,15,variable)     
	#draw_hist(df,'FM5_1.00E-11',0,maxi,15,variable)     
	#draw_hist(df,'FM5_4.00E-11',0,maxi,15,variable)     
	#draw_hist(df,'FM5_6.00E-11',0,maxi,15,variable)     
	#draw_hist(df,'FM5_8.00E-11',0,maxi,15,variable)     
	#draw_hist(df,'FM5_1.00E-10',0,maxi,15,variable)     
	#outname = 'FM5_mWZ.png'	

	draw_hist(df,'FM7_1.00E-11',0,maxi,15,variable)      
	draw_hist(df,'FM7_3.00E-11',0,maxi,15,variable)      
	draw_hist(df,'FM7_5.00E-11',0,maxi,15,variable)      
	draw_hist(df,'FM7_7.00E-11',0,maxi,15,variable)      
	draw_hist(df,'FM7_1.00E-10',0,maxi,15,variable)      
	draw_hist(df,'FM7_2.00E-10',0,maxi,15,variable)      
	draw_hist(df,'FM7_3.00E-10',0,maxi,15,variable)      
	draw_hist(df,'FM7_4.00E-10',0,maxi,15,variable)      
	draw_hist(df,'FM7_5.00E-10',0,maxi,15,variable)      
	outname = 'FM7_mWZ.png'	

	




	plt.xticks(fontsize=16)  # xtick size
	plt.yticks(fontsize=16)  # ytick size
	
	plt.grid(alpha=0.5)  # grid
	plt.legend(prop={"size": 15})  # show legend
	
	#plt.show()  # show histogram
	plt.savefig(outname)
