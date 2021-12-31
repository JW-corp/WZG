import uproot 
import matplotlib.pyplot as plt
import numpy as np









def anal_(infile,channel):

	tree = uproot.open(infile)['Events']
	
	channel_mark = tree['channel_mark'].array()
	print("# tot: ",len(channel_mark))
	print('# ele-ch: ',len(channel_mark[channel_mark==11]))
	print('# mu-ch: ',len(channel_mark[channel_mark==13]))
	print('# tau-ch: ',len(channel_mark[channel_mark==15]))
	print('# others: ',len(channel_mark[channel_mark==0]))
	print(" ")
	
	
	
	## 1. channel mask : we only count ele and mu channel
	
	
	if channel =="Electron":
		channel_cut = channel_mark == 11
	elif channel == 'Muon':
		channel_cut = channel_mark == 13
	else:
		print("args error")
	
	
	## 2. check number of tight leptons in each channel
	
	# read
	ntight_electrons = tree['ntight_electrons'].array()
	ntight_muons	 = tree['ntight_muons'].array()
	ntight_photons   = tree['ntight_photons'].array()
	
	# channel cut
	
	
	## 3. check tight object pt
	
	# read
	leading_tight_electrons_pt = tree['tight_electrons_pt'].array()
	leading_tight_muons_pt	   = tree['tight_muons_pt'].array()
	leading_tight_photons_pt   = tree['tight_photon_pt'].array()
	
	
	
	## 4. check M(ll) in two or more tight object cuts
	
	# read
	M_die  = tree['Ele_dileptonmass'].array()
	M_dimu = tree['Mu_dileptonmass'].array()
	Zele1_pt  = tree['Z_ele1_pt'].array()
	Zele2_pt  = tree['Z_ele2_pt'].array()
	Zmu1_pt  = tree['Z_mu1_pt'].array()
	Zmu2_pt  = tree['Z_mu2_pt'].array()
	
	
	# 5.  cuts
	M_die		= M_die[channel_cut & (ntight_electrons>1)]
	Zele1_pt	= Zele1_pt[channel_cut & (ntight_electrons>1)]
	Zele2_pt	= Zele2_pt[channel_cut & (ntight_electrons>1)]
	M_dimu		= M_dimu[channel_cut & (ntight_muons>1)]
	Zmu1_pt		= Zmu1_pt[channel_cut & (ntight_muons>1)]
	Zmu2_pt		= Zmu2_pt[channel_cut & (ntight_muons>1)]
	


	leading_tight_electrons_pt = leading_tight_electrons_pt[channel_cut & (ntight_electrons>0)]
	leading_tight_muons_pt	   = leading_tight_muons_pt[channel_cut & (ntight_muons>0)]
	leading_tight_photons_pt   = leading_tight_photons_pt[channel_cut & (ntight_photons>0)]



	ntight_electrons = ntight_electrons[channel_cut]
	ntight_muons	 = ntight_muons[channel_cut]
	ntight_photons   = ntight_photons[channel_cut]

	print(" ")
	print("Electron selected: {0} -> {1} : {2:.2f}%".format(len(ntight_electrons),len(ntight_electrons[ntight_electrons>0]),100* len(ntight_electrons[ntight_electrons>0])/ len(ntight_electrons)))
	print("Muon selected: {0} -> {1} : {2:.2f}%".format(len(ntight_muons),len(ntight_electrons[ntight_muons>0]),100* len(ntight_electrons[ntight_muons>0])/ len(ntight_muons)))
	print("Photon selected: {0} -> {1} : {2:.2f}%".format(len(ntight_photons),len(ntight_electrons[ntight_photons>0]),100* len(ntight_electrons[ntight_photons>0])/ len(ntight_photons)))



	return M_die,M_dimu,leading_tight_electrons_pt,leading_tight_muons_pt,leading_tight_photons_pt,ntight_electrons,ntight_muons,ntight_photons


#Channel = 'Electron'
Channel = 'Muon'


M_diele1,M_dimu1 , leading_tight_electrons_pt1,leading_tight_muons_pt1,leading_tight_photons_pt1 , ntight_electrons1,ntight_muons1,ntight_photons1 = anal_('KNU_PKU/793428D5-D85C-9D40-AA0D-E7C718454172_Skim.root',Channel)
M_diele2,M_dimu2 , leading_tight_electrons_pt2,leading_tight_muons_pt2,leading_tight_photons_pt2 , ntight_electrons2,ntight_muons2,ntight_photons2 = anal_('Torino/793428D5-D85C-9D40-AA0D-E7C718454172_Skim.root',Channel)



# draw

#title='N_of_selected_electron';histname_org  = ntight_electrons1; histname_comp =  ntight_electrons2; MIN=0; MAX=5 ; bins=6 ;
#title='N_of_selected_muons';histname_org  = ntight_muons1; histname_comp =  ntight_muons2; MIN=0; MAX=5 ; bins=6 ;
#title='N_of_selected_photons';histname_org  = ntight_photons1; histname_comp =  ntight_photons2; MIN=0; MAX=5 ; bins=6 ;

#title='tight_electron_pt';histname_org  = leading_tight_electrons_pt1; histname_comp =  leading_tight_electrons_pt2; MIN=0; MAX=200 ; bins=21 ;
#title='tight_muon_pt';histname_org  = leading_tight_muons_pt1; histname_comp =  leading_tight_muons_pt2; MIN=0; MAX=200 ; bins=21 ;
#title='tight_photon_pt';histname_org  = leading_tight_photons_pt1; histname_comp =  leading_tight_photons_pt2; MIN=0; MAX=200 ; bins=21 ;


title='Dimuon_mass';histname_org  = M_dimu1; histname_comp =  M_dimu2; MIN=0; MAX=200 ; bins=41 ;
#title='Diele_mass';histname_org  = M_diele1; histname_comp =  M_diele2; MIN=0; MAX=200 ; bins=41 ;
#title='zlep1_pt';histname_org  = Zlep1_pt1; histname_comp = Zlep1_pt2; MIN=0; MAX=200 ; bins=21 ;
#title='zlep2_pt';histname_org  = Zlep2_pt1; histname_comp = Zlep2_pt2; MIN=0; MAX=200 ; bins=21 ;






plt.hist(np.clip(histname_org,MIN,MAX),bins=np.linspace(MIN,MAX,bins),linewidth=2,histtype='step', label='PKU-KNU')
plt.hist(np.clip(histname_comp,MIN,MAX),bins=np.linspace(MIN,MAX,bins),linewidth=2,histtype='step', label='Torino')

#plt.hist(histname_org,bins=np.linspace(MIN,MAX,bins),linewidth=2,histtype='step', label='PKU-KNU')
#plt.hist(histname_comp,bins=np.linspace(MIN,MAX,bins),linewidth=2,histtype='step', label='Torino')

plt.legend()
plt.xlabel(title)
plt.title(Channel + ' ' + 'channel')
plt.grid(alpha=0.5)
plt.savefig(title + '_' + Channel + "_" + 'channel.png')

 
 



