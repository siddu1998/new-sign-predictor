import pandas as pd 


df_gis=pd.read_csv('FL_20180804_I75NB.csv')
df_sign_inv=pd.read_csv('SignInventory_2015.csv')

object_id_list=df_gis["OBJECTID"].tolist()
print(object_id_list)
