from selenium import webdriver
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
	#tickers=['1090','1050','1040','1020','1010','1060','1080','1120','2190','2030','2150','6010','6020','6040','4010','2160','3010','3020','2170','3030','3040','3050','3060','3080','3090','2180','2010','2020','2200']
	#tickers=['1090']
	#exchange='TDWL'
	# Dubai
	tickers=['DIB']
	exchange='DFM'
	#Egypt
	tickers=['COMI']
	exchange='EGX'

	for ticker in tickers:
		#ticker='4011'
		fname=ticker+'-Profile.html'
		ur='https://english.mubasher.info/markets/'+exchange+'/stocks/'+ticker+'/profile'
		dowloadTasiStocks(fname,ur)
		
		fname=ticker+'-Stock.html'
		ur='https://english.mubasher.info/markets/'+exchange+'/stocks/'+ticker
		dowloadTasiStocks(fname,ur)
