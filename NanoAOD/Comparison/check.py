import uproot 
import matplotlib.pyplot as plt
import numpy as np



def analyze_(file,channel='Combined'):

	print("########### start :",file)
	tree	= uproot.open(file)['Events']

	wzg_dilepmass  = tree['WZG_dileptonmass'] .array()


	Npho_sel = tree['ntight_photons'].array()
	Nele_sel	= tree['ntight_electrons'].array()
	Nmu_sel		= tree['ntight_muons'].array()



	rest_pho = len(Npho_sel[Npho_sel > 0])
	rest_ele = len(Nele_sel[Nele_sel>0])
	rest_mu  = len(Nmu_sel[Nmu_sel > 0])

	eff_pho  = 100* float(rest_pho) / len(Npho_sel)
	eff_ele  = 100* float(rest_ele) / len(Nele_sel)
	eff_mu   = 100* float(rest_mu)  / len(Nmu_sel)


	if channel == 'Electron':
		channel_mask = (Nele_sel >= 2)
	elif channel == 'Muon':
		channel_mask = (Nmu_sel >= 2)
	else:
		channel_mask = (Nele_sel >= 2) | (Nmu_sel >= 2)
		
	Npho_sel = Npho_sel[channel_mask]
	Nele_sel = Nele_sel[channel_mask]
	Nmu_sel  = Nmu_sel[channel_mask]	
	wzg_dilepmass = wzg_dilepmass[channel_mask]

	print("Evt after two ele or two mu cut: ",len(wzg_dilepmass)) 
	print("Ele eff: {:.5f}".format(eff_ele))
	print("mu eff: {:.5f}".format(eff_mu,rest_pho))
	print("pho eff: {:.5f}".format(eff_pho,rest_mu))
	print("Evt after {0} channel cut: {1}".format(str(channel),len(wzg_dilepmass)))


	return wzg_dilepmass,Npho_sel,Nele_sel,Nmu_sel


	

file_org  = "KNU_PKU/07BC798B-70E4-5341-8FA0-856C334210BF_Skim.root"
file_comp = "Torino/07BC798B-70E4-5341-8FA0-856C334210BF_Skim.root"
channel = 'Combined'
#channel = 'Electron'
#channel = 'Muon'


wzg_dilepmass_org,Npho_sel_org,Nele_sel_org,Nmu_sel_org		  = 	analyze_(file_org,channel)
wzg_dilepmass_comp,Npho_sel_comp,Nele_sel_comp,Nmu_sel_comp	  = 	analyze_(file_comp,channel)



print(Nele_sel_org)
print(Nele_sel_comp)



# --Hist target 
title='Dilepton_mass';histname_org  =  wzg_dilepmass_org; histname_comp =  wzg_dilepmass_comp; MIN=0; MAX=200 ; bins=20 ; isWeight=True
#title='N_of_selected electron';histname_org  = Nele_sel_org; histname_comp =  Nele_sel_comp; MIN=0; MAX=5 ; bins=6 ; isWeight=True
#title='N_of_selected muon';histname_org  = Nmu_sel_org; histname_comp =  Nmu_sel_comp; MIN=0; MAX=5 ; bins=6 ; isWeight=True
#title='N_of_selected photon';histname_org  = Npho_sel_org; histname_comp =  Npho_sel_comp; MIN=0; MAX=5 ; bins=6 ; isWeight=True



# --Noramlize 1
if isWeight==True:
	weights_org  = np.ones(len(histname_org)) * 1/len(histname_org)
	weights_comp = np.ones(len(histname_comp)) * 1/len(histname_comp)
else:
	weights_org  = np.ones(len(histname_org)) 
	weights_comp = np.ones(len(histname_comp))

# -- Draw
plt.hist(np.clip(histname_org,MIN,MAX),bins=np.linspace(MIN,MAX,bins),linewidth=2,weights = weights_org,histtype='step', label='PKU-KNU')
plt.hist(np.clip(histname_comp,MIN,MAX),bins=np.linspace(MIN,MAX,bins),linewidth=2,weights = weights_comp,histtype='step',label='Torino')

#plt.hist(np.clip(histname_org,MIN,MAX),bins=np.linspace(MIN,MAX,bins),linewidth=2,weights = weights_org,alpha=0.7, label='PKU-KNU')
#plt.hist(np.clip(histname_comp,MIN,MAX),bins=np.linspace(MIN,MAX,bins),linewidth=2,weights = weights_comp,alpha=0.5,label='Torino')

if isWeight:
	plt.xlabel(title + '(norm=1)') 
else:
	plt.xlabel(title) 

plt.title(channel +" " +  'channel')
plt.yscale('log')
plt.legend()
plt.grid(alpha=0.5)
#plt.show()
plt.savefig(title + '_'+ channel +'.png')
