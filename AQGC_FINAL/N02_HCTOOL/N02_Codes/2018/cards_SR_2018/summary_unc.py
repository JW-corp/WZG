unc_source = "input.txt"

import pandas as pd

df = pd.read_csv(unc_source, sep='\s+')

df.set_index('process',inplace=True)

df.drop(columns=['type'],inplace=True)

df = df.apply(pd.to_numeric, errors='coerce')


print(df)
with open('Unc_summary.csv', 'w') as f:
    f.write('Uncertainty, Min, Max, Min(%), Max(%)\n')
    for uncname in df.index:
        idxmin=df.loc[uncname].idxmin()
        uncmin=(df.loc[uncname].min() -1)*100
        idxmax=df.loc[uncname].idxmax()
        uncmax=(df.loc[uncname].max() -1)*100
        print(f"{uncname} : {idxmin} ,  {idxmax},  {uncmin:.3f} , {uncmax:.3f}")
        f.write(f"{uncname} , {idxmin} ,  {idxmax},  {uncmin:.3f} , {uncmax:.3f}\n")

