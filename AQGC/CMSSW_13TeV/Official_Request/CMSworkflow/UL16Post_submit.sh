#!/bin/bash

# test one shot

# there is one grid pack! 
GRID_NAME=LLWA_WToLNu_LOaQGC_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz
GRID_PATH=/hcp/home/jwkim2/2016Pre/${GRID_NAME}


EVENTS=50
FNAME=`echo $GRID_PATH | awk -F '/' '{print $11}' | awk -F '_sl' '{print $1}'`
PROXY_PATH=/tmp/x509up_u556800431
PROXY_NAME=`echo ${PROXY_PATH} | awk -F '/' '{print $3}'`


echo GRID_NAME :	    ${GRID_NAME}
echo GRID_PATH :        ${GRID_PATH}
echo FNAME     :        ${FNAME}
echo PROXY_NAME:        ${PROXY_NAME}

# Setup Working directory
[ -d log ] || mkdir log
[ -d condorOut ] || mkdir condorOut


# Write jdl file
cat << EOF > $FNAME_job.jdl
universe   = vanilla
executable = UL16Post_run_aQGC_all.sh
error      = log/${FNAME}_\$(Cluster)_\$(Process).err
output     = log/${FNAME}_\$(Cluster)_\$(Process).out
log        = log/${FNAME}_\$(Cluster)_\$(Process).log
should_transfer_files      = YES
when_to_transfer_output    = ON_EXIT
use_x509userproxy          = True
transfer_input_files       = ${GRID_PATH},${PROXY_PATH},/hcp/home/jwkim2/2016Pre/randomizeSeeds.py,/hcp/home/jwkim2/tools/NeutrinoE-10/filepath_Neutrino_E-10_gun_2016Post.txt
transfer_output_files = condorOut 
arguments = ${PROXY_NAME} ${GRID_NAME} ${EVENTS} \$(Cluster) \$(Process)
queue 100
EOF

condor_submit $FNAME_job.jdl

