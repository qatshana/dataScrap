import readMubasherHtmlFunc as rm

tickers=['1090','1050','1040','1020','1010','1060','1080','1120','2190','2030','2150','6010','6020','6040','4010','2160','3010','3020','2170','3030','3040','3050','3060','3080','3090','2180','2010','2020','2200']
#tickers=['DIB']
#tickers=['1090']
#tickers=['COMI']
dataList=[]
for ticker in tickers:
	fname=ticker+'-FullData.json'
	dictData=rm.readFileJson(fname)

	print (dictData['Description'])

	#print (dictData['Market Stats']['Previous Close'])

	#print (dictData['P/B Ratio'])
	print (dictData['Company Name'],dictData['Market Cap'],dictData['Close Price'],dictData['Price Change %'])
	data=[dictData['Company Name'],dictData['Market Cap'],dictData['Close Price'],dictData['Price Change %']]
	dataList.append(data)
	#print (len(tickers))
	#print (dictData['Market Cap'])
print (dataList)