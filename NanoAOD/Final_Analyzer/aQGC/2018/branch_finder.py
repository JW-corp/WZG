import uproot 


file = "aQGC_2018.root"


key = ["*aQGC*"]
keys = uproot.open(f'{file}').keys(filter_name=key)
for k in keys:
	print(k)
#print(tree.keys())
