import pandas as pd


infile1 = "fit_out_images_AfterFit_WZG18/fake_fraction.csv"
df1 = pd.read_csv(infile1,header=None,delimiter=r"\s+",names=['region','fake_fraction','statunc'])
df1 = df1.sort_values(by=['region'])

infile2 = "fit_out_images_AfterFit_ZG18/fake_fraction.csv"
df2 = pd.read_csv(infile2,header=None,delimiter=r"\s+",names=['region','fake_fraction','statunc'])
df2 = df2.sort_values(by=['region'])


numerator   = df2['fake_fraction'] - df1['fake_fraction']
denorm		= df2['fake_fraction'] + df1['fake_fraction']
real_tmp_unc = numerator/denorm


print("========= WZG")
print(df1)
print("========= ZG")
print(df2)
#df = pd.DataFrame({'Region':df1['region'], 'Unc': real_tmp_unc})
#print(df)
