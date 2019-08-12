import pandas as pd 

df=pd.read_csv('mutcd.csv')
list_to_copy=[str(i) for i in df['mutcd'] ]
print(list_to_copy)