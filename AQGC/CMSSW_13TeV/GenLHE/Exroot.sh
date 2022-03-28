#!/bin/bash



if [ ! -d condorOut/roots ]; then mkdir -p condorOut/roots; fi
flist=`ls -1 condorOut`


for f in $flist
do
outname=`echo ${f} | awk -F '.' '{print $1}'`
/x5/cms/jwkim/MG5_aMC_v2_7_3/ExRootAnalysis/ExRootLHEFConverter condorOut/$f  condorOut/roots/${outname}.root
done





