from bs4 import BeautifulSoup
import pandas as pd
import json

from selenium import webdriver
from time import sleep
import io

from datetime import datetime
# list of columns received ==> total is 9 columns
col=['Close Price','Last Trade Vol','Change Value','Change %','No of Trades','Total Volume','Bid Price','Bid Vol','Offer Price']
# delay timer to allow for the browser to connect and download results in seconds
delayTimer=20

def readFile(fname):
	with open(fname,'r') as fr:
		data=fr.read()	
	soup = BeautifulSoup(data)
	return soup	

def readHteml(group,soup):	
	

	Lmod=[]
	rowsGeneral= soup.findAll('tr', {'class': group})
	for m in rowsGeneral:
		d=m.text
		Lmod.append(d.strip().split('\n'))
	return (Lmod)	


def getDFStockPrices(groups,fname):
	soup=readFile(fname)
	stockList=[]
	for group in groups:
		stockList.append(readHteml(group,soup))
	data=[]
	for group in stockList:
		for line in group:
			data.append(line)
	stockPrices=pd.DataFrame(data)	
	return stockPrices

def getDfStockPricesAll(fname):
	groups=["odd group-item group-item-energy","even group-item group-item-energy",\
		"odd group-item group-item-materials","even group-item group-item-materials",\
		"odd group-item group-item-capital-goods","even group-item group-item-capital-goods",\
		"odd group-item group-item-commercial-amp-professional-svc","even group-item group-item-commercial-amp-professional-svc",\
		"odd group-item group-item-transportation","even group-item group-item-transportation"\
		"odd group-item group-item-consumer-durables-amp-apparel","even group-item group-item-consumer-durables-amp-apparel",\
		"odd group-item group-item-consumer-services","even group-item group-item-consumer-services",
		"odd group-item group-item-media","even group-item group-item-media",\
		"odd group-item group-item-retailing","even group-item group-item-retailing",\
		"odd group-item group-item-food-amp-staples-retailing","even group-item group-item-food-amp-staples-retailing",\
		"odd group-item group-item-food-amp-beverages","even group-item group-item-food-amp-beverages",
		"odd group-item group-item-health-care-equipment-amp-svc","even group-item group-item-health-care-equipment-amp-svc",\
		"odd group-item group-item-pharma-biotech-amp-life-science","even group-item group-item-pharma-biotech-amp-life-science",\
		"odd group-item group-item-banks" ,"even group-item group-item-banks",\
		"odd group-item group-item-diversified-financials","even group-item group-item-diversified-financials",\
		"odd group-item group-item-insurance","even group-item group-item-insurance",\
		"odd group-item group-item-telecommunication-services","even group-item group-item-telecommunication-services",\
		"odd group-item group-item-utilities","even group-item group-item-utilities",\
		"odd group-item group-item-reits","even group-item group-item-reits",\
		"odd group-item group-item-real-estate-mgmt-amp-dev-t","even group-item group-item-real-estate-mgmt-amp-dev-t"]
	return getDFStockPrices(groups,fname)


def genStockCsc(file,fr):
	df=getDfStockPricesAll(fr)
	with open(file,'w') as fw:
		df.to_csv(fw,index=False)		



def dowloadTasiStocks(fname):
	ur='https://www.tadawul.com.sa/wps/portal/tadawul/markets/equities/market-watch'
	browser=webdriver.Firefox(executable_path=r'C:\Users\qatsh\geckodriver.exe')
	browser.get(ur)
	sleep(delayTimer)
	data=browser.page_source
	browser.close()
	with io.open(fname, "w", encoding="utf-8") as f:
	    f.write(data)


def genDFStock(fname):
	df2=pd.read_csv(fname)
	df2.drop(['1'],axis=1,inplace=True)
	df2.set_index(df2['0'],inplace=True)
	df2.drop(['0'],axis=1,inplace=True)
	#col=['Close Price','Last Trade Vol','Change Value','Change %','No of Trades','Total Volume','Bid Price','Bid Vol','Offer Price']
	df2.columns=col
	m='Last Trade Vol'
	df2[m]= df2[m].str.replace(',', '')
	m='No of Trades'
	df2[m]= df2[m].str.replace(',', '')
	m='Total Volume'
	df2[m]= df2[m].str.replace(',', '')
	m='Bid Vol'
	df2[m]= df2[m].str.replace(',', '')
	df2=df2.astype('float')
	df2['score_ranked']=df2['Change %'].rank(ascending=1)
	df2.sort_values('score_ranked', inplace=True)
	return df2

def genJsonStock(fname):
	df2=pd.read_csv(fname)
	df2.drop(['1'],axis=1,inplace=True)
	df2.set_index(df2['0'],inplace=True)
	df2.drop(['0'],axis=1,inplace=True)
	#col=['Close Price','Last Trade Vol','Change Value','Change %','No of Trades','Total Volume','Bid Price','Bid Vol']
	df2.columns=col
	m='Last Trade Vol'
	df2[m]= df2[m].str.replace(',', '')
	m='No of Trades'
	df2[m]= df2[m].str.replace(',', '')
	m='Total Volume'
	df2[m]= df2[m].str.replace(',', '')
	m='Bid Vol'
	df2[m]= df2[m].str.replace(',', '')
	df2=df2.astype('float')
	d3={}
	status=True
	for c in df2.index:		
		d1=dict(df2.loc[c])
		'''
		# there is dublicate ticker/row in Tadawul list which causes and issue when try to 
		# generate json file. Can not get json file for now, try to rename the ticker after download

		if (c=='SCC' and status==True):
			df.loc[c]
			c='SCC1'
			status=False
		'''	
		d2=dict([(c,d1)])
		d3.update(d2)
	return d3
def saveJsonStockFile(fname,data):
	with open(fname,'w') as fw:
		dataJson=json.dumps(data)
		fw.write(dataJson)

if __name__ == "__main__":
	fname='test2.html'  # name to downloaded html file
	dowloadTasiStocks(fname)
	#fr='test.html'
	fr=fname
	date=str(datetime.now().date())

	file='TASI-'+date+'.csv'  # date stamp file generated (one file per day)
	genStockCsc(file,fr)


	d3=genJsonStock(file)

	#fnameJson='stocks.json'

	#saveJsonStockFile(fnameJson,d3)


	#print(d3['samba'])
	df4=genDFStock(file)   # get list in dataframe format and sort 
	print(df4.head())	#print out top losers

