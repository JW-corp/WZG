### How to calculate aQGC deltaNLL using HiggsCombined tool?

1. make_aqgc_datacard.sh, Combine_help.py : Make data-card which is used as a input of HiggsCombined tool
2. FT0_card_SR_mZA_bin4.txt : sample data card
3. pickle_to_npy.py : Fit-function (SM/aQGC ratio)
4. run.sh : Run HiggsCombined tool (input: sample datacard and fit-function npy file)
5. plot_Nll.py : Plot deltaNLL distribution
