#!/bin/bash






MAXEVENT=10000
#infile='/x4/cms/dylee/NanoAODTool/aQGC/genproductions/bin/MadGraph5_aMCatNLO/tar_storage/FM1_5_9_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz' # full path & name of gridpack
infile=$1



Filename=`echo $infile  | awk -F '/' '{print $11}'` # full name of gridpack
Paramname=`echo $Filename | awk -F '_sl' '{print $1}'` # parameter name of gridpack



if [ ! -d condorOut ]; then mkdir condorOut; fi
if [ ! -d condorLog ]; then mkdir condorLog; fi


echo "Start gridpack ${Filename}.."

cat << EOF >> ${Paramname}.jdl
executable = wrapper_condor_aQGC.sh
universe = vanilla
output   = condorLog/condorLog_${Paramname}_\$(Cluster)_\$(Process).out
error    = condorLog/condorLog_${Paramname}_\$(Cluster)_\$(Process).err
log      = /dev/null
should_transfer_files = yes
transfer_input_files = ${infile},wrapper_condor_aQGC.sh
when_to_transfer_output = ON_EXIT
transfer_output_files = condorOut
requirements = (machine == "node01") || (machine == "node03")||(machine == "node04") || (machine == "node05") || (machine == "node07")
arguments = ${Filename} ${MAXEVENT} \$(Cluster) \$(Process)
queue 1
EOF


echo "Run Condor ${Filename}.jdl .."
condor_submit ${Paramname}.jdl


