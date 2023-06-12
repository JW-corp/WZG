
## 1. Applying fake-lepton uncertainty

### Three uncertainties in fakelepton 
 1. FakeRate systematic uncertainty
 2. FakeRate statistical uncertainty
 3. WZG SR FakeLepton statistical uncertainty (bin) 

### 1. FakeRate Sys & Stat uncertainty Module
- [FakeRate Sys/Stat Unc module](https://github.com/JW-corp/WZG/blob/main/NanoAOD/local_condor_run/modules/FakeLep_Apply_weight_Template_Module.py)
- [FakeRate Sys/Stat Unc post-proc](https://github.com/JW-corp/WZG/blob/main/NanoAOD/local_condor_run/post_proc/Apply_weight_Template_postproc.py)

### 2. Applying and Plotting FakeLepton Unc
- https://github.com/JW-corp/WZG/tree/main/AQGC/Plot



## Applying btag SF and uncertainty
  1. Making btag EF 2-d histogram (lookup table) : [btag Eff maker moduel](https://github.com/JW-corp/WZG/blob/main/NanoAOD/local_condor_run/modules/btagEffProducer.py)
  2. Applying btag SF and making branch for btag-weight : [btag SF](https://github.com/JW-corp/WZG/blob/main/NanoAOD/local_condor_run/modules/btagSFProducer.py), [btag weight](https://github.com/JW-corp/WZG/blob/main/NanoAOD/local_condor_run/modules/btagWeightProducer_1a.py)
  3. Post-processor to run 1 and 2 : [post-proc](https://github.com/JW-corp/WZG/blob/main/NanoAOD/local_condor_run/post_proc/WZG_postproc.py)
  - Please note that you should run separately 1. and 2. The output of 1 should the input of 2.
 
