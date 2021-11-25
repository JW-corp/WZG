import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import mplhep as hep




df = pd.read_csv('aQGC_list_db.csv',delimiter=',')
df.set_index('name',inplace=True)
print(df)


sm_xsec	   = df.loc['sm']['xsec']
aQGC0_xsec = df.loc['aQGC_all0']['xsec']


plt.style.use(hep.style.ROOT)
fig,axs = plt.subplots(1,figsize=(15,10))




axs.hlines(sm_xsec,0,50,linestyle='dotted',colors='gray',label='sm')
axs.hlines(aQGC0_xsec,0,50,linestyle='dotted',colors='darkkhaki',label='aQGC all zeros')

def extract_xy(df,param):
	tmp_df = df[df.index.str.startswith(param)]
	x = [float(i.split('_')[-1])*1e+12 for i in tmp_df.index]
	y = tmp_df['xsec']

	axs.plot(x,y,'-o',label=param)


extract_xy(df,'FT0')
extract_xy(df,'FT1')
extract_xy(df,'FT2')
extract_xy(df,'FT5')
extract_xy(df,'FT6')
extract_xy(df,'FT7')



#extract_xy(df,'FM0')
#extract_xy(df,'FM1')
#extract_xy(df,'FM2')
#extract_xy(df,'FM3')
#extract_xy(df,'FM4')
#extract_xy(df,'FM5')
#extract_xy(df,'FM7')


#axs.set_xlim([0,2000])
#axs.set_ylim([0.014,0.04])


axs.set_xlabel('parameter values') 
axs.set_ylabel('xsec [pb]')
axs.set_yscale('log')


#axs.set_yticks([0.014,0.016,0.017,0.018,0.019,0.02,0.04,0.08,0.1])
#axs.set_yticks([0.014,0.016,0.018,0.02,0.025,0.03,0.035,0.04,0.06,0.08,0.1])
#axs.set_yticks([0.014,0.018,0.02,0.025,0.06,0.08,0.1])
axs.set_yticks([0.016,0.017,0.018,0.02,0.022,0.024,0.026,0.028,0.03])


axs.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())

plt.grid(alpha=0.5)
plt.legend(prop={"size": 15})
plt.show()

