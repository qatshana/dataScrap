import readMubasherHtmlFunc as rm

#exchanges=['sa','ae','eg','om']
exchanges=['sa']
#tickers=['DIB']
#tickers=['1090']
#tickers=['COMI']
#dataList=[]
for exchange in exchanges:
	fname=exchange+'StocksPrices.json'
	dictData=rm.readFileJson(fname)

	#print (dictData['Shuaa'])
	print (dictData['ARNB'])