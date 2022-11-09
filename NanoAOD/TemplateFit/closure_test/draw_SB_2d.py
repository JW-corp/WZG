import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


infile   = ['log.csv']


# -- file (PT-Eta bins loop)
sum_df = 0
for f in infile:

	plt.close()
	colnames = ['Photon IsoChg lower','Photon IsoChg upper','Uncertainty']
	df		 = pd.read_csv(f,names = colnames,header=None,delim_whitespace=True)
	df = df.abs()
	
	
	print(df)
	#print(df.pivot('Iso_lower','Iso_upper','Unc'))
	
	
	df_pivoted = df.pivot('Photon IsoChg lower','Photon IsoChg upper','Uncertainty')
	print(df_pivoted)
	

	sum_df += df_pivoted

	# draw heat,ap
	plt.rcParams["figure.figsize"] = (8,8)
	plt.rcParams.update({'font.size': 15})
	ax = sns.heatmap(df_pivoted,annot=True,linewidths=1,fmt='.2f',linecolor='lightpink')
	ax.invert_yaxis()
	plt.show()


print("##### Summary #####")
print(sum_df/len(infile))
