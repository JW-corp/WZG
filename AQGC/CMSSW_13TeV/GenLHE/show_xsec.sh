#!/bin/bash


# -Make list
flist=`ls -1 store/*.lhe`
base_dir=$PWD # Absolute path


# -Loop
buffer=0 # passing same process  
for fname in $flist
do

 
# get xsec (speed up grep using m1 option)
xsec=`grep -m1 "Inte" ${fname} | awk '{print $6}'`

# fname 
fname=`basename $fname`

# extrac root file path
partical_name=`echo $fname | awk -F '.' '{print $1}'`
tmp_path="/store/roots/${partical_name:0:8}\*.root"
root_path="${base_dir}${tmp_path}"

# passing same process ( there can be same process with different file cf. parrelization )
if [[ $buffer = ${partical_name:0:8} ]]; then continue;fi

# passing SM WZG and QCKM all zeros
if [[ ${partical_name:0:8} == WZA* ]]; then continue; fi
if [[ ${partical_name:0:8} == QCKM* ]]; then continue; fi

# update buffer
buffer=${partical_name:0:8}


# parse file name
fname=`echo $fname | awk -F '_' '{print $1"_"$2".00E-"$3}'`


# print out
echo $fname $root_path $xsec

done
# -- End Loop
