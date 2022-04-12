

#>>> import numpy as np
#>>> np.load('scales.npy',allow_pickle=True)[()]
#{'FT0': {'aqgc': (1, 0.561, 4.418)}}


text2workspace.py datacard/FT03e-12.txt -P HiggsAnalysis.CombinedLimit.QuadraticScaling:quad --PO scaling=scales.npy --PO process=aqgc --PO coefficient=FT0 -o datacard/FT0.root
combine -M MultiDimFit datacard/FT0.root  --algo=grid --points=100   -P FT0 --floatOtherPOIs=0 -t -1 --expectSignal=1 --setParameterRange FT0=0,5


