import numpy as numpy
import os

dict_list = ["WZG","ZGJ","ttZ","ZZ"]

for i in dict_list:
    npy_path = f"/cms/ldap_home/jwkim2/New_ccp/plot_ccp/2017/{i}/closure/event_contents.npy"

    print(f"start {npy_path}")
    if os.path.isfile(npy_path):
        evt_dict = numpy.load(npy_path, allow_pickle=True)[()]
        for key in evt_dict:
            print(key,evt_dict[key])
    else:
        print(f"{npy_path} is not exist.")


