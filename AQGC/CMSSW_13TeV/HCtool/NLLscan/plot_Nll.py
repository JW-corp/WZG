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
infile="/x5/cms/jwkim/HCtool/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/data/tutorials/higgsCombineTest.MultiDimFit.mH120.root"
tree	= uproot.open(infile+":/limit")
arr_FT0		 = tree['FT0'].array()[:-1]
arr_deltaNLL = tree['deltaNLL'].array()[:-1] * 2


# Find CLs 95% x 
x_95=0
y_95=0
for i in range(len(arr_deltaNLL)):
	if arr_deltaNLL[i] >= deltaNLL_95:
		x_95 = arr_FT0[i]
		y_95 = arr_deltaNLL[i]
		break

# Plotting
plt.plot(arr_FT0,arr_deltaNLL,'.',color='royalblue',label='expected 2$\Delta$NLL')
plt.axhline(y=deltaNLL_95,color='black', linewidth=3,linestyle='--') # horizon line 95% CLs
plt.vlines(x_95,min(arr_deltaNLL)-1,y_95,linewidth=3,linestyle='-',color='black',label='expected 95% confidence limit \n[-{0:.3f},{0:.3f}]'.format(x_95))


plt.ylim(min(arr_deltaNLL)-1,max(arr_deltaNLL)+1)

plt.ylabel('2$\Delta$NLL')
plt.xlabel('FT0/$\Lambda^{4}$ [$TeV^{-4}$]')
plt.legend(fontsize=17)
plt.show()
