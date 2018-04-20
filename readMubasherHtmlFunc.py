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

def readFile2(fname):
	with open(fname, "r") as fr:
		data=fr.read()	
	soup = BeautifulSoup(data,"html.parser")
	return soup	
def readFileJson(fname):	
	with open(fname, "r") as fr:
		data=fr.read()
	dictData=json.loads(data)
	return dictData

def readMubasherDataProfile(ticker):
	fname=ticker+'-Profile.html'
	soup=readFile(fname)
	val1='mi-section__title'
	companyName=soup.find('h1', {'class': val1})
	d0=dict([('Company Name',companyName.text)])
	'''
	get company's name and description
	'''
	val1='company-profile__general-information__text2'	
	companyProfile=soup.findAll('span', {'class': val1})	
	companyName=companyProfile[0].text
	companyDescription=companyProfile[1].text
	#print (companyDescription)
	d1=dict([('Description',companyDescription)])

	'''
	Get market stats
	'''
	val1='market-summary__block-row'
	marketBlock=soup.findAll('div', {'class': val1})	
	val1='market-summary__block-text'
	item1='market-summary__block-number'
	items=[]
	values=[]
	d2={}
	for market in marketBlock:
		item=market.find('span', {'class': val1})
		value=market.find('span', {'class': item1})
		items.append(item.text)
		values.append(value.text)
		d2.update(dict([(item.text,value.text)]))	
	d3=dict([('Market Stats',d2)])

	'''
	get shareholders list
	'''
	shareHoldersTag='md-whiteframe-z1__nested'
	shareholders=soup.findAll('ul', {'class': shareHoldersTag})	
	shareholdersList=shareholders[0].find_all('li')
	names=[]
	numbers=[]
	for shareholder in shareholdersList:
			name=shareholder.find('span')			
			number=shareholder.find('span', {'class': 'number'})
			if (number!=None):
				names.append(name.text)
				numbers.append(number.text)
	d4=dict([('Shareholder Name',names)])
	d5=dict([('Shareholder Stake',numbers)])
	d6={}
	d6.update(d4)
	d6.update(d5)
	d7=dict([('Shareholders',d6)])

	'''
	get management list
	'''
	managementTag='company-profile__management md-whiteframe-z1__nested'
	management=soup.findAll('div', {'class': managementTag})
	managementTag2='company-profile__management__item'
	managementList=management[0].find_all('div', {'class': managementTag2})
	mgrNames=[]
	mgrTitles=[]
	for manager in managementList:
		mgrName=manager.find('span', {'class': 'company-profile__management__text1'})
		mgrTitle=manager.find('span', {'class': 'company-profile__management__text2'})
		if (mgrName!=None):
			mgrNames.append(mgrName.text)
			mgrTitles.append(mgrTitle.text)

	d8=dict([('Name',mgrNames)])
	d9=dict([('Title',mgrTitles)])
	d10={}
	d10.update(d8)
	d10.update(d9)
	d11=dict([('Management Team',d10)])	
	dfinal=d0
	dfinal.update(d1)
	dfinal.update(d3)
	dfinal.update(d7)
	dfinal.update(d11)				
	return (dfinal)	


def readMubasherDataStock(ticker,dfinal):	
	'''
	read stocks.html to get outstanding shares
	'''	
	fname=ticker+'-Stock.html'
	soup=readFile(fname)		
	val1='stock-overview__text-and-value-item'
	stockList=soup.find_all('div', {'class': val1})	
	d20={}
	for stock in stockList:
		itemName=stock.find('span', {'class': 'stock-overview__text'})
		itemValue=stock.find('span', {'class': 'number number--aligned'})
		if (itemValue!=None):
			d20.update(dict([(itemName.text,itemValue.text)]))
	
	val1='market-summary__last-price'
	closePrice=soup.find('div', {'class': val1}).text			
	d22=dict([('Close Price',closePrice)])
	val1='market-summary__change-percentage'
	priceChange=soup.find('div', {'class': val1})
	d24=dict([('Price Change %',priceChange.text)])
	d26=d22
	d26.update(d24)
	d26.update(d20)
	dfinal.update(d26)	
	return dfinal	

def saveJsonFile(file,d):
	dJson=json.dumps(d)
	with open(fname, "w") as fw:
		fw.write(dJson)
	

if __name__ == "__main__":
	#tickers=['1090','1050','1040','1020','1010','1060','1080','1120','2190','2030','2150','6010','6020','6040','4010','2160','3010','3020','2170','3030','3040','3050','3060','3080','3090','2180','2010','2020','2200']	
	#tickers=['1090']
	#tickers=['DIB']
	#tickers=['COMI']
	tickers=['1090', '1050', '1040', '1020', '1010', '1060', '1080', '1120', '2190', '2030', '2150', '6010', '6020', '6040', '4010', '2160', '3010', '3020', '2170', '3030', '3040', '3050', '3060', '3080', '3090', '2180', '2010', '2020', '2200', '2240', '2210', '2220', '2090', '2250', '2230', '2040', '2050', '2060', '2070', '2140', '2120', '2110', '2100', '2080', '4020', '4030', '4040', '4050', '4061', '4070', '4080', '4090', '4100', '4110', '4130', '4140', '4150', '4160', '4170', '4180', '4190', '5110', '7010', '6050', '6060', '6070', '6090', '1030', '2130', '8010', '7020', '1140', '2270', '2260', '2280', '2290', '4200', '4210', '2300', '2310', '4220', '4240', '2330', '2340', '2320', '4230', '8030', '2350', '8020', '8060', '8070', '8080', '8040', '4250', '8120', '8130', '8100', '8110', '8140', '8150', '2360', '4270', '8050', '4260', '4280', '8170', '8180', '8160', '4290', '2370', '4300', '2380', '7030', '1150', '8210', '8190', '8200', '1210', '1310', '6001', '4001', '7040', '1211', '2001', '1212', '2002', '4310', '6002', '3091', '3001', '3002', '6004', '8290', '8250', '8240', '8230', '8270', '1320', '8260', '8280', '4002', '1214', '1213', '8310', '8300', '1330', '1301', '4003', '8311', '1201', '8312', '3003', '1810', '4007', '4004', '3005', '4031', '3004', '4011', '4009', '3007', '4005', '1302', '1820', '8012', '1180', '8011', '9505', '4320', '1304', '1202', '9503', '1303', '4006', '4008', '9506', '9502', '9507', '9500', '9501', '9504', '9508']
	i=0
	for ticker in tickers:
		d1=readMubasherDataProfile(ticker)
		d2=readMubasherDataStock(ticker,d1)
		fname=ticker+"-Desc.json"
		saveJsonFile(fname,d1)
		fname=ticker+'-FullData.json'
		saveJsonFile(fname,d2)
		i+=1
		print(i)
