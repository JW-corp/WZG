channel = 0
channel_map = {
	0: "WZG",
	1: "WZG_emm",
	2: "WZG_mee",
	3: "WZG_eee",
	4: "WZG_mmm",

	10: "ttZ",
	11: "ttZ_emm",
	12: "ttZ_mee",
	13: "ttZ_eee",
	14: "ttZ_mmm",

	20: "ttG",
	21: "ttG_emm",
	22: "ttG_mee",
	23: "ttG_eee",
	24: "ttG_mmm",

	9: "ZZ",
	5: "ZZ_eemm",
	6: "ZZ_mmee",
	7: "ZZ_eeee",
	8: "ZZ_mmmm"
}

lumi = 59.7
year = "2018"

UpDown = 0
UpDown_map={
	0:None,
	1:"jesTotalUp",
	2:"jesTotalDown",
	3:"jerUp",
	4:"jerDown"
}
# 0: nominal
# 1: JESup 
# 2: JESdown
# 3: JERup
# 4: JERdown


branch = {
	"channel_mark":{
		"name":"channel_mark",
		"axis_name":"channel",
		"bin_array":[1,2,3,4,5],
	},
	"mwa":{
		"name":"mwa",
		"axis_name":"m_{l_{W}#gamma} [GeV]",
		"bin_strategy":"average",
		"xbins":10,
		"xleft":0,
		"xright":200,

	},
	"WZG_dileptonmass":{
		"name":"WZG_dileptonmass",
		"axis_name":"m_{Z} [GeV]",
		"bin_strategy":"average",
		"xbins":3,
		"xleft":75,
		"xright":105,
	},
	"WZG_trileptonmass":{
		"name":"WZG_trileptonmass",
		"axis_name":"m_{lll} [GeV]",
		"bin_array":[100,200,300,500],
	},
	"WZG_mlla":{
		"name":"WZG_mlla",
		"axis_name":"m_{ll#gamma} [GeV]",
		"xbins":10,
		"xleft":0,
		"xright":500,
	},
	"WZG_mllla":{
		"name":"WZG_mllla",
		"axis_name":"m_{lll#gamma} [GeV]",
		"bin_array":[300,600,5000],
		#"bin_array":[300,600,1000],
	},
	"WZG_lepton1_pt":{
		"name":"WZG_lepton1_pt",
		"axis_name":"P_{T, W} [GeV]",
		"xbins":10,
		"xleft":0,
		"xright":200,
	},
	"WZG_lepton1_eta":{
		"name":"WZG_lepton1_eta",
		"axis_name":"#eta_{W}",
		"xbins":6,
		"xleft":-2.5,
		"xright":2.5,
	},
	"WZG_lepton1_phi":{
		"name":"WZG_lepton1_phi",
		"axis_name":"|#phi_{W}|",
		"xbins":6,
		"xleft":-3.15,
		"xright":3.15,
	},
	"WZG_lepton2_pt":{
		"name":"WZG_lepton2_pt",
		"axis_name":"P_{T, Z1} [GeV]",
		"xbins":10,
		"xleft":0,
		"xright":200,
	},
	"WZG_lepton2_eta":{
		"name":"WZG_lepton2_eta",
		"axis_name":"#eta_{Z1}",
		"xbins":6,
		"xleft":-2.5,
		"xright":2.5,
	},
	"WZG_lepton2_phi":{
		"name":"WZG_lepton2_phi",
		"axis_name":"|#phi_{Z1}|",
		"xbins":6,
		"xleft":-3.15,
		"xright":3.15,
	},
	"WZG_lepton3_pt":{
		"name":"WZG_lepton3_pt",
		"axis_name":"P_{T, Z2} [GeV]",
		"xbins":10,
		"xleft":0,
		"xright":200,
	},
	"WZG_lepton3_eta":{
		"name":"WZG_lepton3_eta",
		"axis_name":"|#eta_{Z2}|",
		"xbins":6,
		"xleft":-2.5,
		"xright":2.5,
	},
	"WZG_lepton3_phi":{
		"name":"WZG_lepton3_phi",
		"axis_name":"|#phi_{Z2}|",
		"xbins":6,
		"xleft":-3.15,
		"xright":3.15,
	},
	"WZG_photon_pt":{
		"name":"WZG_photon_pt",
		"axis_name":"P_{T, #gamma} [GeV]",
		"xbins":10,
		"xleft":0,
		"xright":200,
	},
	"WZG_photon_eta":{
		"name":"WZG_photon_eta",
		"axis_name":"#eta_{#gamma}",
		"xbins":6,
		"xleft":-2.5,
		"xright":2.5,
	},
	"WZG_photon_phi":{
		"name":"WZG_photon_phi",
		"axis_name":"|#phi_{#gamma}|",
		"xbins":6,
		"xleft":-3.15,
		"xright":3.15,
	},
	"MET":{
		"name":"MET",
		"axis_name":"MET [GeV]",
		"xbins":5,
		"xleft":30,
		"xright":120,
	},
	"nJets":{
		"name":"nJets",
		"axis_name":"nJets",
		"xbins":8,
		"xleft":0,
		"xright":8,
	},
	"nbJets":{
		"name":"nbJets",
		"axis_name":"nbJets",
		"xbins":8,
		"xleft":0,
		"xright":8,
	},
	"dr_wla":{
		"name":"dr_wla",
		"axis_name":"#Delta R(l_{W}, #gamma)",
		"xbins":20,
		"xleft":0,
		"xright":6,
	},
	"dr_zl1a":{
		"name":"dr_zl1a",
		"axis_name":"#Delta R(l_{Z1}, #gamma)",
		"xbins":20,
		"xleft":0,
		"xright":6,
	},
	"dr_zl2a":{
		"name":"dr_zl2a",
		"axis_name":"#Delta R(l_{Z2}, #gamma)",
		"xbins":20,
		"xleft":0,
		"xright":6,
	}
}



filelist_data = [
"/cms/ldap_home/jwkim2/New_ccp/Ntuplizer/CMSSW_10_6_19/src/PhysicsTools/NanoAODTools/nanoAOD-WVG/FakeLepton/DoubleMuon_Run2018A_0000/DoubleMuon_Run2018A_0000_Skim.root"
]



filelist_MC = {
	}

