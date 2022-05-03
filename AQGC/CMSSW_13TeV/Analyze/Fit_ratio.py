import numpy as np
import ROOT


# Read data within fixed m(WZ) bins 

#fname_list = ['FM0_llA_mass.npy' ,'FM1_llA_mass.npy' ,'FM2_llA_mass.npy' ,'FM3_llA_mass.npy' ,'FM4_llA_mass.npy' ,'FM5_llA_mass.npy','FM7_llA_mass.npy' ,'FT0_llA_mass.npy' ,'FT1_llA_mass.npy' ,'FT2_llA_mass.npy' ,'FT5_llA_mass.npy' ,'FT6_llA_mass.npy' ,'FT7_llA_mass.npy']
fname_list = ['FM5_llA_mass.npy']
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
		func_x = np.linspace(-1*np.max(graph_x),np.max(graph_x),200)


		# Save fit-results
		key_name	   = fname.split('_')[0]
		out_name	   = 'outfit_' + key_name + '.pickle'
		fit_result_out = {key_name: {'aqgc': (1, p1, p0)}}

		
		import pickle
		with open(out_name,"wb") as fw:
			pickle.dump(fit_result_out,fw,protocol=2)
		

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
		
