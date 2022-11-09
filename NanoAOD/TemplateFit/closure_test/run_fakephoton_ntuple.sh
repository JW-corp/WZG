#!/bin/bash

python FakePhoton_CR_template_Fit_2016.py data 2>&1 | tee log_data &
python FakePhoton_CR_template_Fit_2016.py real 2>&1 | tee log_real &
python FakePhoton_CR_template_Fit_2016.py fake 2>&1 | tee log_fake &
