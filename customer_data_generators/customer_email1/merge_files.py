import pandas as pd

df_crm = pd.read_csv('output/crm.csv')
df_email = pd.read_csv('output/email.csv')

dfconcated = pd.concat([df_crm,df_email],axis=0,ignore_index=True)
dfconcated.to_csv('output/crm_email.csv',index=False)