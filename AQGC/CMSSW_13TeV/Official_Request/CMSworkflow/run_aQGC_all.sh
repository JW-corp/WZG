#!/bin/bash

# -- I/O
GRID_PATH=$1
EVENTS=$2


# Make working dir
TOPDIR=$PWD
FNAME=`echo $GRID_PATH | awk -F '/' '{print $11}' | awk -F '_sl' '{print $1}'`
mkdir $FNAME
FIRST_DIR=$PWD


cp /x5/cms/jwkim/Generator/aQGC_CMS_workFlow/BatchJob/tools/NeutrinoE-10/filepath_Neutrino_E-10_gun_2016Pre.txt /x5/cms/jwkim/Generator/aQGC_CMS_workFlow/BatchJob/tools/randomizeSeeds.py $FNAME
cd $FNAME


echo GridPack: $GRID_PATH
echo N evts: $EVENTS

# -- CMSSET
export SCRAM_ARCH=slc7_amd64_gcc700
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
echo "$VO_CMS_SW_DIR $SCRAM_ARCH"
source $VO_CMS_SW_DIR/cmsset_default.sh
voms-proxy-init -voms cms -valid 190:00

# -- Network
export SSL_CERT_DIR='/etc/grid-security/certificates'
export X509_USER_PROXY=/tmp/x509up_u538
#source /cvmfs/cms.cern.ch/crab3/crab.sh
#crab submit -c crabConfig.py


# -- CMSSW INSTALL
if [ -r CMSSW_10_6_22/src ] ; then
  echo release CMSSW_10_6_22 already exists
else
  scram p CMSSW CMSSW_10_6_22
fi
cd CMSSW_10_6_22/src
eval `scram runtime -sh`

# -- You are in src dir

# -Reference fragment file
#curl -s -k https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/SMP-RunIIFall18wmLHEGS-00112 --retry 3 --create-dirs -o Configuration/GenProduction/python/SMP-RunIIFall18wmLHEGS-00112-fragment.py


# 1.. Start fragment run

# -Write fragment file directly
mkdir -p Configuration/GenProduction/python
cat << EOF >> Configuration/GenProduction/python/SMP-RunIISummer20UL16wmLHEGENAPV-00xxx-fragment.py
import FWCore.ParameterSet.Config as cms

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring('/x4/cms/dylee/NanoAODTool/aQGC/genproductions/bin/MadGraph5_aMCatNLO/tar_storage/FM0_1_10_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz'),
    nEvents = cms.untracked.uint32(${EVENTS}),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)


from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        pythia8PSweightsSettingsBlock,
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'pythia8PSweightsSettings',
                                    )
    )
)
ProductionFilterSequence = cms.Sequence(generator)
EOF
scram b
cp ../../randomizeSeeds.py Configuration/GenProduction/python
cd -

# You are in working dir
ls -alh
echo "1... Start frament run"
start=$(date +%s)
cmsDriver.py Configuration/GenProduction/python/SMP-RunIISummer20UL16wmLHEGENAPV-00xxx-fragment.py \
            --python_filename SMP-RunIISummer20UL16wmLHEGENAPV-00xxx_1_cfg.py \
            --eventcontent RAWSIM,LHE \
            --customise Configuration/DataProcessing/Utils.addMonitoring,Configuration/GenProduction/randomizeSeeds.randomizeSeeds \
            --datatier GEN,LHE \
			--fileout file:SMP-RunIISummer20UL16wmLHEGENAPV-00xxx.root \
            --conditions 106X_mcRun2_asymptotic_preVFP_v8 \
            --beamspot Realistic25ns13TeV2016Collision \
            --step LHE,GEN \
            --geometry DB:Extended \
            --era Run2_2016_HIPM \
            --no_exec --mc -n $EVENTS || exit $? ;

cmsRun SMP-RunIISummer20UL16wmLHEGENAPV-00xxx_1_cfg.py
end=$(date +%s)
echo ">>>>>>>>>>>>>>>>>>>>> Elapsed Time for step1 LHE GEN: $(($end-$start)) seconds"

# 2.. Start SIM
if [ -r CMSSW_10_6_17_patch1/src ] ; then
  echo release CMSSW_10_6_17_patch1 already exists
else
  scram p CMSSW CMSSW_10_6_17_patch1
fi
cd CMSSW_10_6_17_patch1/src
eval `scram runtime -sh`
scram b
cd ../..
start=$(date +%s)
cmsDriver.py  --python_filename SMP-RunIISummer20UL16SIMAPV-00xxx_1_cfg.py \
            --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring \
            --datatier GEN-SIM \
            --fileout file:SMP-RunIISummer20UL16SIMAPV-00xxx.root \
            --conditions 106X_mcRun2_asymptotic_preVFP_v8 \
            --beamspot Realistic25ns13TeV2016Collision \
            --step SIM \
            --geometry DB:Extended \
            --filein file:SMP-RunIISummer20UL16wmLHEGENAPV-00xxx.root \
            --era Run2_2016_HIPM \
            --runUnscheduled \
            --no_exec --mc -n $EVENTS || exit $? ;
cmsRun SMP-RunIISummer20UL16SIMAPV-00xxx_1_cfg.py
end=$(date +%s)
echo ">>>>>>>>>>>>>>>>>>>>> Elapsed Time for step2 SIM: $(($end-$start)) seconds"

# 3.. Start DIGI
start=$(date +%s)
cmsDriver.py  --python_filename SMP-RunIISummer20UL16DIGIPremixAPV-00xxx_1_cfg.py \
            --eventcontent PREMIXRAW \
            --customise Configuration/DataProcessing/Utils.addMonitoring \
            --datatier GEN-SIM-DIGI \
            --fileout file:SMP-RunIISummer20UL16DIGIPremixAPV-00xxx.root \
            --pileup_input "filelist:filepath_Neutrino_E-10_gun_2016Pre.txt" \
            --conditions 106X_mcRun2_asymptotic_preVFP_v8 \
            --step DIGI,DATAMIX,L1,DIGI2RAW \
            --procModifiers premix_stage2 \
            --geometry DB:Extended \
            --filein file:SMP-RunIISummer20UL16SIMAPV-00xxx.root \
            --datamix PreMix \
            --era Run2_2016_HIPM \
            --runUnscheduled \
            --no_exec --mc -n $EVENTS || exit $? ;
cmsRun SMP-RunIISummer20UL16DIGIPremixAPV-00xxx_1_cfg.py
end=$(date +%s)
echo ">>>>>>>>>>>>>>>>>>>>> Elapsed Time for step3 DIGI: $(($end-$start)) seconds"

# 4.. Start HLT
if [ -r CMSSW_8_0_33_UL/src ] ; then
  echo release CMSSW_8_0_33_UL already exists
else
  scram p CMSSW CMSSW_8_0_33_UL
fi
cd CMSSW_8_0_33_UL/src
eval `scram runtime -sh`
scram b
cd ../..

start=$(date +%s)
cmsDriver.py  --python_filename SMP-RunIISummer20UL16HLTAPV-00xxx_1_cfg.py \
            --eventcontent RAWSIM \
            --outputCommand "keep *_mix_*_*,keep *_genPUProtons_*_*" \
            --customise Configuration/DataProcessing/Utils.addMonitoring \
            --datatier GEN-SIM-RAW \
            --inputCommands "keep *","drop *_*_BMTF_*","drop *PixelFEDChannel*_*_*_*" \
            --fileout file:SMP-RunIISummer20UL16HLTAPV-00xxx.root \
            --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 \
            --customise_commands 'process.source.bypassVersionCheck = cms.untracked.bool(True)' \
            --step HLT:25ns15e33_v4 \
			--geometry DB:Extended \
            --filein file:SMP-RunIISummer20UL16DIGIPremixAPV-00xxx.root \
            --era Run2_2016 \
            --no_exec --mc -n $EVENTS || exit $? ;
cmsRun SMP-RunIISummer20UL16HLTAPV-00xxx_1_cfg.py
end=$(date +%s)
echo ">>>>>>>>>>>>>>>>>>>>> Elapsed Time for step4 HLT: $(($end-$start)) seconds"


# 5.. Start RECO
if [ -r CMSSW_10_6_17_patch1/src ] ; then
  echo release CMSSW_10_6_17_patch1 already exists
else
  scram p CMSSW CMSSW_10_6_17_patch1
fi
cd CMSSW_10_6_17_patch1/src
eval `scram runtime -sh`
scram b
cd ../..
start=$(date +%s)
cmsDriver.py  --python_filename SMP-RunIISummer20UL16RECOAPV-00xxx_1_cfg.py \
            --eventcontent AODSIM \
            --customise Configuration/DataProcessing/Utils.addMonitoring \
            --datatier AODSIM \
            --fileout file:SMP-RunIISummer20UL16RECOAPV-00xxx.root \
            --conditions 106X_mcRun2_asymptotic_preVFP_v8 \
            --step RAW2DIGI,L1Reco,RECO,RECOSIM \
            --geometry DB:Extended \
            --filein file:SMP-RunIISummer20UL16HLTAPV-00xxx.root \
            --era Run2_2016_HIPM \
            --runUnscheduled \
            --no_exec --mc -n $EVENTS || exit $? ;
cmsRun SMP-RunIISummer20UL16RECOAPV-00xxx_1_cfg.py
end=$(date +%s)
echo ">>>>>>>>>>>>>>>>>>>>> Elapsed Time for step4 RECO : $(($end-$start)) seconds"


# 6.. Start MINIAOD
if [ -r CMSSW_10_6_25/src ] ; then
  echo release CMSSW_10_6_25 already exists
else
  scram p CMSSW CMSSW_10_6_25
fi
cd CMSSW_10_6_25/src
eval `scram runtime -sh`
scram b
cd ../..
start=$(date +%s)
cmsDriver.py  --python_filename SMP-RunIISummer20UL16MiniAODAPVv2-00xxx_1_cfg.py \
            --eventcontent MINIAODSIM \
            --customise Configuration/DataProcessing/Utils.addMonitoring \
            --datatier MINIAODSIM \
            --fileout file:SMP-RunIISummer20UL16MiniAODAPVv2-00xxx.root \
            --conditions 106X_mcRun2_asymptotic_preVFP_v11 \
            --step PAT \
            --procModifiers run2_miniAOD_UL \
            --geometry DB:Extended \
            --filein file:SMP-RunIISummer20UL16RECOAPV-00xxx.root \
            --era Run2_2016_HIPM \
            --runUnscheduled \
            --no_exec --mc -n $EVENTS || exit $? ;

cmsRun SMP-RunIISummer20UL16MiniAODAPVv2-00xxx_1_cfg.py
end=$(date +%s)
echo ">>>>>>>>>>>>>>>>>>>>> Elapsed Time for step5 MINIAOD: $(($end-$start)) seconds"


# 7.. Start NanoAOD
if [ -r CMSSW_10_6_26/src ] ; then
  echo release CMSSW_10_6_26 already exists
else
  scram p CMSSW CMSSW_10_6_26
fi
cd CMSSW_10_6_26/src
eval `scram runtime -sh`
scram b
cd ../..
start=$(date +%s)
cmsDriver.py  --python_filename SMP-RunIISummer20UL16NanoAODAPVv9-00xxx_1_cfg.py \
            --eventcontent NANOEDMAODSIM \
            --customise Configuration/DataProcessing/Utils.addMonitoring \
            --datatier NANOAODSIM \
            --fileout file:SMP-RunIISummer20UL16NanoAODAPVv9-00xxx.root \
            --conditions 106X_mcRun2_asymptotic_preVFP_v11 \
            --step NANO \
            --filein file:SMP-RunIISummer20UL16MiniAODAPVv2-00xxx.root \
            --era Run2_2016_HIPM,run2_nanoAOD_106Xv2 \
            --no_exec --mc -n $EVENTS || exit $? ;

sed -i -e 's/PoolOutputModule/NanoAODOutputModule/g' SMP-RunIISummer20UL16NanoAODAPVv9-00xxx_1_cfg.py
cmsRun SMP-RunIISummer20UL16NanoAODAPVv9-00xxx_1_cfg.py
end=$(date +%s)
echo ">>>>>>>>>>>>>>>>>>>>> Elapsed Time for step6 NanoAOD: $(($end-$start)) seconds"




