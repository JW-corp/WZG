### How to run HCtool (aQGC expected confidence interval case)

1. First, you need to preapre root file that contain all of up/down weights to calculate following uncertainties (In this case aQGC_2018.root)
2. Prepare combine.json (basic info about calculating limit, ex bin...), combine_AQGC.csv (list of systematic sources)
3. Prepare datacard which is input of HC tool . --> Automate this using 1. and 2. Automated code is Combine_help.py
4. Check datacard cards_SR_2018/aQGC_card_SR_mlllA_bin2.txt
5. Run HCtool (confidence interval) N02_run_fit.sh 
6. Plot interval N03_plot_Nll.py 
