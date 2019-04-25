from selenium import webdriver
import time
 
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
options.binary_location = "/usr/bin/chromium-browser"
driver = webdriver.Chrome(chrome_options=options)
driver.get('http://127.0.0.1/grillen')
