import awkward as ak
import uproot
import numpy as np
import matplotlib.pyplot as plt
import os



def read_branches(infile,outname,branches):

	events = uproot.open(infile+':/Events')
	print("Total events: ",events.num_entries)
	#print(events.show())
	
	data_dict={}
	
	for name in branches:
		data_array		= events[name].array()
		print('read {0} legnth {1}'.format(name,len(data_array)))
		data_dict[name] = data_array
	
	np.save(outname,data_dict)
	return data_dict

if __name__ == "__main__":

	infile  = "../../WZG_selector/B/wza_UL16Pre_Nanov9_Skim.root"
	outname = "test_wzg_nomial.npy"
	channel = "WZG"

	if channel == "WZG": 

		branches=[
		"WZG_lepton1_pt"
		,"WZG_lepton1_eta"      
		,"WZG_lepton1_phi"     
		,"WZG_lepton2_pt"     
		,"WZG_lepton2_eta"      
		,"WZG_lepton2_phi"     
		,"WZG_lepton3_pt"     
		,"WZG_lepton3_eta"
		,"WZG_lepton3_phi"      
		,"WZG_photon_pt"     
		,"WZG_photon_eta"       
		,"WZG_photon_phi"       
		,"WZG_dileptonmass"     
		,"WZG_trileptonmass"    
		,"WZG_MET" 
		]

	elif channel == "ZZ": 
		branches=[
		"ZZ_lepton1_pt"
		,"ZZ_lepton1_eta"
		,"ZZ_lepton1_phi"
		,"ZZ_lepton2_pt"
		,"ZZ_lepton2_eta"
		,"ZZ_lepton2_phi"
		,"ZZ_lepton3_pt"
		,"ZZ_lepton3_eta"
		,"ZZ_lepton3_phi"
		,"ZZ_lepton4_pt"
		,"ZZ_lepton4_eta"
		,"ZZ_lepton4_phi"
		,"ZZ_mllz1"
		,"ZZ_mllz2"
		,"ZZ_trileptonmass"
		,"ZZ_MET"
		]

	elif channel == "ttG": 
		branches=[
    	"ttG_lepton1_pt"
    	,"ttG_lepton1_eta"
    	,"ttG_lepton1_phi"
    	,"ttG_lepton2_pt"
    	,"ttG_lepton2_eta"
    	,"ttG_lepton2_phi"
    	,"ttG_lepton3_pt"
    	,"ttG_lepton3_eta"
    	,"ttG_lepton3_phi"
    	,"ttG_photon_pt"
    	,"ttG_photon_eta"
    	,"ttG_photon_phi"
		,"ttZ_dileptonmass"
		,"ttZ_trileptonmass"
		,"ttZ_MET"
		]

	else:
		raise Exception("No such Control Region")

	hist_options = {
		'pt' : np.linspace(0,50,51)
		,'eta' : np.linspace(-3,3,200)
		,'phi' : np.linspace(-3.2,3.2,200)
		,'dileptonmass' : np.linspace(60,120,61)
		,'trileptonmass' : np.linspace(50,200,151)
		,'MET' : np.linspace(0,200,200)
	}


	# First, read and save all branches
	if not os.path.isfile(outname):
		data_dict  = read_branches(infile,outname,branches)

	# If you already had data, just read and go ahead
	else:
		data_dict = np.load(outname,allow_pickle='True')[()]

	# Option I Auto gen
	for name in branches:
		bins = hist_options[name.split('_')[-1]]
		h1 = data_dict[name]		
		plt.hist(h1,bins=bins,histtype='step')
		plt.savefig(name + '.png')
		plt.close()
	
	# Option II Single gen
	#bins = hist_options[name.split('_')[0]]
	#h1   = data_dict["WZG_lepton3_pt"]
	#plt.hist(h1,bins=bins,histtype='step')
	#plt.show()









