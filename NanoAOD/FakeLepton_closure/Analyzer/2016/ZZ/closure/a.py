import numpy as np

# open event_contents.npy
evt_dict = np.load("event_contents.npy", allow_pickle=True).item()
print(evt_dict)