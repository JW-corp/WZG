## --For All SB
#low_isochg = list(range(3,9,1))
#high_isochg = list(range(8,14,1))
#closure_dict={}
#
#for l,low in enumerate(low_isochg):
#	for h,high in enumerate(high_isochg):
#		if l > h:
#			continue
#		
#		name = f"from_{low}_to_{high}"
#		closure_dict[name] = [low,high]


# --Just test for one SB
closure_dict = {"from_4_to_10":[4,10]}



filelist_data = [
"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/DoubleEG_Run2016B_2016.root"
,"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/DoubleEG_Run2016C_2016.root"
,"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/DoubleEG_Run2016D_2016.root"
,"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/DoubleEG_Run2016E_2016.root"
,"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/DoubleEG_Run2016F_2016.root"
,"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/DoubleEG_Run2016G_2016.root"
,"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/DoubleEG_Run2016H_2016.root"
,"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/DoubleMuon_Run2016B_2016.root"
,"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/DoubleMuon_Run2016C_2016.root"
,"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/DoubleMuon_Run2016D_2016.root"
,"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/DoubleMuon_Run2016E_2016.root"
,"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/DoubleMuon_Run2016F_2016.root"
,"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/DoubleMuon_Run2016G_2016.root"
,"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/DoubleMuon_Run2016H_2016.root"
,"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/MuonEG_Run2016B_2016.root"
,"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/MuonEG_Run2016C_2016.root"
,"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/MuonEG_Run2016D_2016.root"
,"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/MuonEG_Run2016E_2016.root"
,"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/MuonEG_Run2016F_2016.root"
,"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/MuonEG_Run2016G_2016.root"
,"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/MuonEG_Run2016H_2016.root"
,"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/SingleElectron_Run2016B_2016.root"
,"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/SingleElectron_Run2016C_2016.root"
,"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/SingleElectron_Run2016D_2016.root"
,"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/SingleElectron_Run2016E_2016.root"
,"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/SingleElectron_Run2016F_2016.root"
,"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/SingleElectron_Run2016G_2016.root"
,"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/SingleElectron_Run2016H_2016.root"
,"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/SingleMuon_Run2016B_2016.root"
,"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/SingleMuon_Run2016C_2016.root"
,"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/SingleMuon_Run2016D_2016.root"
,"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/SingleMuon_Run2016E_2016.root"
,"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/SingleMuon_Run2016F_2016.root"
,"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/SingleMuon_Run2016G_2016.root"
,"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/SingleMuon_Run2016H_2016.root"
]


# Di-lepton requirement -> WZG and ZG are overlapped
filelist_MC ={
   "ZGToLLG":
		{"name":"ZGToLLG",
		"path":"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8_2016.root",
		"xsec":55.48},
#	"WZG":
#		{"name":"WZG",
#		"path":"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/LLWA_WToLNu_4FS_TuneCP5_13TeV-amcatnlo-pythia8_2016.root",
#		"xsec":0.0384},
}



filelist_pseudo_data ={
   "DYJetsToLL":
		{"name":"DYJetsToLL",
		"path":"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8_2016.root",
		"xsec":6077.22},
   "ZGToLLG":
		{"name":"ZGToLLG",
		"path":"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8_2016.root",
		"xsec":55.48},
	"WZG":
		{"name":"WZG",
		"path":"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/LLWA_WToLNu_4FS_TuneCP5_13TeV-amcatnlo-pythia8_2016.root",
		"xsec":0.0384},
	"TTG":
			{"name":"TTGJets", 
"path": "/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_2016.root",
			"xsec":3.697,
			"color":3},
	"TTZLLNuNu":
			{"name":"TTZToLLNuNu", 
			 "path":"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8_2016.root",
			"xsec":0.2529,
			"color":4},
	"TTZLL":
			{"name":"TTZToLL", 
			"path":"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8_2016.root",
			"xsec":0.05324,
			"color":44},
	"TTW":
			{"name":"TTWJetsToLNu", 
			 "path":"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_2016.root",
			"xsec":0.2043,
			"color":5},
	"TTTT":
			{"name":"TTTT", 
			"path":"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/TTTT_TuneCP5_13TeV-amcatnlo-pythia8_2016.root",
			"xsec":0.008213,
			"color":45},
	"tZq":
			{"name":"tZq_ll", 
			"path":"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-amcatnlo-pythia8_2016.root",
			"xsec":0.07358,
			"color":6},
	"sT":
			{"name":"sT top", 
			"path":"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/ST_tW_top_5f_DS_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8_2016.root",
			"xsec":33.67,
			"color":46},
	"sT_anti":
			{"name":"sT antitop", 
			"path":"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/ST_tW_antitop_5f_DS_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8_2016.root",
			"xsec":35.13,
			"color":46},
	"WWW":
			{"name":"WWW", 
			"path":"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8_2016.root",
			"xsec":0.2086,
			"color":7},
	"WWZ":
			{"name":"WWZ", 
			"path":"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8_2016.root",
			"xsec":0.1707,
			"color":47},
	"WG":
			{"name":"WGToLNuG",
			"path":"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/WGToLNuG_01J_5f_PDFWeights_TuneCP5_13TeV-amcatnloFXFX-pythia8_2016.root",
			"xsec":190.8,
			"color":39},
		"qqZZ":
			{"name":"qqZZ",
			"path":"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/ZZTo4L_TuneCP5_13TeV_powheg_pythia8_2016.root",
			"xsec":1.325,
			"color":12},
		"ggZZ_2e2mu":
			{"name":"ggZZ_2e2mu",
			"path":"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/GluGluToContinToZZTo2e2mu_TuneCP5_13TeV-mcfm701-pythia8_2016.root",
			"xsec":0.00319,
			"color":13},
		"ggZZ_2e2nu":
			{"name":"ggZZ_2e2nu",
			"path":"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/GluGluToContinToZZTo2e2nu_TuneCP5_13TeV-mcfm701-pythia8_2016.root",
			"xsec":0.00319,
			"color":13},
		"ggZZ_2e2tau":
			{"name":"ggZZ_2e2tau",
			"path":"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/GluGluToContinToZZTo2e2tau_TuneCP5_13TeV-mcfm701-pythia8_2016.root",
			"xsec":0.00319,
			"color":13},
		"ggZZ_2mu2nu":
			{"name":"ggZZ_2mu2nu",
			"path":"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/GluGluToContinToZZTo2mu2nu_TuneCP5_13TeV-mcfm701-pythia8_2016.root",
			"xsec":0.00319,
			"color":13},
		"ggZZ_2mu2tau":
			{"name":"ggZZ_2mu2tau",
			"path":"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/GluGluToContinToZZTo2mu2tau_TuneCP5_13TeV-mcfm701-pythia8_2016.root",
			"xsec":0.00319,
			"color":13},
		"ggZZ_4e":
			{"name":"ggZZ_4e",
			"path":"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/GluGluToContinToZZTo4e_TuneCP5_13TeV-mcfm701-pythia8_2016.root",
			"xsec":0.00159,
			"color":13},
		"ggZZ_4mu":
			{"name":"ggZZ_4mu",
			"path":"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/GluGluToContinToZZTo4mu_TuneCP5_13TeV-mcfm701-pythia8_2016.root",
			"xsec":0.00159,
			"color":13},
		"ggZZ_4tau":
			{"name":"ggZZ_4tau",
			"path":"/cms/ldap_home/jwkim2/New_ccp/FakePhoton_CR/merged/GluGluToContinToZZTo4tau_TuneCP5_13TeV-mcfm701-pythia8_2016.root",
			"xsec":0.00159,
			"color":13},
}


pt_dicts={
	"EB_PT1": [20,30,1],
	"EB_PT2": [30,50,1],
	"EB_PT3": [50,80,1],
	"EB_PT4": [80,120,1],
	"EB_PT5": [120,5000,1],
	"EE_PT1": [20,50,0],
	"EE_PT2": [50,5000,0]
}