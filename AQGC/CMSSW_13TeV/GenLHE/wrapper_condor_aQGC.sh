#!/bin/bash

GRIDPACK=$1
MAXEVENT=$2
cluster_name=$3
proc_name=$4
Paramname=`echo $GRIDPACK | awk -F '_sl' '{print $1}'`

gcc_version='slc7_amd64_gcc700'
CMSSW_version='CMSSW_10_6_19'





source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=$gcc_version
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
cd /cvmfs/cms.cern.ch/${gcc_version}/cms/cmssw/${CMSSW_version}/
eval `scramv1 runtime -sh`
cd -
tar xvf ${GRIDPACK}




start=`date +%s`
./runcmsgrid.sh ${MAXEVENT} ${RANDOM}
if [ ! -d condorOut ]; then mkdir condorOut; fi
mv cmsgrid_final.lhe condorOut/${Paramname}_${cluster_name}_${proc_name}.lhe
end=`date +%s`


echo "Running time: $((end-start))"
