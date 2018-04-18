import pandas as pd

df=pd.read_csv('TasiCompanyList.csv')

print (df.head())
df.set_index('COMPANY',inplace=True)
print (df.head())
print(df.loc['samba':'ARNB',['SYMBOL']])

tickers=df.loc['samba':'ARNB',['SYMBOL']].values

print (tickers)