import matplotlib.pyplot as plt
import mplhep as hep
from matplotlib import rc
import pandas as pd
import numpy as np


plt.style.use(hep.style.ROOT)
plt.rcParams["figure.figsize"] = (8,8)
#plt.xlim(10,1000)
#plt.ylim(0.00000000001, 10)


df = pd.read_csv('FT0limit.csv',delim_whitespace=True)


param = [i*0.1 for i in range(1,len(df)+1)]


#param = np.array(range(len(df['name']))) + 1


plt.plot(param,df['median'].values, '--',label ="Median $\sigma$$_{exp}/\sigma$$_{theo}$", color ='black')
plt.fill_between(param, df['m2'].values, df['p2'].values, color='yellow', label = 'Expected $\pm$ 2$\sigma$')
plt.fill_between(param, df['m1'].values, df['p1'].values, color='limegreen', label = 'Expected $\pm$ 1$\sigma$')
plt.axhline(y=1, color='r', linewidth=1)
plt.yscale('log')
plt.rc('xtick',labelsize=10)
plt.rc('ytick',labelsize=10)
plt.title("$\sqrt{s}$ = 13 TeV, L = 35.86 fb$^{-1}$", loc='left',fontsize=15)
plt.xlabel("$f_{T0}/\Lambda^{4}$ ($x 10^{-12}$ GeV)", fontsize=15)
plt.ylabel("$\sigma$$_{exp}/\sigma$$_{theo}$", fontsize=15)
plt.minorticks_on()
plt.legend()
plt.show()





#1plt.savefig("testlimit")
