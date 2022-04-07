import pandas as pd
import subprocess



file_name = "FT0.csv"
base_dir  = "datacard/"
out_name  = file_name.split('.')[0] 
out_path  = base_dir + out_name + '.txt'
out_csv_name = out_name+'limit.csv'

df = pd.read_csv(base_dir + file_name)
df = df.reset_index()


args = 'echo' + ' ' + 'name' + ' ' + ' ' + 'm2' + ' ' + 'm1' + ' ' + 'median'  + ' ' + 'p1' + ' ' + 'p2' + ' ' + '>' + ' ' + out_csv_name 
subprocess.call(args,shell=True)

for idx,row in df.iterrows():

	if idx==0:
		sm_yield = row['yield']
		continue
	


	args = './' + 'make_data_card.sh' + ' ' + str(row['name']) + ' ' + str(row['yield']) + ' '+  str(sm_yield) + ' ' + out_csv_name
	subprocess.call(args,shell=True)
	

