from selenium import webdriver
from time import sleep
import io
from datetime import datetime
delayTimer=20

def dowloadTasiStocks(fname):
	ur='https://www.tadawul.com.sa/wps/portal/tadawul/markets/equities/market-watch'
	browser=webdriver.Firefox(executable_path=r'C:\Users\qatsh\geckodriver.exe')
	browser.get(ur)
	sleep(delayTimer)
	data=browser.page_source
	browser.close()
	with io.open(fname, "w", encoding="utf-8") as f:
	    f.write(data)

if __name__ == "__main__":
	#fname='test2.html'
	date=str(datetime.now().date())
	fname='TASI-'+date+'.html'  # date stamp file generated (one file per day)
	dowloadTasiStocks(fname)
	
