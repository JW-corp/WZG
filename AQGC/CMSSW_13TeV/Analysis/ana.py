import uproot
import matplotlib.pyplot as plt
import mplhep as hep
import numpy as np
import pandas as pd
import awkward as ak
import vector
from IPython.display import display
from ana_db import hist_name_dict, out_name_dict

def Read_Tree(path):
	tree = uproot.open(path)['LHEF']
	Evt_num = tree.num_entries
	print('there are {0} numebr of events'.format(Evt_num))
	Particles = tree.arrays(filter_name='Particle*')
	
	
	#print("show me the PID: ",Particles['Particle.PID'])
	
	ele_mask = abs(Particles['Particle.PID'])==11
	mu_mask  = abs(Particles['Particle.PID'])==13

	# only muon or electron channels are considered
	basic_mask = (ak.num(Particles['Particle.PT'][ele_mask]) +ak.num(Particles['Particle.PT'][mu_mask])) >= 3
	print("Before basic channel cut: ",len(Particles))
	print("After basic channel cut: ",len(Particles[basic_mask]))
	return Evt_num,Particles[basic_mask]


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
	
	Lepton_mask = (abs(Particles['Particle.PID']) == 11) | (abs(Particles['Particle.PID']) == 13)
	Lepton = ak.zip({
	"PID" :	Particles['Particle.PID'][Lepton_mask],
	"PT" :	Particles['Particle.PT'][Lepton_mask],
	"Eta":	Particles['Particle.Eta'][Lepton_mask],
	"Phi":	Particles['Particle.Phi'][Lepton_mask],
	"E" :	Particles['Particle.E'][Lepton_mask],
	"Px" : Particles['Particle.Px'][Lepton_mask],
	"Py" : Particles['Particle.Py'][Lepton_mask],  
	"Pz" : Particles['Particle.Pz'][Lepton_mask],  
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

	
	return Lepton,Photon,Wboson


# --Main analysis code
def Analysis(Particles):
	
	Lepton,Photon,Wboson = Make_Object_Array(Particles)
	
	WLep_vec  = vector.obj(px=Lepton[:,0].Px,py=Lepton[:,0].Py,pz=Lepton[:,0].Pz,E=Lepton[:,0].E)
	ZLep1_vec = vector.obj(px=Lepton[:,1].Px,py=Lepton[:,1].Py,pz=Lepton[:,1].Pz,E=Lepton[:,1].E)
	ZLep2_vec = vector.obj(px=Lepton[:,2].Px,py=Lepton[:,2].Py,pz=Lepton[:,2].Pz,E=Lepton[:,2].E)
	Pho_vec	  = vector.obj(px=Photon[:,0].Px,py=Photon[:,0].Py,pz=Photon[:,0].Pz,E=Photon[:,0].E)

	WLep  = Lepton[:,0]
	ZLep1 = Lepton[:,1]
	ZLep2 = Lepton[:,2]
	Pho   = Photon[:,0]

	Z_vec      = ZLep1_vec + ZLep2_vec
	ZA_vec     = ZLep1_vec + ZLep2_vec + Pho_vec
	lll_vec    = ZLep1_vec + ZLep2_vec + WLep_vec

	Mll  = Z_vec.M
	MllA = ZA_vec.M
	Mlll = lll_vec.M

	lepPT_mask = (ZLep1.PT > 25) & (ZLep2.PT > 15) & (WLep.PT > 25 )
	Mll_mask   = abs(Mll-91.188)<=15
	Mlll_mask  = Mlll > 100
	MllA_mask  = MllA > 250	

	SR_selection_mask = lepPT_mask & Mll_mask & Mlll_mask & MllA_mask

	MllA  = MllA[SR_selection_mask]
	Mll   = Mll[SR_selection_mask]
	PhoPT = Pho.PT[SR_selection_mask]
	

	# You can add more here...
	return MllA




# --Added for more complex channel-wise coding
def Process(path):
	Evt_num,Particles  = Read_Tree(path)
	MllA			   = Analysis(Particles)
	return Evt_num,MllA


def draw_hist(df,target,start,end,bin,hist):

	# read data
	Nevt,llA_mass_arr	= Process(df.loc[target]['path'])
	arr_w				= np.ones(len(llA_mass_arr)) *  35.86*1000 *df.loc[target]['xsec'] / Nevt # weight


	# make hist
	h_llA_mass   = np.clip(llA_mass_arr,start,end)

	bins	 = np.linspace(start, end, bin) 
	binwidth = (end - start) / bin

	if hist=='llA_mass':
		h1 = plt.hist(h_llA_mass, weights = arr_w, bins=bins, alpha=1, histtype='step', linewidth=2,label=target)
	else:
		print("no ..!")	

	plt.xlabel(hist, fontsize=16)  # Y-label
	plt.ylabel("Number of Events/(%d GeV)" % binwidth, fontsize=16)  # Y-label

	print("## Breakdown histograms")
	bin_contents = h1[0]
	bin_x		 = h1[1]
	
	return bin_x,bin_contents




def run(hist_name_list,df,start,end,Nbins,variable,sm_y,outname):
	aQGC_y_dict = {}
	for hist_name in hist_name_list:
		_, y = draw_hist(df,hist_name,start,end,Nbins,variable)

		# get aQGC/SM ratio
		aQGC_y_dict[hist_name] = y / sm_y

	graph_x  = [(bin_x[i] + bin_x[i+1])/2 for i in range(0,len(bin_x)-1)]
	np.save(outname+'.npy',[graph_x,aQGC_y_dict])





if __name__ == "__main__":

	# Read DB
	df = pd.read_csv('xsec_aQGC_DB.csv',delimiter=',')
	df.set_index('name',inplace=True)

	# variables
	plt.style.use(hep.style.ROOT)
	variable,mini,maxi = 'llA_mass',250,1000 # histname, xmin xmax

	#Nbins=15
	Nbins=6

	# Set_parameters
	param_list = ['FT0' ,'FT1' ,'FT2' ,'FT5' ,'FT6' ,'FT7' ,'FM0' ,'FM1' ,'FM2' ,'FM3' ,'FM4' ,'FM6' ,'FM7'] 
	#param_list = ['FT0'] 


	#param = param_list[0]
	for param in param_list:
		hist_name_list = hist_name_dict[param]
		outname = out_name_dict[param]
		
		# Draw SM/
		bin_x, sm_y = draw_hist(df,'sm',mini,maxi,Nbins,variable)

		## Draw aQGC
		run(hist_name_list,df,mini,maxi,Nbins,variable,sm_y,outname)

		plt.xticks(fontsize=16)  # xtick size
		plt.yticks(fontsize=16)  # ytick size
		
		plt.grid(alpha=0.5)  # grid
		plt.legend(prop={"size": 15})  # show legend
		plt.title(outname+'.png',fontsize=17)	
		plt.yscale('log')
	
		#plt.show()
		plt.savefig(outname)
		plt.close()
