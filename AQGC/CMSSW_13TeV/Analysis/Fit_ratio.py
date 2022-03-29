import numpy as np
import ROOT



# Read data within fixed m(WZ) bins 

fname_list = ['FM0_mllA.npy' ,'FM1_mllA.npy' ,'FM2_mllA.npy' ,'FM3_mllA.npy' ,'FM4_mllA.npy' ,'FM5_mllA.npy' ,'FM7_mllA.npy' ,'FT0_mllA.npy' ,'FT1_mllA.npy' ,'FT2_mllA.npy' ,'FT5_mllA.npy' ,'FT6_mllA.npy' ,'FT7_mllA.npy'] 

fname_list = ['FT0_mllA.npy']

bin = 5

for fname in fname_list:
	#fname = 'FT0_mllA.npy'
	data  = np.load(fname,allow_pickle=True)[()]
	y_dict = data[1] 
	y_keys = data[1].keys()
	
	
	for ith_bin in range(bin):
	
		x      = data[0][ith_bin]
		
		
		
		# Make data point
		graph_x=[]
		graph_y=[]
		for y_key in y_keys:
		
			# unit: 1E-12
			if y_key.split('_')[-1] == 'all0':
				x_val=0
			else:
				x_val   = float(y_key.split('_')[-1])  / 1E-12 
			print(x_val,y_dict[y_key][ith_bin])
			graph_x.append(x_val)
			graph_y.append(y_dict[y_key][ith_bin])
		graph_x=np.array(graph_x)
		graph_y=np.array(graph_y)
		
		
		
		# Fitting : p0 + p1x + p2x^2
		g1     = ROOT.TGraph(len(graph_x),graph_x,graph_y)
		fit1   = g1.Fit('pol2','S')
		print(fit1) 
		
		p0=fit1.Parameter(0)
		p1=fit1.Parameter(1)
		p2=fit1.Parameter(2)
		def func(x,p0,p1,p2):
			return p0 + p1*x + p2*x*x
		func_x = np.linspace(0,np.max(graph_x),100)
		
		
		# Draw graph
		import matplotlib.pyplot as plt
		plt.plot(graph_x,graph_y,'o')
		plt.plot(func_x,func(func_x,p0,p1,p2),color='r',alpha=0.5,label='fitted: p0 + p1x + p2$x^2$')
		plt.plot([], [], ' ', label="p0 : {0:.3f}".format(p0))
		plt.plot([], [], ' ', label="p1 : {0:.3f}".format(p1))
		plt.plot([], [], ' ', label="p2 : {0:.3f}".format(p2))
		
		plt.legend()
		plt.grid('-',alpha=0.5)
		
		plt.xlabel('parameter [1e-12]')
		plt.ylabel('aQGC/SM')
		#plt.show()
		
		
		# Save figure
		outname = 'RatioPlot_' + fname.split('.')[0] + '_{0}th_bins.png'.format(ith_bin) 
		plt.savefig(outname)
		plt.close()
		
