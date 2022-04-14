#!/bin/bash

param=$1
aqgc_yield=$2 #scan	
sm_yield=$3  #fit
out_csv_name=$4

cat << EOF > datacard/${param}.txt
imax 1  number of channels
jmax *  number of backgrounds
kmax *  number of nuisance parameters (sources of systematical uncertainties)
-----------------------------------------------------------------------------
bin                  llaMass
observation          0
-----------------------------------------------------------------------------
bin                  llaMass         llaMass              
process              aqgc	   sm           
process              0         1                  
rate		         $aqgc_yield    $sm_yield
-----------------------------------------------------------------------------
# 
lumi        lnN      1.012     1.012 
JES/JER     lnN      1.2       1.2
HLT_sta     lnN		 1.007	   1.007
HLT_sys		lnN		 1.005	   1.005
id_eff		lnN		 1.001	   1.001
EOF

combine -M AsymptoticLimits datacard/${param}.txt  --run blind > wzg_13TeC_aqgc.out
r_list=`cat wzg_13TeC_aqgc.out | grep "Ex" | awk '{print $5}'`

echo ${param} ${r_list} >> $out_csv_name



