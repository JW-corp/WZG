channel = 9
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

lumi = 41.5
year = "2017"

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
    "ZZ_mllz1":{
        "name":"ZZ_mllz1",
        "axis_name":"m_{Z1} [GeV]",
        "xbins":5,
        "xleft":75,
        "xright":105,
    },
    "ZZ_mllz2":{
        "name":"ZZ_mllz2",
        "axis_name":"m_{Z2} [GeV]",
        "xbins":5,
        "xleft":75,
        "xright":105,
    },
    "ZZ_trileptonmass":{
        "name":"ZZ_trileptonmass",
        "axis_name":"m_{lll} [GeV]",
        "bin_array":[100,150,200,250,300,500],
    },
    "ZZ_lepton1_pt":{
        "name":"ZZ_lepton1_pt",
        "axis_name":"P_{T, l1} [GeV]",
        "xbins":10,
        "xleft":0,
        "xright":200,
    },
    "ZZ_lepton1_eta":{
        "name":"ZZ_lepton1_eta",
        "axis_name":"#eta_{l1}",
        "xbins":6,
        "xleft":-2.5,
        "xright":2.5,
    },
    "ZZ_lepton2_pt":{
        "name":"ZZ_lepton2_pt",
        "axis_name":"P_{T, l2} [GeV]",
        "xbins":10,
        "xleft":0,
        "xright":200,
    },
    "ZZ_lepton2_eta":{
        "name":"ZZ_lepton2_eta",
        "axis_name":"#eta_{l2}",
        "xbins":6,
        "xleft":-2.5,
        "xright":2.5,
    },
    "MET":{
        "name":"MET",
        "axis_name":"MET [GeV]",
        "xbins":10,
        "xleft":0,
        "xright":30,
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
    }
}



filelist_pseudo_data = {
    "QCD_Pt-15to20_EMEnriched": {
        "name": "QCD_Pt-15to20_EMEnriched",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/QCD_Pt-15To20_MuEnrichedPt5_TuneCP5_13TeV-pythia8_2017.root",
        "xsec": 1327000,
        "color": 41,
    },
    "QCD_Pt-20to30_EMEnriched": {
        "name": "QCD_Pt-20to30_EMEnriched",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8_2017.root",
        "xsec": 4908000,
        "color": 41,
    },
    "QCD_Pt-30to50_EMEnriched": {
        "name": "QCD_Pt-30to50_EMEnriched",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8_2017.root",
        "xsec": 6396000,
        "color": 41,
    },
    "QCD_Pt-50to80_EMEnriched": {
        "name": "QCD_Pt-50to80_EMEnriched",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8_2017.root",
        "xsec": 1989000,
        "color": 41,
    },
    "QCD_Pt-80to120_EMEnriched": {
        "name": "QCD_Pt-80to120_EMEnriched",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8_2017.root",
        "xsec": 366500,
        "color": 41,
    },
    "QCD_Pt-120to170_EMEnriched": {
        "name": "QCD_Pt-120to170_EMEnriched",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8_2017.root",
        "xsec": 66490,
        "color": 41,
    },
    "QCD_Pt-170to300_EMEnriched": {
        "name": "QCD_Pt-170to300_EMEnriched",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8_2017.root",
        "xsec": 16480,
        "color": 41,
    },
    "QCD_Pt-300toInf_EMEnriched": {
        "name": "QCD_Pt-300toInf_EMEnriched",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8_2017.root",
        "xsec": 1097,
        "color": 41,
    },
    "QCD_Pt-15To20_MuEnriched": {
        "name": "QCD_Pt-15To20_MuEnriched",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/QCD_Pt-15To20_MuEnrichedPt5_TuneCP5_13TeV-pythia8_2017.root",
        "xsec": 2799000,
        "color": 41,
    },
    "QCD_Pt-20To30_MuEnriched": {
        "name": "QCD_Pt-20To30_MuEnriched",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/QCD_Pt-20To30_MuEnrichedPt5_TuneCP5_13TeV-pythia8_2017.root",
        "xsec": 2526000,
        "color": 41,
    },
    "QCD_Pt-30To50_MuEnriched": {
        "name": "QCD_Pt-30To50_MuEnriched",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/QCD_Pt-30To50_MuEnrichedPt5_TuneCP5_13TeV-pythia8_2017.root",
        "xsec": 1362000,
        "color": 41,
    },
    "QCD_Pt-50To80_MuEnriched": {
        "name": "QCD_Pt-50To80_MuEnriched",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/QCD_Pt-50To80_MuEnrichedPt5_TuneCP5_13TeV-pythia8_2017.root",
        "xsec": 376600,
        "color": 41,
    },
    "QCD_Pt-80To120_MuEnriched": {
        "name": "QCD_Pt-80To120_MuEnriched",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/QCD_Pt-80To120_MuEnrichedPt5_TuneCP5_13TeV-pythia8_2017.root",
        "xsec": 88930,
        "color": 41,
    },
    "QCD_Pt-120To170_MuEnriched": {
        "name": "QCD_Pt-120To170_MuEnriched",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_13TeV-pythia8_2017.root",
        "xsec": 21230,
        "color": 41,
    },
    "QCD_Pt-170To300_MuEnriched": {
        "name": "QCD_Pt-170To300_MuEnriched",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/QCD_Pt-170To300_MuEnrichedPt5_TuneCP5_13TeV-pythia8_2017.root",
        "xsec": 7055,
        "color": 41,
    },
    "QCD_Pt-300To470_MuEnriched": {
        "name": "QCD_Pt-300To470_MuEnriched",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/QCD_Pt-300To470_MuEnrichedPt5_TuneCP5_13TeV-pythia8_2017.root",
        "xsec": 619.3,
        "color": 41,
    },
    "QCD_Pt-470To600_MuEnriched": {
        "name": "QCD_Pt-470To600_MuEnriched",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/QCD_Pt-470To600_MuEnrichedPt5_TuneCP5_13TeV-pythia8_2017.root",
        "xsec": 59.24,
        "color": 41,
    },
    "QCD_Pt-600To800_MuEnriched": {
        "name": "QCD_Pt-600To800_MuEnriched",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/QCD_Pt-600To800_MuEnrichedPt5_TuneCP5_13TeV-pythia8_2017.root",
        "xsec": 18.21,
        "color": 41,
    },
    "QCD_Pt-800To1000_MuEnriched": {
        "name": "QCD_Pt-800To1000_MuEnriched",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/QCD_Pt-800To1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8_2017.root",
        "xsec": 3.275, 
        "color": 41,
    },
    "DYJetsToLL_M10to50": {
        "name": "DYJetsToLL_M10to50",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8_2017.root",
        "xsec": 18610,
        "color": 30,
    },
    "DYJestsToLL_M-50": {
        "name": "DYJestsToLL_M-50",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8_2017.root",
        "xsec": 6077.22,
        "color": 30,
    },
    "WJetsToLNu": {
        "name": "WJetsToLNu",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8_2017.root",
        "xsec": 61526.7,
        "color": 43,
    },
    "TTG": {
        "name": "TTGJets",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_2017.root",
        "xsec": 3.697,
        "color": 3,
    },
    "TTZLLNuNu": {
        "name": "TTZToLLNuNu",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8_2017.root",
        "xsec": 0.2529,
        "color": 4,
    },
    "TTZLL": {
        "name": "TTZToLL",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8_2017.root",
        "xsec": 0.05324,
        "color": 44,
    },
    "TTW": {
        "name": "TTWJetsToLNu",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_2017.root",
        "xsec": 0.2043,
        "color": 5,
    },
    "TTTT": {
        "name": "TTTT",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/TTTT_TuneCP5_13TeV-amcatnlo-pythia8_2017.root",
        "xsec": 0.008213,
        "color": 45,
    },
    "tZq": {
        "name": "tZq_ll",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-amcatnlo-pythia8_2017.root",
        "xsec": 0.07358,
        "color": 6,
    },
    "sT": {
        "name": "sT top",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/ST_tW_top_5f_DS_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8_2017.root",
        "xsec": 33.67,
        "color": 46,
    },
    "sT_anti": {
        "name": "sT antitop",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/ST_tW_antitop_5f_DS_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8_2017.root",
        "xsec": 35.13,
        "color": 46,
    },
    "WWW": {
        "name": "WWW",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8_2017.root",
        "xsec": 0.2086,
        "color": 7,
    },
    "WWZ": {
        "name": "WWZ",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8_2017.root",
        "xsec": 0.1707,
        "color": 47,
    },
    # 	"WZ":
    # 		 {"name":"WZ",
    # 		 "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2017/WZ_TuneCP5_13TeV-pythia8_2017.root",
    # 		 "xsec":47.13,
    # 		 "color":8},
    "ZGToLLG": {
        "name": "ZGToLLG",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8_2017.root",
        "xsec": 55.48,
        "color": 9,
    },
    "WG": {
        "name": "WGToLNuG",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/WGToLNuG_01J_5f_PDFWeights_TuneCP5_13TeV-amcatnloFXFX-pythia8_2017.root",
        "xsec": 190.8,
        "color": 39,
    },
    "qqZZ": {
        "name": "qqZZ",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/ZZTo4L_TuneCP5_13TeV_powheg_pythia8_2017.root",
        "xsec": 1.325,
        "color": 12,
    },
    "ggZZ_2e2mu": {
        "name": "ggZZ_2e2mu",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/GluGluToContinToZZTo2e2mu_TuneCP5_13TeV-mcfm701-pythia8_2017.root",
        "xsec": 0.00319,
        "color": 13,
    },
    #"ggZZ_2e2nu": {
    #    "name": "ggZZ_2e2nu",
    #    "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/GluGluToContinToZZTo2e2nu_TuneCP5_13TeV-mcfm701-pythia8_2017.root",
    #    "xsec": 0.00319,
    #    "color": 13,
    #},
    "ggZZ_2e2tau": {
        "name": "ggZZ_2e2tau",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/GluGluToContinToZZTo2e2tau_TuneCP5_13TeV-mcfm701-pythia8_2017.root",
        "xsec": 0.00319,
        "color": 13,
    },
    "ggZZ_2mu2nu": {
        "name": "ggZZ_2mu2nu",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/GluGluToContinToZZTo2mu2nu_TuneCP5_13TeV-mcfm701-pythia8_2017.root",
        "xsec": 0.00319,
        "color": 13,
    },
    "ggZZ_2mu2tau": {
        "name": "ggZZ_2mu2tau",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/GluGluToContinToZZTo2mu2tau_TuneCP5_13TeV-mcfm701-pythia8_2017.root",
        "xsec": 0.00319,
        "color": 13,
    },
    "ggZZ_4e": {
        "name": "ggZZ_4e",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/GluGluToContinToZZTo4e_TuneCP5_13TeV-mcfm701-pythia8_2017.root",
        "xsec": 0.00159,
        "color": 13,
    },
    "ggZZ_4mu": {
        "name": "ggZZ_4mu",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/GluGluToContinToZZTo4mu_TuneCP5_13TeV-mcfm701-pythia8_2017.root",
        "xsec": 0.00159,
        "color": 13,
    },
    "ggZZ_4tau": {
        "name": "ggZZ_4tau",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/GluGluToContinToZZTo4tau_TuneCP5_13TeV-mcfm701-pythia8_2017.root",
        "xsec": 0.00159,
        "color": 13,
    },
    "WZG": {
        "name": "WZG",
        "path": "/cms/ldap_home/jwkim2/New_ccp/FakeLepton_weight_pseudo/2017/LLWA_WToLNu_4FS_TuneCP5_13TeV-amcatnlo-pythia8_2017.root",
        "xsec": 0.0384,
        "color": 2,
    },
}

