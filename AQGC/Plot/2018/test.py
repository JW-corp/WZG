import uproot
import awkward as ak
import numpy as np



file = "/cms/ldap_home/jwkim2/New_ccp/Ntuples/2018/LLWA_WToLNu_4FS_TuneCP5_13TeV-amcatnlo-pythia8_2018_0000.root"


arrays = uproot.open(file + ":Events").arrays(["Photon_ID_Weight","Photon_ID_Weight_UP","Photon_ID_Weight_DOWN"])
print(arrays)
