from data_dict_FakeFrac_2017 import *
#from data_dict_FakeFrac_2018 import *
import os

# check the file exist or not 

print("check pseudo data")
for key in filelist_pseudo_data:
    if not os.path.isfile(filelist_pseudo_data[key]['path']):
        print("file not exist: ", filelist_pseudo_data[key]['path'])

print("check data")
for data in filelist_data:
    if not os.path.isfile(data):
        print("file not exist: ", data)

print("check MC")
for key in filelist_MC:
    if not os.path.isfile(filelist_MC[key]['path']):
        print("file not exist: ", filelist_MC[key]['path'])




