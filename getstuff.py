#!/usr/bin/python2

from selenium import webdriver
options = webdriver.ChromeOptions()
options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
options.add_argument('headless')
driver=webdriver.Chrome('/Users/TheCmar7/Downloads/chromedriver', chrome_options=options)
driver.get("https://advnet.l8on.org:443")
performance_data = driver.execute_script("return window.performance.getEntries();")
print (performance_data[0][u'startTime'])
for x in range(0,len(performance_data)):
	print(performance_data[x]);
