#eee_2018 = {'TTWJets' : 0.08494535389445367
#,'tZq' : 0.15671086096185374
#,'TTGJets' : 0.5118574755144031
#,'TTZtoLL' : 0.8665960775858972
#,'WZG' : 2.59034978125
#,'Fake_Photon' : 3.23113691822749
#,'WZ' : 4.215307287753569
#,'ZGToLLG' : 5.342383075613633
#,'ZZ' : 6.437842
#,'Egamma' : 23.0}
#
#eemu_2018 = {'tZq' : 0.17599364268176934
#,'TTWJets' : 0.19744055229521662
#,'ZGToLLG' : 0.6164288164169576
#,'TTGJets' : 0.9306499554807329
#,'TTZtoLL' : 0.9759632830994114
#,'ZZ' : 1.6094605
#,'Fake_Photon' : 2.179492827533051
#,'WZG' : 3.0044809375
#,'WZ' : 3.6654845980465818
#,'Egamma' : 18.0}
#
#
#eee_2017 = {"TTWJets" : 0.1164167265063389
#,"tZq" : 0.13170698430181385
#,"TTGJets" : 0.23864331248759046
#,"TTZtoLL" : 0.7204606482285714
#,"Fake_Photon" : 2.017346133841179
#,"WZG" : 2.029929584375
#,"WZ" : 3.1949114206128133
#,"ZGToLLG" : 3.3420234045367625
#,"ZZ" : 5.0450198
#,"DoubleEG" : 13.0}
#
#
#eemu_2017 = {"tZq" : 0.13391313144254774
#,"TTWJets" : 0.17976112181125858
#,"ZGToLLG" : 0.5440503216687753
#,"TTZtoLL" : 0.8106987053714285
#,"TTGJets" : 1.0568489553021865
#,"Fake_Photon" : 1.4082106189809076
#,"WZG" : 2.35446378125
#,"ZZ" : 2.5225099
#,"WZ" : 3.3401346670043046
#,"DoubleEG" : 10.0}



# -- with fake lepton estimation
#eee_2018_CRZJets = {"TTWJets"		 : 0.0
#,"tZq"			 : 0.007366478584197991
#,"TTZtoLL"		 : 0.02515223598519496
#,"TTGJets"		 : 0.038218160342671274
#,"WZG"			 : 0.16085708945304017
#,"ZGToLLG"		: 0.24653607017346596
#,"Fake_Photon"	: 0.34226033518068355
#,"WZ"			 : 0.43696646858095506
#,"ZZ"			 : 0.7635241770969916
#,"FakeLepton"	 : 1.7570576816797256
#,"Egamma"		 : 3.0}




#eee_2018_Signal = {"TTWJets"		 : 0.02130421751198272
#,"tZq"			 : 0.06943330762589854
#,"TTGJets"		 : 0.15995193320178
#,"TTZtoLL"		 : 0.295179068043656
#,"WZG"			 : 1.1735421708497613
#,"Fake_Photon"	 : 1.2781432252718699
#,"ZGToLLG"		 : 1.4920127804659007
#,"WZ"			 : 1.8192250935569325
#,"ZZ"			 : 1.8298688565146826
#,"FakeLepton"	 : 3.6310926228761673
#,"Egamma"		 : 11.0}




# Fakelepton genFlav
#eee_2018_CRZJets={"TTWJets"			 : 0.0
#,"ZGToLLG"			 : 0.0
#,"tZq"			 	 : 0.006312627760807455
#,"TTZtoLL"			 : 0.02295464458970269
#,"WZG"				 : 0.13530732333074336
#,"FakePhoton"		 : 0.34226033518068355
#,"WZ"				 : 0.43696646858095506
#,"ZZ"				 : 0.7635241770969916
#,"FakeLepton"		 : 1.7570576816797256
#,"Egamma"			 : 3.0}


#eee_2018_Signal={"TTWJets"		: 0.019421831370141463
#,"tZq"			: 0.06325330860025923
#,"TTZtoLL"		: 0.2546259270203022
#,"ZGToLLG"		: 0.27553771351210554
#,"WZG"			: 1.040461884201646
#,"FakePhoton"  : 1.27814322527187
#,"ZZ"			:		1.5688808213967218
#,"WZ"			: 1.8192250935569325
#,"FakeLepton"  : 3.6310926228761673
#,"Egamma"	    : 11.0}



# Fakelepton + RunC
eee_2018_CRZJets={"TTWJets"			: 0.0
,"ZGToLLG"			: 0.0
,"tZq"				: 0.007109740315794325
,"TTZtoLL"			: 0.025990830060640888
,"WZG"				: 0.15361954963926713
,"WZ"				: 0.5013767834377475
,"ZZ"			    : 0.8720926977875798
,"FakeLepton"		: 1.7570576816797256
,"Egamma"			: 4.0}






def rep(dict_):
	bkg=0
	sig=0
	data=0
	list_key=[]
	for i,j in dict_.items():
		print("{0:12} : {1:.3f}".format(i,j))

		if not ((i == 'WZG') or (i=='Egamma') or (i=='DoubleEG')):
			list_key.append(i)

		if not ((i == 'WZG') or (i=='Egamma') or (i=='DoubleEG')):
			bkg += j

		if (i=='WZG'):
			sig = j

		if ((i=='Egamma') or (i=='DoubleEG')):
			data = j 
	list_key.append('WZG')
	print(list_key)
	print('signal: ',sig)
	print('bkg: ',bkg)
	print('data: ',data)

rep(eee_2018_CRZJets)
#rep(eee_2018_Signal)
