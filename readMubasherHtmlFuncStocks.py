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
	
	stock=stocksList[0]
	#print (stock)
	fullList=[]
	for stock in stocksList:
		valPrice='number ng-binding'
		valName='nowrap'
		price=stock.findAll('td', {'class': valPrice})
		name=stock.find('td', {'class': valName})
		valChangePerc='number ng-binding'
		changePercent=stock.find('td', {'class': valChangePerc})
		
		
		#print (name.text.strip(),price[0].text,price[1].text.strip())
		
		d=[name.text.strip(),price[0].text,price[1].text.strip()]
		valChange='mi-hide-for-small number ng-binding'

		change=stock.findAll('td', {'class': valChange})

		#print (change)	
		for c in change:
			#print (c.text)
			d.append(c.text)
		fullList.append(d)	
	print (d)

	#items=[]
	#values=[]
	#d2={}

	'''
	for market in marketBlock:
		item=market.find('span', {'class': val1})
		value=market.find('span', {'class': item1})
	'''
	dfinal=10
	return dfinal

'''
	companyName=soup.find('h1', {'class': val1})
	d0=dict([('Company Name',companyName.text)])
	val1='company-profile__general-information__text2'	
	companyProfile=soup.findAll('span', {'class': val1})	
	companyName=companyProfile[0].text
	companyDescription=companyProfile[1].text
	print (companyDescription)
	d1=dict([('Description',companyDescription)])
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
'''


def saveJsonFile(file,d):
	dJson=json.dumps(d)
	with open(fname, "w") as fw:
		fw.write(dJson)
	

if __name__ == "__main__":
	
	fname='TasiStocksPrices'
	d1=readMubasherDataStocks(fname)
	
	#fname=ticker+"-Desc.json"
	#saveJsonFile(fname,d1)
	