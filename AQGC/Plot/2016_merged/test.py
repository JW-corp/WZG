import awkward as ak


# Make test array
j1 = (1<<0) | (1<<1)  # med
j2 = (1<<0) # loose 
j3 = (1<<0) | (1<<1) | (1<<2) # tight
arr = ak.Array([[j1],[j2,j3]]) 


# tight  cut
btag_bit = (1<<0) | (1<<1) | (1<<2)

# test ~>>
print("arr: ",arr)

mask = arr & btag_bit == btag_bit
print("mask: ",mask)

arr = arr[mask]
print("applied",arr)





