import pandas as pd

df2=pd.read_csv('TasiCompanyList.csv')
df2.set_index('COMPANY',inplace=True)
tickers=[]
for t in df2.index:
    txt=str(df2.loc[t]['SYMBOL'])
    tickers.append(txt)


print (tickers)
print (len(tickers))
