#!/bin/bash

#>>> import numpy as np
#>>> np.load('scales.npy',allow_pickle=True)[()]
#{'FT0': {'aqgc': (1, 0.561, 4.418)}}





#for i in 'FT0' 'FT1' 'FT5' 'FT6' # 5
#do
#band=5


#for i in 'FT2' 'FT7'
#do
#band=50


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




echo "start fit......${i} "
cardname="cards_SR_full/aQGC_card_SR_mlllA_bin2.txt"



scalename="/cms/ldap_home/jwkim2/New_ccp/plot/aQGC_merged/aQGC_dim8/ratios/${i}_ratio.npy"
outname="cards_SR_full/${i}.root"

text2workspace.py ${cardname} -P HiggsAnalysis.CombinedLimit.QuadraticScaling:quad --PO scaling=${scalename} --PO process=aQGC --PO coefficient=${i} -o ${outname}

cat << EOF > fit_${i}.sh
combine -M MultiDimFit ${outname} --algo=grid --points=1000 -P ${i} --floatOtherPOIs=0 -t -1 --expectSignal=1 --setParameterRange ${i}=-${band},${band}
EOF

source fit_${i}.sh
mv higgsCombineTest.MultiDimFit.mH120.root "cards_SR_full/${i}.root"
rm fit_${i}.sh
done

