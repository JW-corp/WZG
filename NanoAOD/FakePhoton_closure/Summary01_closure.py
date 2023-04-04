import pandas as pd






def summary_unc(mypath):
	df = pd.read_csv(mypath,header=None,names=['Iso_low','Iso_high','Unc','True_Fake_Yield','Estimated_Fake_Yield'],delimiter=r"\s+")
	df = df.sort_index()
	print(df)


path_16= "N01_Closure_test_results/fit_out_images_AfterFit_16/closure.csv"
path_17= "N01_Closure_test_results/fit_out_images_AfterFit_17/closure.csv"
path_18= "N01_Closure_test_results/fit_out_images_AfterFit_18/closure.csv"

summary_unc(path_16)
summary_unc(path_17)
summary_unc(path_18)