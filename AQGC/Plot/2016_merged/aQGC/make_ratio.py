import ROOT
import numpy as np




cW	  = ['-2.0','-1.5','-1.4','-1.3','-1.2','-1.1','1.1','1.2','1.3','1.4','1.5','2.0']
cHW   = ['-2.0','-1.5','-1.4','-1.3','-1.2','-1.1','1.1','1.2','1.3','1.4','1.5','2.0']
cHB   = ['-2.0','-1.5','-1.4','-1.3','-1.2','-1.1','1.1','1.2','1.3','1.4','1.5','2.0']
cHWB  = ['-2.0','-1.5','-1.4','-1.3','-1.2','-1.1','1.1','1.2','1.3','1.4','1.5','2.0']
cHDD  = ['-4.0','-3.5','-3.0','-2.5','-2.0','-1.5','-1.4','-1.3','-1.2','-1.1','1.1','1.2','1.3','1.4','1.5','2.0','2.5','3.0','3.5','4.0']

list_all = ['cW','cHW','cHB','cHWB','cHDD']
list_map = {'cW':cW,'cHW':cHW,'cHB':cHB,'cHWB':cHWB,'cHDD':cHDD}



Nbin = 2



file_hist = ROOT.TFile.Open("test/WZG.root")
h1 = file_hist.Get("WZG_WZG_mllla_aQGC_None_Rwt0")

All_zero = h1.GetBinContent(Nbin)


cnt=1
for param in list_all:
	tmp_var_list=[]
	tmp_rat_list=[]


	
	# Center value
	tmp_var_list.append(0)
	tmp_rat_list.append(All_zero/All_zero)

	for i, var in enumerate(list_map[param]):

		infile_name = "WZG_WZG_mllla_aQGC_None_Rwt" + str(cnt)
		h1 = file_hist.Get(infile_name)

		ratio = h1.GetBinContent(Nbin)/All_zero
		
		print(cnt,param,h1.GetBinContent(Nbin),All_zero,ratio)
		tmp_var_list.append(float(var))
		tmp_rat_list.append(float(ratio))
		cnt+=1


	outname = param + '.npy'
	np.save(outname,[tmp_var_list,tmp_rat_list])






quit()


#h1.SetLineColor(2)
#h1.SetFillColor(0)
#h1.SetLineWidth(4)
#
#
#print(h1)
#c1 = ROOT.TCanvas("","",1000,1000)
#h1.Draw("HIST")
#c1.Print("this.png")


