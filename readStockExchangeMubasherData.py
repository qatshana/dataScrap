import readMubasherHtmlFunc as rm
import json
import pandas as pd 

#exchanges=['sa','ae','eg','om']
exchanges=['sa']
#tickers=['DIB']
#tickers=['1090']
#tickers=['COMI']
#dataList=[]

'''
for exchange in exchanges:
	date='-2018-04-22-'
	fname=exchange+'StocksPrices.json'
	dictData=rm.readFileJson(fname)

	#print (dictData['Shuaa'])
	print (dictData['ARNB'])
'''
with open('eg-2018-04-22-StocksPrices.json','r') as fr:
    data=fr.read()

d=json.loads(data)
print (d['COMI'])


df=pd.read_csv('eg-2018-04-22-StocksPrices.csv')

df.drop('Unnamed: 0',axis=1,inplace=True)

df.set_index('Ticker',inplace=True)

print(df.loc['COMI'])

print(df.head(10))

print(df.tail(5))



df=pd.read_csv('sa-2018-04-22-StocksPrices.csv')

df.drop('Unnamed: 0',axis=1,inplace=True)

df.set_index('Ticker',inplace=True)


print(df.head(10))

print(df.tail(10))