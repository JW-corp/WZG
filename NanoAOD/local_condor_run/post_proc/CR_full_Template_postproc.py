#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import countHistogramsProducer
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2	   import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.eleRECOSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.eleIDSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.muonScaleResProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.muonIDISOSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CR_full_Template_Module import *

import argparse
import re
import optparse

PrefCorrUL16_preVFP = lambda : PrefCorr(jetroot="L1PrefiringMaps.root", jetmapname="L1prefiring_jetptvseta_UL2016preVFP", photonroot="L1PrefiringMaps.root", photonmapname="L1prefiring_photonptvseta_UL2016preVFP", branchnames=["PrefireWeight","PrefireWeight_Up", "PrefireWeight_Down"])
PrefCorrUL16_postVFP = lambda : PrefCorr(jetroot="L1PrefiringMaps.root", jetmapname="L1prefiring_jetptvseta_UL2016postVFP", photonroot="L1PrefiringMaps.root", photonmapname="L1prefiring_photonptvseta_UL2016postVFP", branchnames=["PrefireWeight","PrefireWeight_Up", "PrefireWeight_Down"])
PrefCorrUL17 = lambda : PrefCorr(jetroot="L1PrefiringMaps.root", jetmapname="L1prefiring_jetptvseta_UL2017BtoF", photonroot="L1PrefiringMaps.root", photonmapname="L1prefiring_photonptvseta_UL2017BtoF", branchnames=["PrefireWeight","PrefireWeight_Up", "PrefireWeight_Down"])

parser = argparse.ArgumentParser(description='fake photon CR full template production')
parser.add_argument('-f', dest='file', default='', help='File input. In local mode it will be the filepath. In condor mode it will be the dataset name')
parser.add_argument('-m', dest='mode', default='local', help='runmode local/condor')
parser.add_argument('-y', dest='year', default='2018', help='year')
parser.add_argument('-d', dest='isdata',action='store_true',default=False)
parser.add_argument('-p', dest='period',default="B", help="Run period, only work for data")
parser.add_argument('-s', dest='preskim',default='', help="preskim json input")


## ---> Added by JW
parser.add_argument('-dataset_name', dest='dataset_name',default="B", help="Run period, only work for data")
args = parser.parse_args()
## <-- Added by JW



if args.isdata:
	if args.year == '2018':
		jetmetCorrector = createJMECorrector(isMC=False, dataYear="UL2018", runPeriod=args.period, metBranchName="MET")
		Modules = [countHistogramsProducer(),jetmetCorrector(),CR_FakePhotonFullModule_18()]
	if args.year == '2017':
		jetmetCorrector = createJMECorrector(isMC=False, dataYear="UL2017", runPeriod=args.period, metBranchName="MET")
		Modules = [countHistogramsProducer(),jetmetCorrector(),CR_FakePhotonFullModule_17()]
	if args.year == '2016':
		jetmetCorrector = createJMECorrector(isMC=False, dataYear="UL2016", runPeriod=args.period, metBranchName="MET")
		Modules = [countHistogramsProducer(),jetmetCorrector(),CR_FakePhotonFullModule_16()]
	if args.year == '2016_preVFP':
		jetmetCorrector = createJMECorrector(isMC=False, dataYear="UL2016_preVFP", runPeriod=args.period, metBranchName="MET")
		Modules = [countHistogramsProducer(),jetmetCorrector(),CR_FakePhotonFullModule_16preVFP()]



else:
	if args.year == '2018':
		jetmetCorrector = createJMECorrector(isMC=True, dataYear="UL2018", jesUncert="Total", metBranchName="MET", splitJER=False, applyHEMfix=True)
		Modules = [countHistogramsProducer(),jetmetCorrector(),muonScaleRes2018(),muonIDISOSF2018(),eleRECOSF2018(),eleIDSF2018(),CR_FakePhotonFullModule_18(),puWeight_2018()]
	if args.year == '2017':
		jetmetCorrector = createJMECorrector(isMC=True, dataYear="UL2017", jesUncert="Total", metBranchName="MET", splitJER=False)
		Modules = [countHistogramsProducer(),PrefCorrUL17(),muonScaleRes2017(),muonIDISOSF2017(),eleRECOSF2017(),eleIDSF2017(),jetmetCorrector(),CR_FakePhotonFullModule_17(),puWeight_2017()]
	if args.year == '2016':
		jetmetCorrector = createJMECorrector(isMC=True, dataYear="UL2016", jesUncert="Total", metBranchName="MET", splitJER=False)
		Modules = [countHistogramsProducer(),PrefCorrUL16_postVFP(),muonScaleRes2016b(),muonIDISOSF2016(),eleRECOSF2016(),eleIDSF2016(),jetmetCorrector(),CR_FakePhotonFullModule_16(),puWeight_2016()]
	if args.year == '2016_preVFP':
		jetmetCorrector = createJMECorrector(isMC=True, dataYear="UL2016_preVFP", jesUncert="Total", metBranchName="MET", splitJER=False)
		Modules = [countHistogramsProducer(),PrefCorrUL16_preVFP(),muonScaleRes2016a(),muonIDISOSF2016_preVFP(),eleRECOSF2016_preVFP(),eleIDSF2016_preVFP(),jetmetCorrector(),CR_FakePhotonFullModule_16preVFP(),puWeight_2016()]

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

if args.preskim:
	from preselect_help import preselect_json_load
	preselection = preselect_json_load(args.preskim)
else:
	preselection = None

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
print("processing..: ",infilelist)
# Check weather the output directory exists
isExist = os.path.exists(args.dataset_name)
# If not.. mkdir
if not isExist:
	os.makedirs(args.dataset_name)
## <--- Added by JW


#p=PostProcessor(".",infilelist,
p=PostProcessor(args.dataset_name,infilelist,  # new: specify the directory following name of dataset
				branchsel="CR_full_keep_and_drop.txt",
				cut=preselection,
				modules=Modules,
				justcount=False,
				noOut=False,
				fwkJobReport=fwkjobreport, 
				jsonInput=jsoninput, 
				provenance=True,
				outputbranchsel="CR_full_output_branch_selection.txt",
				)
p.run()
