from bs4 import BeautifulSoup
import pandas as pd
import json
from selenium import webdriver
from time import sleep
import io
from datetime import datetime

def readFile(fname):
	with io.open(fname, "r", encoding="utf-8") as fr:
		data=fr.read()	
	soup = BeautifulSoup(data,"html.parser")
	return soup	

def readFileJson(fname):	
	with open(fname, "r") as fr:
		data=fr.read()
	dictData=json.loads(data)
	return dictData

def readMubasherDataStocks(name):
	fname=name+'.html'
	soup=readFile(fname)
	val1='ng-scope'
	stocksList=soup.findAll('tr', {'class': val1})
	fullList=[]
	dFinal={}
	for stock in stocksList:
		valPrice='number ng-binding'
		valName='nowrap'
		price=stock.findAll('td', {'class': valPrice})
		d1=dict([('Close Price',price[0].text)])
		name=stock.find('td', {'class': valName})
		# get ticker from link
		tickerTxt=stock.find('a', {'class': 'ng-binding'})
		tickerLink=tickerTxt.attrs['href'].split('/')
		ticker=tickerLink[len(tickerLink)-1]	
		d2=dict([('Change %',price[1].text.strip())])
		d1.update(d2)
		#d3=dict([(name.text.strip(),d1)])
		d3=dict([(ticker,d1)])
		dFinal.update(d3)	
		#d=[name.text.strip(),price[0].text,price[1].text.strip()]
		d=[ticker,name.text.strip(),price[0].text,price[1].text.strip()]
		valChange='mi-hide-for-small'
		change=stock.findAll('td', {'class': valChange})
		for c in change:
			d.append(c.text)
		fullList.append(d)		
	return (fullList,dFinal)

def saveJsonFile(fname,d):
	dJson=json.dumps(d)
	with open(fname, "w") as fw:
		fw.write(dJson)
	
if __name__ == "__main__":	
	exchange='sa'
	exchanges=['sa','ae','om','eg']
	date='-2018-04-22-'
	for exchange in exchanges:
		fname=exchange+date+'StocksPrices'
		(stocksList,stocksListDict)=readMubasherDataStocks(fname)
		rowList=['Ticker','Name','Close Price', 'Change %', 'Empty','Traded Value',  'Volume', 'Bid Price', 'Day High', 'Day Low','Date']
		df1=pd.DataFrame(stocksList)
		df1.columns=rowList
		df1.drop('Empty',axis=1,inplace=True)	
		fileCsv=fname+'.csv'
		df1.to_csv(fileCsv)
		print('Done with '+ exchange)
		fileJson=fname+'.json'
		saveJsonFile(fileJson,stocksListDict)
