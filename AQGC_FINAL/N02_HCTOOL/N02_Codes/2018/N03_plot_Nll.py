import uproot 
import awkward as ak
import matplotlib.pyplot as plt
import mplhep as hep
import glob
import csv


# ROOT.Math.chisquared_quantile_c(1-0.95,1)
deltaNLL_95 = 3.8414588206941236


# I&O , Convert tree to arrays (First value is ignored)

fpath = "cards_SR_2018/*.root"
#fpath = "cards_SR_2016/FM5.root"

flist = glob.glob(fpath)



limit_list=[]

# Loop
for infile in flist:

	print("processing... {0}".format(infile))
	param_name	 = infile.split('/')[-1].split('.')[0]
	tree		 = uproot.open(infile+":/limit")
	arr_param	 = tree[param_name].array()[1:]
	arr_deltaNLL = tree['deltaNLL'].array()[1:] * 2

	# Find CLs 95% x 
	mx_95=0
	my_95=0
	px_95=0
	py_95=0

	convex_cnt=0
	for i in range(len(arr_deltaNLL)):
	
		# negative
		if (arr_deltaNLL[i] <= deltaNLL_95) and (convex_cnt==0):
			mx_95 = arr_param[i]
			my_95 = arr_deltaNLL[i]
			convex_cnt+=1
			#print(mx_95,my_95)
	
		# positive
		if (arr_deltaNLL[i] >= deltaNLL_95) and (convex_cnt==1):
			px_95 = arr_param[i]
			py_95 = arr_deltaNLL[i]
			#print(px_95,py_95)
			break

	# Plotting
	# Design CMS tdrStyle
	lumi=59.7
	plt.figure(figsize=(8, 8)) 
	plt.style.use(hep.style.CMS)                                                                                                                                          
	hep.cms.text("Preliminary")
	#hep.cms.text("Work in progress")
	hep.cms.lumitext("{} fb$^{{-1}}$".format(lumi))
	plt.plot(arr_param,arr_deltaNLL,'.',color='royalblue',label='expected 2$\Delta$NLL')
	
	plt.axhline(y=deltaNLL_95,color='black', linewidth=3,linestyle='--') # horizon line 95% CLs
	
	plt.vlines(mx_95,-1,my_95,linewidth=3,linestyle='-',color='black',label='expected 95% confidence limit \n[{0:.3f},{1:.3f}]'.format(mx_95,px_95))
	plt.vlines(px_95,-1,py_95,linewidth=3,linestyle='-',color='black')
	
	
	plt.ylim(min(arr_deltaNLL)-1,max(arr_deltaNLL)+1)
	
	plt.ylabel("2$\Delta$NLL")
	plt.xlabel("%s /$\Lambda^{4}$ [$TeV^{-4}$]" % (param_name))
	plt.legend(fontsize=17)
		
	#plt.savefig("cards_SR_2018/NLL_scan_{0}.png".format(param_name))
	plt.savefig("cards_SR_2018/NLL_scan_{0}.pdf".format(param_name))
	#plt.show()
	plt.close()
	limit_list.append([param_name,mx_95,px_95])


import pandas as pd
df=pd.DataFrame(limit_list,columns=['name','-95CLs','+95CLs'])
df = df.sort_values(by=['name'])
print(df)
df.to_csv("CLs_18.csv")
#df.to_excel("CLs_18.xlsx")


