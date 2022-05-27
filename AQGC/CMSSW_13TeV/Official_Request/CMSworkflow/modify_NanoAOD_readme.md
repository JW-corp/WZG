```bash
cd CMSSW_10_6_26/src
git-cms-init
git cms-addpkg PhysicsTools/NanoAOD
```
  
### modify PhysicsTools/NanoAOD/Plugin/GenWeightsTableProducer.cc
  
```
if (groupname == “mg_reweighting”) {
—>
if (groupname.find(“mg_reweighting”) != std::string::npos) {
```





