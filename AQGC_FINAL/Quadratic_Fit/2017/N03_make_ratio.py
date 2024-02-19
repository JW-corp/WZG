import ROOT
import numpy as np
import os


## - Predifined variables
FM0=['-4e-10','-3e-10','-2e-10','-1e-10','-5e-11','2e-11','2e-11','5e-11','1e-10','2e-10','3e-10','4e-10']
FM1=['-4e-10','-3e-10','-2e-10','-1e-10','-5e-11','2e-11','2e-11','5e-11','1e-10','2e-10','3e-10','4e-10']
FM2=['-4e-10','-3e-10','-2e-10','-1e-10','-5e-11','2e-11','2e-11','5e-11','1e-10','2e-10','3e-10','4e-10']
FM3=['-4e-10','-3e-10','-2e-10','-1e-10','-5e-11','2e-11','2e-11','5e-11','1e-10','2e-10','3e-10','4e-10']
FM7=['-8e-11','-6e-11','-4e-11','-2e-11','-1e-11','-5e-12','-3e-12','-1e-12','1e-12','3e-12','5e-12','1e-11','2e-11','4e-11','6e-11','8e-11']
FM4=['-3e-11','-2e-11','-1e-11','-5e-12','-4e-12','-3e-12','-2e-12','-1e-12','1e-12','2e-12','3e-12','4e-12','5e-12','1e-11','2e-11','3e-11']
FM5=['-3e-11','-2e-11','-1e-11','-5e-12','-4e-12','-3e-12','-2e-12','-1e-12','1e-12','2e-12','3e-12','4e-12','5e-12','1e-11','2e-11','3e-11']
FT0=['-3e-11','-2e-11','-1e-11','-5e-12','-4e-12','-3e-12','-2e-12','-1e-12','1e-12','2e-12','3e-12','4e-12','5e-12','1e-11','2e-11','3e-11']
FT1=['-3e-11','-2e-11','-1e-11','-5e-12','-4e-12','-3e-12','-2e-12','-1e-12','1e-12','2e-12','3e-12','4e-12','5e-12','1e-11','2e-11','3e-11']
FT2=['-3e-11','-2e-11','-1e-11','-5e-12','-4e-12','-3e-12','-2e-12','-1e-12','1e-12','2e-12','3e-12','4e-12','5e-12','1e-11','2e-11','3e-11']
FT5=['-3e-11','-2e-11','-1e-11','-5e-12','-4e-12','-3e-12','-2e-12','-1e-12','1e-12','2e-12','3e-12','4e-12','5e-12','1e-11','2e-11','3e-11']
FT6=['-3e-11','-2e-11','-1e-11','-5e-12','-4e-12','-3e-12','-2e-12','-1e-12','1e-12','2e-12','3e-12','4e-12','5e-12','1e-11','2e-11','3e-11']
FT7=['-3e-11','-2e-11','-1e-11','-5e-12','-4e-12','-3e-12','-2e-12','-1e-12','1e-12','2e-12','3e-12','4e-12','5e-12','1e-11','2e-11','3e-11']

list_map = {'FM0':FM0 ,'FM1':FM1 ,'FM2':FM2 ,'FM3':FM3 ,'FM4':FM4 ,'FM5':FM5 ,'FM7':FM7 ,'FT0':FT0 ,'FT1':FT1 ,'FT2':FT2,'FT5':FT5 ,'FT6':FT6 ,'FT7':FT7}
list_all = ['FM0' ,'FM1' ,'FM2' ,'FM3' ,'FM4' ,'FM5' ,'FM7' ,'FT0' ,'FT1' ,'FT2' ,'FT5','FT6' ,'FT7']


## - I/O
Nbin = 2
file_hist = ROOT.TFile.Open("test/WZG.root")
h1 = file_hist.Get("WZG_WZG_mllla_aQGC_None_Rwt0")
All_zero = h1.GetBinContent(Nbin)


## - Check output directory
npy_out_dir_name = 'npys'
if not os.path.exists(npy_out_dir_name):
	os.makedirs(npy_out_dir_name)



## - Loop
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
	outpath = npy_out_dir_name + '/' + outname
	np.save(outpath,[tmp_var_list,tmp_rat_list])

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


