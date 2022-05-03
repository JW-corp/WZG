import pickle
import numpy as np
import glob

fpath		= "fit_pickles_for_HC/*.pickle"
pickle_list = glob.glob(fpath)


for f in pickle_list:
	with open(f,"rb") as fr:
		data = pickle.load(fr)
		
	
	print(data)
	#{u'FM0': {u'aqgc': (1, -0.004284855941696378, 7.174695315824152e-05)}}

	key       = str(data.keys()[0])
	inner_key = str(data[key].keys()[0])
	val = data[key][inner_key]
	data = {key:{'aQGC':val}}

	fname = f.split('/')[-1].split('_')[-1].split('.')[0]
	fpath = "fit_pickles_for_HC/" + "outfit_" + fname + ".npy"
	print(fpath)

	np.save(fpath,data)


