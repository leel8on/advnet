#!/usr/bin/python2

from selenium import webdriver
options = webdriver.ChromeOptions()
options.binary_location = '/usr/bin/chromium-browser'
options.add_argument('headless')
driver=webdriver.Chrome(chrome_options=options)
driver.get("http://www.google.com")
performance_data = driver.execute_script("return window.performance.getEntries();")
print (performance_data)
