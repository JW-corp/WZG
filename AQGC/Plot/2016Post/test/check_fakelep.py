import uproot
import mplhep as hep
import matplotlib.pyplot as plt

myfile = "WZG.root"
tree = uproot.open(myfile)

hist_norminal = tree['WZG_WZG_mllla_FakeLep_None'].to_numpy()
hist_sys_up = tree['WZG_WZG_mllla_FakeLep_sys_up'].to_numpy()
hist_sys_down = tree['WZG_WZG_mllla_FakeLep_sys_down'].to_numpy()

hist_stat_up = tree['WZG_WZG_mllla_FakeLep_stat_up'].to_numpy()
hist_stat_down = tree['WZG_WZG_mllla_FakeLep_stat_down'].to_numpy()

print(hist_norminal[0])

lumi=16.8
plt.figure(figsize=(8, 8)) 
plt.style.use(hep.style.CMS)                                                                                                                                          
hep.cms.text("Preliminary")
hep.cms.lumitext("{} fb$^{{-1}}$".format(lumi))

def make_sys_plot():
    hep.histplot(hist_norminal, label='FakeLep_None', histtype='step', color='black')
    hep.histplot(hist_sys_up, label='FakeLep_sys_up', histtype='step', color='red')
    hep.histplot(hist_sys_down, label='FakeLep_sys_down', histtype='step', color='blue')

    for i in range(len(hist_norminal[0])):
        print("##"*20)
        print(f"Bin norm {i+1} :{hist_norminal[0][i]}")
        print(f"Bin up{i+1} :{hist_sys_up[0][i]}")
        print(f"Bin down{i+1} :{hist_sys_down[0][i]}")
        print(f"Unc Bin {i+1}: ",max(abs(hist_sys_up[0][i]-hist_norminal[0][i]), abs(hist_sys_down[0][i]-hist_norminal[0][i])) / hist_norminal[0][i])
        print("##"*20)


    plt.xlabel("$m_{lll}$ [GeV]")
    plt.ylabel("Events/bin")
    plt.ylim(-0.2, 0)
    plt.legend()
    plt.savefig("FakeLep_Sys.png")


def make_stat_plot():
    hep.histplot(hist_norminal, label='FakeLep_None', histtype='step', color='black')
    hep.histplot(hist_stat_up, label='FakeLep_stat_up', histtype='step', color='red')
    hep.histplot(hist_stat_down, label='FakeLep_stat_down', histtype='step', color='blue')

    for i in range(len(hist_norminal[0])):
        print("##"*20)
        print(f"Bin norm {i+1} :{hist_norminal[0][i]}")
        print(f"Bin up{i+1} :{hist_stat_up[0][i]}")
        print(f"Bin down{i+1} :{hist_stat_down[0][i]}")
        print(f"Unc Bin {i+1}: ",max(abs(hist_stat_up[0][i]-hist_norminal[0][i]), abs(hist_stat_down[0][i]-hist_norminal[0][i])) / hist_norminal[0][i])
        print("##"*20)

    plt.xlabel("$m_{lll}$ [GeV]")
    plt.ylabel("Events/bin")
    plt.ylim(-0.2, 0)
    plt.legend()
    plt.savefig("FakeLep_Stat.png")

make_sys_plot()
#make_stat_plot()
