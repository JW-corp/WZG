### How to apply *restrict file* in gen-production

- Prepare the restrict card.
- Add import model SMEFTsim_U35_MwScheme_UFO-WZA_WToLNu_LOaQGC_dim6 in proc card. Note that the naming rule. 
- Prepare extramodels.dat (I uesd the default model) : The purpose of this card is to active if statement in Line 247 of gridpack_generation.sh 
- Modify gridpack_generation.sh : Line 267
