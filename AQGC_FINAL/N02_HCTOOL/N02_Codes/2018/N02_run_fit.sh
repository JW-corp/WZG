#!/bin/bash

#>>> import numpy as np
#>>> np.load('scales.npy',allow_pickle=True)[()]
#{'FT0': {'aqgc': (1, 0.561, 4.418)}}


#for i in 'FT0' 'FT1' 'FT5' 'FT6' # 5
#do
#band=5

#for i in 'FT2' 'FT7'
#do
#band=100

#for i in 'FM0' 'FM2' 'FM3'
#do
#band=800

#for i in 'FM1' 
#do
#band=3000

#for i in  'FM4' 'FM5'
#do
#band=100


for i in  'FM7'
do
band=300

##
echo "start fit......${i} "
cardname="cards_SR_2018/aQGC_card_SR_mlllA_bin2.txt"

scalename="../../../Quadratic_Fit/2018/aQGC_dim8/ratios/${i}_ratio.npy"
dirpath="cards_SR_2018"
outname="${dirpath}/${i}.root"

text2workspace.py ${cardname} -P HiggsAnalysis.CombinedLimit.QuadraticScaling:quad --PO scaling=${scalename} --PO process=aQGC --PO coefficient=${i} -o ${outname}

cat << EOF > fit_${i}.sh
combine -M MultiDimFit ${outname} --algo=grid --points=1000 -P ${i} --floatOtherPOIs=0 -t -1 --expectSignal=1 --setParameterRange ${i}=-${band},${band}
#combine -M MultiDimFit ${outname} --algo=grid --points=1000 -P ${i} --floatOtherPOIs=0 --setParameterRange ${i}=-${band},${band}
EOF

source fit_${i}.sh

mv higgsCombineTest.MultiDimFit.mH120.root "cards_SR_2018/${i}.root"
rm fit_${i}.sh




done

