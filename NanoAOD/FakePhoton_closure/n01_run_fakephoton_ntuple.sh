#!/bin/bash


# --> True template uncertainty
 
# --2016
#python n01_FakePhoton_CR_template_Ntuple_2016.py data False 2>&1 | tee log_data  
#python n01_FakePhoton_CR_template_Ntuple_2016.py real False 2>&1 | tee log_real  &
#python n01_FakePhoton_CR_template_Ntuple_2016.py fake False 2>&1 | tee log_fake  &


# --2017
#python n01_FakePhoton_CR_template_Ntuple_2017.py data False 2>&1 | tee log_data  &
#python n01_FakePhoton_CR_template_Ntuple_2017.py real False 2>&1 | tee log_real  &
#python n01_FakePhoton_CR_template_Ntuple_2017.py fake False 2>&1 | tee log_fake  &

# --2018
#python n01_FakePhoton_CR_template_Ntuple_2018.py data False 2>&1 | tee log_data  &
python n01_FakePhoton_CR_template_Ntuple_2018.py real False 2>&1 | tee log_real  &
#python n01_FakePhoton_CR_template_Ntuple_2018.py fake False 2>&1 | tee log_fake  &

# --> Closure test

# --2016
#python n01_FakePhoton_CR_template_Ntuple_2016.py data True 2>&1 | tee log_data 
#python n01_FakePhoton_CR_template_Ntuple_2016.py real True 2>&1 | tee log_real &
#python n01_FakePhoton_CR_template_Ntuple_2016.py fake True 2>&1 | tee log_fake &


# --2017
#python n01_FakePhoton_CR_template_Ntuple_2017.py data True 2>&1 | tee log_data &
#python n01_FakePhoton_CR_template_Ntuple_2017.py real True 2>&1 | tee log_real &
#python n01_FakePhoton_CR_template_Ntuple_2017.py fake True 2>&1 | tee log_fake &

# --2018
#python n01_FakePhoton_CR_template_Ntuple_2018.py data True 2>&1 | tee log_data &
#python n01_FakePhoton_CR_template_Ntuple_2018.py real True 2>&1 | tee log_real &
#python n01_FakePhoton_CR_template_Ntuple_2018.py fake True 2>&1 | tee log_fake &
