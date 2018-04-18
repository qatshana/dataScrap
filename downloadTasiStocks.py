from selenium import webdriver
from time import sleep
import io

def dowloadTasiStocks(fname):
	ur='https://www.tadawul.com.sa/wps/portal/tadawul/markets/equities/market-watch'
	browser=webdriver.Firefox(executable_path=r'C:\Users\aqatshan\geckodriver.exe')
	browser.get(ur)
	sleep(10)
	data=browser.page_source
	browser.close()
	with io.open(fname, "w", encoding="utf-8") as f:
	    f.write(data)

if __name__ == "__main__":
	fname='test2.html'
	dowloadTasiStocks(fname)
	
