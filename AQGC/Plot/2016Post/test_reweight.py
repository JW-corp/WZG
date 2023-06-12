import uproot


#infile = "/cms/ldap_home/jwkim2/New_ccp/aQGC/dim8/LLWA_aQGC_UL16Post_Skim.root"
#infile = "/cms/ldap_home/jwkim2/New_ccp/aQGC/dim8/LLWA_aQGC_UL16Pre_Skim.root"
infile = "/cms/ldap_home/jwkim2/New_ccp/aQGC/dim8/LLWA_aQGC_UL16_Skim.root"



arr    = uproot.open(infile+":/Events")["LHEReweightingWeight"].array()
print(arr)


