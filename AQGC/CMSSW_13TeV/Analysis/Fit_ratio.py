import numpy as np
import ROOT



# Read data within fixed m(WZ) bins 


fname_list = ['FT0_llA_mass.npy']
#fname_list = ['FT0_lllA_mass.npy']

bin = 4

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
		f1	   = ROOT.TF1("f1","[0]*x*x + [1]*x+1")
		#fit1   = g1.Fit('pol2','S')
		fit1   = g1.Fit('f1','S')
		print(fit1) 
		
		p0=fit1.Parameter(0)
		p1=fit1.Parameter(1)
		def func(x,p0,p1):
			return 1+ p1*x + p0*x*x
		func_x = np.linspace(0,np.max(graph_x),100)
		
		if ith_bin == bin-1:
			ratio_point_from_func = np.array([func(0.1*i,p0,p1) for i in range(1,10*int(graph_x.max())+1)])
			print([i*0.1 for i in range(1,10*int(graph_x.max())+1)])
			print("ratio: ",ratio_point_from_func)
			np.save('FT0_ratio.npy',ratio_point_from_func)

		# Draw graph
		import matplotlib.pyplot as plt
		plt.plot(graph_x,graph_y,'o')
		plt.plot(func_x,func(func_x,p0,p1),color='r',alpha=0.5,label='fitted: 1 + p1x + p0$x^2$')
		plt.plot([], [], ' ', label="p0 : {0:.3f}".format(p0))
		plt.plot([], [], ' ', label="p1 : {0:.3f}".format(p1))
		
		plt.legend()
		plt.grid('-',alpha=0.5)
		
		plt.xlabel('parameter [1e-12]')
		plt.ylabel('aQGC/SM')
		#plt.show()
		
		
		# Save figure
		outname = 'RatioPlot_' + fname.split('.')[0] + '_{0}th_bins.png'.format(ith_bin) 
		plt.savefig(outname)
		plt.close()
		
