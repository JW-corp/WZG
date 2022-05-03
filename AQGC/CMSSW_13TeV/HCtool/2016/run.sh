#!/bin/bash

#>>> import numpy as np
#>>> np.load('scales.npy',allow_pickle=True)[()]
#{'FT0': {'aqgc': (1, 0.561, 4.418)}}





#for i in 'FT0' 'FT1' 'FT2' 'FT5' 'FT6' 'FT7'
#for i in 'FM0' 'FM1' 'FM2' 'FM3' 'FM4' 'FM7'
#for i in 'FM0' 'FM1' 
#for i in 'FM4' 
for i in 'FM5' 
do
echo "start fit......${i} "
cardname="cards_SR_2016/${i}_card_SR_mZA_bin4.txt"
scalename="fit_pickles_for_HC/outfit_${i}.npy"
outname="cards_SR_2016/${i}.root"

text2workspace.py ${cardname} -P HiggsAnalysis.CombinedLimit.QuadraticScaling:quad --PO scaling=${scalename} --PO process=aQGC --PO coefficient=${i} -o ${outname}

cat << EOF > fit_${i}.sh
combine -M MultiDimFit ${outname} --algo=grid --points=1000 -P ${i} --floatOtherPOIs=0 -t -1 --expectSignal=1 --setParameterRange ${i}=-5,5
EOF

source fit_${i}.sh
mv higgsCombineTest.MultiDimFit.mH120.root "cards_SR_2016/${i}.root"
rm fit_${i}.sh
done
