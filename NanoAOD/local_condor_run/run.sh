

# Test for tutorial (2018)
#python run_condor.pt -f jsons/input_mc_test_2018.json


# Private test
#python run_condor.py -f jsons/AR_2016_test.json -y 2016_preVFP -isFake True



# Conmbined (2018)
#python run_condor.py -f jsons/input_mc2018.json
#python run_condor.py -f jsons/input_data2018.json

#python run_condor.py -f jsons/input_mc_test_2018.json -y 2016
#python run_condor.py -f jsons/input_mc_test_2018.json -y 2016_preVFP




## FakePhoton
#python run_condor.py -f jsons/AR_input_2016preVFP.json -y 2016_preVFP -isFake True
#python run_condor.py -f jsons/AR_input_2016postVFP.json -y 2016 -isFake True


## FakeLepton

##FR
#python run_condor_FakeLep.py -f jsons/FR_input_2016preVFP.json -y 2016_preVFP -isFakeFR True
python run_condor_FakeLep.py -f jsons/FR_input_2016postVFP.json -y 2016 -isFakeFR True

##AR
#python run_condor_FakeLep.py -f jsons/AR_input_2016preVFP.json -y 2016_preVFP -isFakeAR True
#python run_condor_FakeLep.py -f jsons/AR_input_2016postVFP.json -y 2016 -isFakeAR True





##  Data
# preVFP

#python run_condor.py -f jsons/input_data2016_pre.json -y 2016_preVFP


# postVFP
#python run_condor.py -f jsons/input_data2016_post.json -y 2016



## MC
# preVFP
#python run_condor.py -f jsons/input_mc2016_pre.json -y 2016_preVFP


#postVFP
#python run_condor.py -f jsons/input_mc2016_post.json -y 2016
