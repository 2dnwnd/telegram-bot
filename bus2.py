import time
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import tokenid

id = tokenid.user_id
pw = tokenid.user_pw


browser = webdriver.Chrome()
# browser.get('https://map.naver.com/v5/bus/bus-route')
browser.get('https://www.naver.com/')
time.sleep(1)

# elem = browser.find_element_by_xpath('//*[@id="container"]/shrinkable-layout/div/bus-home/div[1]/bus-search/div/div/div/div/div')
# elem.click()
# elem.send_keys(bus)
# elem.send_keys(Keys.ENTER)

elem = browser.find_element_by_xpath('//*[@id="query"]')
elem.send_keys('31-7')
elem.send_keys(Keys.ENTER)

browser.find_element(By.XPATH, '//*[@id="cs_bus_realinfo"]/div[2]/div[2]/div/ul/li[1]/div[2]/a').click()