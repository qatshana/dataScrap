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
	soup = BeautifulSoup(data)
	return soup	

def readFile2(fname):
	with open(fname, "r") as fr:
		data=fr.read()	
	soup = BeautifulSoup(data)
	return soup	



if __name__ == "__main__":
	#tickers=['1090','1050','1040','1020','1010','1060','1080','1120','2190','2030','2150','6010','6020','6040','4010','2160','3010','3020','2170','3030','3040','3050','3060','3080','3090','2180','2010','2020','2200']	
	#tickers=['1090']
	#tickers=['DIB']
	tickers=['COMI']
	for ticker in tickers:
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
		print (companyDescription)
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
					print(number.text)
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
				print(mgrName.text,mgrTitle.text)
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
		print (dfinal)
		dfinalJson=json.dumps(dfinal)
		fname=ticker+"-Desc.json"
		with open(fname, "w") as fw:
			fw.write(dfinalJson)				
		'''
		read stocks.html to get outstanding shares
		'''	
		#fname='stock.html'  # name to downloaded html file		
		fname=ticker+'-Stock.html'
		soup=readFile2(fname)
		

		val1='stock-overview__text-and-value-item'
		stockList=soup.find_all('div', {'class': val1})	
		d20={}
		for stock in stockList:
			itemName=stock.find('span', {'class': 'stock-overview__text'})
			itemValue=stock.find('span', {'class': 'number number--aligned'})
			if (itemValue!=None):
				print (itemName.text,itemValue.text)
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

		dfinalJson=json.dumps(dfinal)
		fname=ticker+'-FullData.json'
		with open(fname, "w") as fw:
			fw.write(dfinalJson)		