import numpy as np
import ROOT
import matplotlib.pyplot as plt
import os
#import mplhep as hep
#plt.style.use(hep.style.CMS)


import csv

npys = ['npys/FM0.npy' ,'npys/FM1.npy' ,'npys/FM2.npy' ,'npys/FM3.npy' ,'npys/FM4.npy' ,'npys/FM5.npy' ,'npys/FM7.npy' ,'npys/FT0.npy' ,'npys/FT1.npy' ,'npys/FT2.npy' ,'npys/FT5.npy' ,'npys/FT6.npy' ,'npys/FT7.npy']

f = open('fit_summary_2018.csv','w')
wr = csv.writer(f)
wr.writerow(['Operator','Chi2','NDF','P-value'])

for i in range(len(npys)):


	graph_x = np.load(npys[i])[0] * 1e+12
	graph_y = np.load(npys[i])[1]
		
	g1     = ROOT.TGraph(len(graph_x),graph_x,graph_y)
	f1     = ROOT.TF1("f1","[0]*x*x + [1]*x+1")
	fit1   = g1.Fit('f1','S')

	
	p0=fit1.Parameter(0)
	p1=fit1.Parameter(1)
	
	def func(x,p0,p1):
	    return 1+ p1*x + p0*x*x
	
	minx = np.min(graph_x)
	maxx = np.max(graph_x)
	max_abs_x = max(abs(minx),abs(maxx))
	
	#func_x = np.linspace(np.min(graph_x),np.max(graph_x),200)
	func_x = np.linspace(-1*max_abs_x,max_abs_x,200)
	
	
	
	# Draw graph
	plt.plot(graph_x,graph_y,'o')
	plt.plot(func_x,func(func_x,p0,p1),color='r',alpha=0.5,label='fitted: 1 + p1x + p0$x^2$')
	plt.plot([], [], ' ', label="p0 : {0:.6f}".format(p0))
	plt.plot([], [], ' ', label="p1 : {0:.6f}".format(p1))
	
	plt.legend()
	plt.grid('-',alpha=0.5)
	xname  = npys[i].split('/')[1].split('.')[0] + "/" + "$\Lambda^{4}$" + "[TeV$^{-4}$]"
	plt.xlabel(xname)
	plt.ylabel('aQGC/SM')
	
	# --> Output	
	directory = 'ratios'
	if not os.path.exists(directory):
		os.makedirs(directory)

	key_name = npys[i].split('/')[1].split('.')[0]
	outname_npy = 'ratios/' + key_name + "_ratio" + ".npy"
	outname_png = 'ratios/' + key_name + "_ratio" + ".png"
	outname_pdf = 'ratios/' + key_name + "_ratio" + ".pdf"
	
	print("### Fit summary ###")
	print("Name,Chi2,Ndf,Pvalue")
	print(key_name,fit1.Chi2(), fit1.Ndf(), fit1.Prob())
	print("### ----------- ###")

	wr.writerow([key_name,fit1.Chi2(),int(fit1.Ndf()),fit1.Prob()])

	fit_func = {key_name : {'aQGC' : (1,p1,p0)}}
	#np.save(outname_npy,fit_func)
	#plt.savefig(outname_png)
	#plt.savefig(outname_pdf)
	
	plt.close()
	
	
