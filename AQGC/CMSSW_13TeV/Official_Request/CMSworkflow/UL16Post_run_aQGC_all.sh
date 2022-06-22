#!/bin/bash

# -- I/O
GRID_PATH=`readlink -e $2`
EVENTS=$3

# Only for Condor Run
Cluster=$4
Process=$5
FILE_TAG=${Cluster}_${Process}
NANOAOD_DIR_LOC=/hcp/home/jwkim2/2016Pre/CMSSW_10_6_26/src
PUMIX=`readlink -e filepath_Neutrino_E-10_gun_2016Post.txt`



echo GridPack: $GRID_PATH
echo N evts: $EVENTS
echo FILE_TAG: $FILE_TAG


# -- Initialize path
TOPDIR=${PWD}
[ -d condorOut ] || mkdir condorOut
echo "-----> Working directory: ${TOPDIR}"
ls -alh


# -- voms proxy set
#export X509_USER_PROXY=${TopDir}/$1
voms-proxy-info 

# -- CMSSET
export SCRAM_ARCH=slc7_amd64_gcc700
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
echo "$VO_CMS_SW_DIR $SCRAM_ARCH"
source $VO_CMS_SW_DIR/cmsset_default.sh




# -- 1 step: LHE GEN 
echo "---------------> Start step1: LHE GEN ------------"
if [ -r CMSSW_10_6_22/src ] ; then
  echo release CMSSW_10_6_22 already exists
else
  scram p CMSSW CMSSW_10_6_22
fi
cd CMSSW_10_6_22/src
eval `scram runtime -sh`

#Reference fragment file
#curl -s -k https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/SMP-RunIIFall18wmLHEGS-00112 --retry 3 --create-dirs -o Configuration/GenProduction/python/SMP-RunIIFall18wmLHEGS-00112-fragment.py

# -Write fragment file directly
if [ -r Configuration/GenProduction/python ] ; then
	echo "Configuration/GenProduction/python already exists"
else
mkdir -p Configuration/GenProduction/python
cat << EOF >> Configuration/GenProduction/python/SMP-RunIISummer20UL16wmLHEGENAPV-00xxx-fragment.py
import FWCore.ParameterSet.Config as cms

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring('${GRID_PATH}'),
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
fi
cp ${TOPDIR}/randomizeSeeds.py Configuration/GenProduction/python
scram b
cd $TOPDIR
ls -alh


echo "1... Start frament run"
if [ -r SMP-RunIISummer20UL16wmLHEGENAPV-00xxx_1_cfg_${FILE_TAG}.py ] ; then
	echo "SMP-RunIISummer20UL16wmLHEGENAPV-00xxx_1_cfg_${FILE_TAG}.py already exist" 
else
cmsDriver.py Configuration/GenProduction/python/SMP-RunIISummer20UL16wmLHEGENAPV-00xxx-fragment.py \
            --python_filename SMP-RunIISummer20UL16wmLHEGENAPV-00xxx_1_cfg_${FILE_TAG}.py \
            --eventcontent RAWSIM,LHE \
            --customise Configuration/DataProcessing/Utils.addMonitoring,Configuration/GenProduction/randomizeSeeds.randomizeSeeds \
            --datatier GEN,LHE \
			--fileout file:SMP-RunIISummer20UL16wmLHEGENAPV-00xxx_${FILE_TAG}.root \
            --conditions 106X_mcRun2_asymptotic_v13  \
            --beamspot Realistic25ns13TeV2016Collision \
            --step LHE,GEN \
            --geometry DB:Extended \
            --era Run2_2016 \
            --no_exec --mc -n $EVENTS || exit $? ;
fi
start=$(date +%s)
cmsRun SMP-RunIISummer20UL16wmLHEGENAPV-00xxx_1_cfg_${FILE_TAG}.py
end=$(date +%s)
echo ">>>>>>>>>>>>>>>>>>>>> Elapsed Time for step1 LHE GEN: $(($end-$start)) seconds"
cd $TOPDIR
ls -alh



# 2.. Start SIM
echo "---------------> Start step2: SIM ------------"
if [ -r CMSSW_10_6_17_patch1/src ] ; then
  echo release CMSSW_10_6_17_patch1 already exists
else
  scram p CMSSW CMSSW_10_6_17_patch1
fi
cd CMSSW_10_6_17_patch1/src
eval `scram runtime -sh`
scram b
cd $TOPDIR


if [ -r SMP-RunIISummer20UL16SIMAPV-00xxx_1_cfg_${FILE_TAG}.py ] ; then
	echo "SMP-RunIISummer20UL16SIMAPV-00xxx_1_cfg_${FILE_TAG}.py already exist" 
else
cmsDriver.py  --python_filename SMP-RunIISummer20UL16SIMAPV-00xxx_1_cfg_${FILE_TAG}.py \
            --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring \
            --datatier GEN-SIM \
            --fileout file:SMP-RunIISummer20UL16SIMAPV-00xxx_${FILE_TAG}.root \
            --conditions 106X_mcRun2_asymptotic_v13  \
            --beamspot Realistic25ns13TeV2016Collision \
            --step SIM \
            --geometry DB:Extended \
            --filein file:SMP-RunIISummer20UL16wmLHEGENAPV-00xxx_${FILE_TAG}.root \
            --era Run2_2016 \
            --runUnscheduled \
            --no_exec --mc -n $EVENTS || exit $? ;
fi
start=$(date +%s)
cmsRun SMP-RunIISummer20UL16SIMAPV-00xxx_1_cfg_${FILE_TAG}.py
end=$(date +%s)
echo ">>>>>>>>>>>>>>>>>>>>> Elapsed Time for step2 SIM: $(($end-$start)) seconds"
ls -alh



# 3.. Start DIGI



echo "---------------> Start step3: DIGI ------------"
if [ -r SMP-RunIISummer20UL16DIGIPremixAPV-00xxx_1_cfg_${FILE_TAG}.py ] ; then
	echo "SMP-RunIISummer20UL16DIGIPremixAPV-00xxx_1_cfg_${FILE_TAG}.py already exist" 
else
cmsDriver.py  --python_filename SMP-RunIISummer20UL16DIGIPremixAPV-00xxx_1_cfg_${FILE_TAG}.py \
            --eventcontent PREMIXRAW \
            --customise Configuration/DataProcessing/Utils.addMonitoring \
            --datatier GEN-SIM-DIGI \
            --fileout file:SMP-RunIISummer20UL16DIGIPremixAPV-00xxx_${FILE_TAG}.root \
            --pileup_input filelist:${PUMIX} \
            --conditions 106X_mcRun2_asymptotic_v13  \
            --step DIGI,DATAMIX,L1,DIGI2RAW \
            --procModifiers premix_stage2 \
            --geometry DB:Extended \
            --filein file:SMP-RunIISummer20UL16SIMAPV-00xxx_${FILE_TAG}.root \
            --datamix PreMix \
            --era Run2_2016 \
            --runUnscheduled \
            --no_exec --mc -n $EVENTS || exit $? ;
fi

start=$(date +%s)
cmsRun SMP-RunIISummer20UL16DIGIPremixAPV-00xxx_1_cfg_${FILE_TAG}.py
end=$(date +%s)
echo ">>>>>>>>>>>>>>>>>>>>> Elapsed Time for step3 DIGI: $(($end-$start)) seconds"
ls -alh




# 4.. Start HLT
echo "---------------> Start step4: HLT ------------"
if [ -r CMSSW_8_0_33_UL/src ] ; then
  echo release CMSSW_8_0_33_UL already exists
else
  scram p CMSSW CMSSW_8_0_33_UL
fi
cd CMSSW_8_0_33_UL/src
eval `scram runtime -sh`
scram b
cd $TOPDIR

if [ -r SMP-RunIISummer20UL16HLTAPV-00xxx_1_cfg_${FILE_TAG}.py ] ; then
	echo "SMP-RunIISummer20UL16HLTAPV-00xxx_1_cfg_${FILE_TAG}.py already exist" 
else
cmsDriver.py  --python_filename SMP-RunIISummer20UL16HLTAPV-00xxx_1_cfg_${FILE_TAG}.py \
            --eventcontent RAWSIM \
            --outputCommand "keep *_mix_*_*,keep *_genPUProtons_*_*" \
            --customise Configuration/DataProcessing/Utils.addMonitoring \
            --datatier GEN-SIM-RAW \
            --inputCommands "keep *","drop *_*_BMTF_*","drop *PixelFEDChannel*_*_*_*" \
            --fileout file:SMP-RunIISummer20UL16HLTAPV-00xxx_${FILE_TAG}.root \
            --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 \
            --customise_commands 'process.source.bypassVersionCheck = cms.untracked.bool(True)' \
            --step HLT:25ns15e33_v4 \
			--geometry DB:Extended \
            --filein file:SMP-RunIISummer20UL16DIGIPremixAPV-00xxx_${FILE_TAG}.root \
            --era Run2_2016 \
            --no_exec --mc -n $EVENTS || exit $? ;
fi

start=$(date +%s)
cmsRun SMP-RunIISummer20UL16HLTAPV-00xxx_1_cfg_${FILE_TAG}.py
end=$(date +%s)
echo ">>>>>>>>>>>>>>>>>>>>> Elapsed Time for step4 HLT: $(($end-$start)) seconds"
ls -alh




# 5.. Start RECO
echo "---------------> Start step5: RECO ------------"
if [ -r CMSSW_10_6_17_patch1/src ] ; then
  echo release CMSSW_10_6_17_patch1 already exists
else
  scram p CMSSW CMSSW_10_6_17_patch1
fi
cd CMSSW_10_6_17_patch1/src
eval `scram runtime -sh`
scram b
cd $TOPDIR


if [ -r SMP-RunIISummer20UL16RECOAPV-00xxx_1_cfg_${FILE_TAG}.py ] ; then
    echo "SMP-RunIISummer20UL16RECOAPV-00xxx_1_cfg_${FILE_TAG}.py already exist"
else
cmsDriver.py  --python_filename SMP-RunIISummer20UL16RECOAPV-00xxx_1_cfg_${FILE_TAG}.py \
            --eventcontent AODSIM \
            --customise Configuration/DataProcessing/Utils.addMonitoring \
            --datatier AODSIM \
            --fileout file:SMP-RunIISummer20UL16RECOAPV-00xxx_${FILE_TAG}.root \
            --conditions 106X_mcRun2_asymptotic_v13  \
            --step RAW2DIGI,L1Reco,RECO,RECOSIM \
            --geometry DB:Extended \
            --filein file:SMP-RunIISummer20UL16HLTAPV-00xxx_${FILE_TAG}.root \
            --era Run2_2016 \
            --runUnscheduled \
            --no_exec --mc -n $EVENTS || exit $? ;
fi

start=$(date +%s)
cmsRun SMP-RunIISummer20UL16RECOAPV-00xxx_1_cfg_${FILE_TAG}.py
end=$(date +%s)
echo ">>>>>>>>>>>>>>>>>>>>> Elapsed Time for step5 RECO : $(($end-$start)) seconds"
ls -alh




# 6.. Start MINIAOD
echo "---------------> Start step6: MINIAOD ------------"
if [ -r CMSSW_10_6_25/src ] ; then
  echo release CMSSW_10_6_25 already exists
else
  scram p CMSSW CMSSW_10_6_25
fi
cd CMSSW_10_6_25/src
eval `scram runtime -sh`
scram b
cd $TOPDIR

if [ -r SMP-RunIISummer20UL16MiniAODAPVv2-00xxx_1_cfg_${FILE_TAG}.py ] ; then
    echo "SMP-RunIISummer20UL16MiniAODAPVv2-00xxx_1_cfg_${FILE_TAG}.py already exist"
else
cmsDriver.py  --python_filename SMP-RunIISummer20UL16MiniAODAPVv2-00xxx_1_cfg_${FILE_TAG}.py \
            --eventcontent MINIAODSIM \
            --customise Configuration/DataProcessing/Utils.addMonitoring \
            --datatier MINIAODSIM \
            --fileout file:SMP-RunIISummer20UL16MiniAODAPVv2-00xxx_${FILE_TAG}.root \
            --conditions 106X_mcRun2_asymptotic_v17  \
            --step PAT \
            --procModifiers run2_miniAOD_UL \
            --geometry DB:Extended \
            --filein file:SMP-RunIISummer20UL16RECOAPV-00xxx_${FILE_TAG}.root \
            --era Run2_2016 \
            --runUnscheduled \
            --no_exec --mc -n $EVENTS || exit $? ;
fi
start=$(date +%s)
cmsRun SMP-RunIISummer20UL16MiniAODAPVv2-00xxx_1_cfg_${FILE_TAG}.py
end=$(date +%s)
echo ">>>>>>>>>>>>>>>>>>>>> Elapsed Time for step6 MINIAOD: $(($end-$start)) seconds"
ls -alh




# 7.. Start NanoAOD
echo "---------------> Start step7: NANOAOD ------------"

cd $NANOAOD_DIR_LOC
ls -alh
pwd
eval `scram runtime -sh`
cd $TOPDIR

cmsDriver.py  --python_filename SMP-RunIISummer20UL16NanoAODAPVv9-00xxx_1_cfg_${FILE_TAG}.py \
            --eventcontent NANOEDMAODSIM \
            --customise Configuration/DataProcessing/Utils.addMonitoring \
            --datatier NANOAODSIM \
            --fileout file:SMP-RunIISummer20UL16NanoAODAPVv9-00xxx_${FILE_TAG}.root \
            --conditions 106X_mcRun2_asymptotic_v17 \
            --step NANO \
            --filein file:SMP-RunIISummer20UL16MiniAODAPVv2-00xxx_${FILE_TAG}.root \
            --era Run2_2016,run2_nanoAOD_106Xv2 \
            --no_exec --mc -n $EVENTS || exit $? ;
sed -i -e 's/PoolOutputModule/NanoAODOutputModule/g' SMP-RunIISummer20UL16NanoAODAPVv9-00xxx_1_cfg_${FILE_TAG}.py


export HOME=$TOPDIR
start=$(date +%s)
cmsRun SMP-RunIISummer20UL16NanoAODAPVv9-00xxx_1_cfg_${FILE_TAG}.py
end=$(date +%s)
echo ">>>>>>>>>>>>>>>>>>>>> Elapsed Time for step7 NanoAOD: $(($end-$start)) seconds"
ls -alh

echo "Congratulation! Finished! ... Now moving outputs to condorOut"


#mv SMP-RunIISummer20UL16wmLHEGENAPV-00xxx_1_cfg_${FILE_TAG}.py condorOut
mv SMP-RunIISummer20UL16wmLHEGENAPV-00xxx_${FILE_TAG}.root condorOut
#mv SMP-RunIISummer20UL16SIMAPV-00xxx_1_cfg_${FILE_TAG}.py condorOut
#mv SMP-RunIISummer20UL16SIMAPV-00xxx_${FILE_TAG}.root condorOut
#mv SMP-RunIISummer20UL16DIGIPremixAPV-00xxx_${FILE_TAG}.root condorOut
#mv SMP-RunIISummer20UL16DIGIPremixAPV-00xxx_1_cfg_${FILE_TAG}.py condorOut
#mv SMP-RunIISummer20UL16HLTAPV-00xxx_1_cfg_${FILE_TAG}.py condorOut
#mv SMP-RunIISummer20UL16HLTAPV-00xxx_${FILE_TAG}.root condorOut
#mv SMP-RunIISummer20UL16RECOAPV-00xxx_${FILE_TAG}.root condorOut
#mv SMP-RunIISummer20UL16RECOAPV-00xxx_1_cfg_${FILE_TAG}.py condorOut
#mv SMP-RunIISummer20UL16MiniAODAPVv2-00xxx_${FILE_TAG}.root condorOut
#mv SMP-RunIISummer20UL16MiniAODAPVv2-00xxx_1_cfg_${FILE_TAG}.py condorOut
mv SMP-RunIISummer20UL16NanoAODAPVv9-00xxx_${FILE_TAG}.root condorOut
#mv SMP-RunIISummer20UL16NanoAODAPVv9-00xxx_1_cfg_${FILE_TAG}.py condorOut
