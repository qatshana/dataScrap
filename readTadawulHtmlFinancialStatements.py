from bs4 import BeautifulSoup
import pandas as pd
import json

from selenium import webdriver
from time import sleep
import io

from datetime import datetime



def readFile(fname):
	with open(fname,'r') as fr:
		data=fr.read()	
	soup = BeautifulSoup(data,"html.parser")
	return soup	

def getSpecificStateRow(rowsState,lineList):
	
	for row in rowsState:
		items= row.findAll('td')
		rowList=[]		
		for item in items:
			rowList.append(item.text)
		lineList.append(rowList)	
	return lineList		

def processStatment(filename,tableName):
	fname=filename+'.html'
	soup=readFile(fname)	
	table=soup.find('table',{'id':tableName})
	rowsStateeven= table.findAll('tr', {'role': 'row'} and {'class': 'even'} )
	rowsStateOdd= table.findAll('tr', {'role': 'row'} and {'class': 'odd'})
	lineList=[]
	rowsState=rowsStateOdd
	lineList=getSpecificStateRow(rowsState,lineList)
	rowsState=rowsStateeven
	lineList=getSpecificStateRow(rowsState,lineList)
	df=pd.DataFrame(lineList)
	col=['item','2017','2016','2015','2014']
	df.columns=col
	df.to_csv(filename+'.csv',index=False)	


if __name__ == "__main__":

	#fn='SARCO'
	#fn='Aldrees'
	fn='SCC1'
	fileName=fn+'-BS'
	tableName='statementsTable0'
	processStatment(fileName,tableName)
	fileName=fn+'-IS'
	tableName='statementsTable1'
	processStatment(fileName,tableName)

