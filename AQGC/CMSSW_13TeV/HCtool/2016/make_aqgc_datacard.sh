#!/bin/bash

#flist=`ls -1 aqgc_root_for_HC/*.root`

flist='aqgc_root_for_HC/FM5_WZG_2016.root'
for f in $flist
do
echo "####### start $f ######"
python Combine_help.py $f
done
