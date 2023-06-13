#!/bin/bash
python run_fit.py  EB_PT1  2>&1 | tee log1 &
python run_fit.py  EB_PT2 2>&1 | tee log2 &
python run_fit.py  EB_PT3 2>&1 | tee log3 &
python run_fit.py  EB_PT4 2>&1 | tee log4 &
python run_fit.py  EB_PT5  2>&1 | tee log5 &
python run_fit.py  EE_PT1 2>&1 | tee log6 &
python run_fit.py  EE_PT2 2>&1 | tee log7 &
