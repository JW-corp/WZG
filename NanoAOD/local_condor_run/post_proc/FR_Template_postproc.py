import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-f',dest='infile',help="if an input file is not provide, assume this is a crab job")
parser.add_argument('-d',dest='isdata',action='store_true',default=False)
parser.add_argument('-y', dest='year', default='2018', help='year')


#args = parser.parse_args()





from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.modules.FakeLep_FR_Template_Module import *

from PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2	   import *
from PhysicsTools.NanoAODTools.postprocessing.modules.eleRECOSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.eleIDSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.muonScaleResProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.muonIDISOSFProducer import *

parser = argparse.ArgumentParser(description='baseline selection')
parser.add_argument('-f', dest='file', default='', help='File input. In local mode it will be the filepath. In condor mode it will be the dataset name')
parser.add_argument('-m', dest='mode', default='local', help='runmode local/condor')
parser.add_argument('-y', dest='year', default='2018', help='year')
parser.add_argument('-d', dest='isdata',action='store_true',default=False)
parser.add_argument('-p', dest='period',default="B", help="Run period, only work for data")

## ---> Added by JW
parser.add_argument('-dataset_name', dest='dataset_name',default="B", help="Run period, only work for data")
## <-- Added by JW

args = parser.parse_args()

PrefCorrUL16_preVFP = lambda : PrefCorr(jetroot="L1PrefiringMaps.root", jetmapname="L1prefiring_jetptvseta_UL2016preVFP", photonroot="L1PrefiringMaps.root", photonmapname="L1prefiring_photonptvseta_UL2016preVFP", branchnames=["PrefireWeight","PrefireWeight_Up", "PrefireWeight_Down"])
PrefCorrUL16_postVFP = lambda : PrefCorr(jetroot="L1PrefiringMaps.root", jetmapname="L1prefiring_jetptvseta_UL2016postVFP", photonroot="L1PrefiringMaps.root", photonmapname="L1prefiring_photonptvseta_UL2016postVFP", branchnames=["PrefireWeight","PrefireWeight_Up", "PrefireWeight_Down"])
PrefCorrUL17 = lambda : PrefCorr(jetroot="L1PrefiringMaps.root", jetmapname="L1prefiring_jetptvseta_UL2017BtoF", photonroot="L1PrefiringMaps.root", photonmapname="L1prefiring_photonptvseta_UL2017BtoF", branchnames=["PrefireWeight","PrefireWeight_Up", "PrefireWeight_Down"])

if args.isdata:
	print("data"*20)
	if args.year == '2018':
		jetmetCorrector = createJMECorrector(isMC=False, dataYear="UL2018", runPeriod=args.period, metBranchName="MET")
		Modules = [muonScaleRes2018(),FRFakeLep_first_Template_Module(),jetmetCorrector(),FRFakeLeptonModule()]
	if args.year == '2017':
		jetmetCorrector = createJMECorrector(isMC=False, dataYear="UL2017", runPeriod=args.period, metBranchName="MET")
		Modules = [muonScaleRes2017(),FRFakeLep_first_Template_Module(),jetmetCorrector(),FRFakeLeptonModule()]
	if args.year == '2016':
		jetmetCorrector = createJMECorrector(isMC=False, dataYear="UL2016", runPeriod=args.period, metBranchName="MET")
		Modules = [muonScaleRes2016b(),FRFakeLep_first_Template_Module(),jetmetCorrector(),FRFakeLeptonModule_16()]
	if args.year == '2016_preVFP':
		jetmetCorrector = createJMECorrector(isMC=False, dataYear="UL2016_preVFP", runPeriod=args.period, metBranchName="MET")
		Modules = [muonScaleRes2016a(),FRFakeLep_first_Template_Module(),jetmetCorrector(),FRFakeLeptonModule_16()]
else:
	print("MC"*20)
	if args.year == '2018':
		jetmetCorrector = createJMECorrector(isMC=True, dataYear="UL2018", jesUncert="Total", metBranchName="MET", splitJER=False, applyHEMfix=True)
		Modules = [countHistogramsProducer(),muonScaleRes2018(),FRFakeLep_first_Template_Module(),puAutoWeight_2018(),muonIDISOSF2018(),eleRECOSF2018(),eleIDSF2018(),jetmetCorrector(),FRFakeLeptonModule()]
	if args.year == '2017':
		jetmetCorrector = createJMECorrector(isMC=True, dataYear="UL2017", jesUncert="Total", metBranchName="MET", splitJER=False)
		Modules = [countHistogramsProducer(),muonScaleRes2017(),FRFakeLep_first_Template_Module(),puAutoWeight_2017(),PrefCorrUL17(),muonIDISOSF2017(),eleRECOSF2017(),eleIDSF2017(),jetmetCorrector(),FRFakeLeptonModule()]
	if args.year == '2016':
		jetmetCorrector = createJMECorrector(isMC=True, dataYear="UL2016", jesUncert="Total", metBranchName="MET", splitJER=False)
		Modules = [countHistogramsProducer(),muonScaleRes2016b(),FRFakeLep_first_Template_Module(),puAutoWeight_2016(),PrefCorrUL16_postVFP(),muonIDISOSF2016(),eleRECOSF2016(),eleIDSF2016(),jetmetCorrector(),FRFakeLeptonModule_16()]
	if args.year == '2016_preVFP':
		jetmetCorrector = createJMECorrector(isMC=True, dataYear="UL2016_preVFP", jesUncert="Total", metBranchName="MET", splitJER=False)
		Modules = [countHistogramsProducer(),muonScaleRes2016a(),FRFakeLep_first_Template_Module(),puAutoWeight_2016(),PrefCorrUL16_preVFP(),muonIDISOSF2016_preVFP(),eleRECOSF2016_preVFP(),eleIDSF2016_preVFP(),jetmetCorrector(),FRFakeLeptonModule_16()]

if args.file:

	infilelist = []
	jsoninput = None
	fwkjobreport = False

	if args.mode == 'condor':
		import DAS_filesearch as search
		infilelist.append(search.getValidSite(args.file)+args.file) 
	else:
		infilelist = [args.file]

else:

	from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
	infilelist = inputFiles()
	jsoninput = runsAndLumis()
	fwkjobreport = True

if args.isdata and args.year.startswith('2016'):
	import FWCore.PythonUtilities.LumiList as LumiList
	import FWCore.ParameterSet.Config as cms

	lumisToProcess = cms.untracked.VLuminosityBlockRange( LumiList.LumiList(filename="/x5/cms/jwkim/gitdir/JWCorp/JW_analysis/for_graduation2022/CMSSW_10_6_19/src/PhysicsTools/NanoAODTools/nanoAOD-WVG/local_condor_run/goldenjson/2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt").getCMSSWString().split(',') )

	runsAndLumis_special = {}
	for l in lumisToProcess:
		if "-" in l:
			start, stop = l.split("-")
			rstart, lstart = start.split(":")
			rstop, lstop = stop.split(":")
		else:
			rstart, lstart = l.split(":")
			rstop, lstop = l.split(":")
		if rstart != rstop:
			raise Exception(
				"Cannot convert '%s' to runs and lumis json format" % l)
		if rstart not in runsAndLumis_special:
			runsAndLumis_special[rstart] = []
		runsAndLumis_special[rstart].append([int(lstart), int(lstop)])
	jsoninput = runsAndLumis_special

## ---> Added by JW
# Check weather the output directory exists
isExist = os.path.exists(args.dataset_name)
# If not.. mkdir
if not isExist:
		os.makedirs(args.dataset_name)
## <--- Added by JW

#p=PostProcessor(".",infilelist,
p=PostProcessor(args.dataset_name,infilelist,  # new: specify the directory following name of dataset
				branchsel="FR_keep_and_drop.txt",
				modules = Modules,
				provenance=True,
				justcount=False,
				noOut=False,
				fwkJobReport=fwkjobreport, 
				jsonInput=jsoninput, 
				outputbranchsel = "FR_output_branch_selection.txt")

p.run()
