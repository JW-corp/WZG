

#>>> import numpy as np
#>>> np.load('scales.npy',allow_pickle=True)[()]
#{'FT0': {'aqgc': (1, 0.561, 4.418)}}


text2workspace.py cards_SR_2016/card_SR_mZA_bin4.txt -P HiggsAnalysis.CombinedLimit.QuadraticScaling:quad --PO scaling=scales.npy --PO process=aQGC --PO coefficient=FT0 -o cards_SR_2016/aQGC.root
combine -M MultiDimFit cards_SR_2016/aQGC.root  --algo=grid --points=100   -P FT0 --floatOtherPOIs=0 -t -1 --expectSignal=1 --setParameterRange FT0=-5,5


