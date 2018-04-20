from selenium import webdriver
import datetime
from time import sleep
import io

delayTimer=30 # delay timer in seconds

def dowloadTasiStocks(fname,ur):	
	browser=webdriver.Firefox(executable_path=r'C:\Users\qatsh\geckodriver.exe')
	browser.get(ur)
	sleep(delayTimer)
	data=browser.page_source
	browser.close()
	with io.open(fname, "w", encoding="utf-8") as f:
	    f.write(data)

if __name__ == "__main__":
	timeStamp=datetime.datetime.now()
	country='sa'

	countries=['sa','ae','om','eg']
	#countries=['sa']
	listType='all-stock-prices'
	for country in countries:
		fname=country+'StocksPrices.html'	
		ur='https://english.mubasher.info/countries/'+country+'/'+listType
		dowloadTasiStocks(fname,ur)
		print (country)
			
	