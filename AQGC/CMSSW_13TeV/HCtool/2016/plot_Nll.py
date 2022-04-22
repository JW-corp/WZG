import uproot 
import awkward as ak
import matplotlib.pyplot as plt
import mplhep as hep

# Design CMS tdrStyle
lumi=35.86
plt.figure(figsize=(8, 8)) 
plt.style.use(hep.style.CMS)                                                                                                                                          
hep.cms.text("Preliminary")
hep.cms.lumitext("{} fb$^{{-1}}$".format(lumi))


# ROOT.Math.chisquared_quantile_c(1-0.95,1)
deltaNLL_95 = 3.8414588206941236


# I&O , Convert tree to arrays (First value is ignored)
infile="/x5/cms/jwkim/HCtool/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/data/tutorials/2016/higgsCombineTest.MultiDimFit.mH120.root"
tree	= uproot.open(infile+":/limit")
arr_FT0		 = tree['FT0'].array()[1:]
arr_deltaNLL = tree['deltaNLL'].array()[1:] * 2



# Find CLs 95% x 
mx_95=0
my_95=0
px_95=0
py_95=0


convex_cnt=0
for i in range(len(arr_deltaNLL)):

	# negative
	print(arr_deltaNLL[i])
	if (arr_deltaNLL[i] <= deltaNLL_95) and (convex_cnt==0):
		mx_95 = arr_FT0[i]
		my_95 = arr_deltaNLL[i]
		convex_cnt+=1
		print(mx_95,my_95)

	# positive
	if (arr_deltaNLL[i] >= deltaNLL_95) and (convex_cnt==1):
		px_95 = arr_FT0[i]
		py_95 = arr_deltaNLL[i]
		print(px_95,py_95)
		break




# Plotting
plt.plot(arr_FT0,arr_deltaNLL,'.',color='royalblue',label='expected 2$\Delta$NLL')

plt.axhline(y=deltaNLL_95,color='black', linewidth=3,linestyle='--') # horizon line 95% CLs

plt.vlines(mx_95,-1,my_95,linewidth=3,linestyle='-',color='black',label='expected 95% confidence limit \n[{0:.3f},{1:.3f}]'.format(mx_95,px_95))
plt.vlines(px_95,-1,py_95,linewidth=3,linestyle='-',color='black')


plt.ylim(min(arr_deltaNLL)-1,max(arr_deltaNLL)+1)

plt.ylabel('2$\Delta$NLL')
plt.xlabel('FT0/$\Lambda^{4}$ [$TeV^{-4}$]')
plt.legend(fontsize=17)
plt.savefig("NLL_scan.png")
plt.show()
