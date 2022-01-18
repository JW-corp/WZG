## Make gridpack of WZG aQGC samples
  
###1 SetUp CMS Environment
   
```bash
source /x5/cms/jwkim/Generator/Genproduction/cmsset
```
  
###2 Install GenProduction

```bash
source /x5/cms/jwkim/Generator/Genproduction/prepare_gen_production.sh PATH_OF_WORKING_DIRECTORY
```
  
###3 Access MG5 directory
```bash
cd /PATH_OF_WORKING_DIRECTORY/genproductions/bin/MadGraph5_aMCatNLO/
```
  
###4 Set up MG5 cards
```bash
mkdir cards/WZAToLNuLLA_LO_QCKM
cd cards/WZAToLNuLLA_LO_QCKM
#Copy WZAToLNuLLA_LO_QCKM_extramodels.dat  WZAToLNuLLA_LO_QCKM_madspin_card.dat  WZAToLNuLLA_LO_QCKM_proc_card.dat  WZAToLNuLLA_LO_QCKM_run_card.dat  here
```
  
###5 Launch
```bash
./gridpack_generation.sh WZAToLNuLLA_LO_QCKM cards/WZAToLNuLLA_LO_QCKM 2>&1 | tee MyAQGC_model.log
```


