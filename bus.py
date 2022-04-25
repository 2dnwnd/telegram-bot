import time
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import tokenid

id = tokenid.user_id
pw = tokenid.user_pw

browser = webdriver.Chrome()
browser.get('https://map.naver.com')
time.sleep(3)

# 즐겨찾기 누르기
elem = browser.find_element(By.XPATH,'//*[@id="sidebar"]/navbar/perfect-scrollbar/div/div[1]/div/ul/li[6]/a')
elem.click()
time.sleep(3)

# 로그인하기
Id = browser.find_element(By.XPATH, '//*[@id="id"]')
Id.click()
pyperclip.copy(id)
Id.send_keys(Keys.CONTROL, 'v')
time.sleep(1)

password = browser.find_element(By.XPATH,'//*[@id="pw"]')
password.click()
pyperclip.copy(pw)
password.send_keys(Keys.CONTROL, 'v')
time.sleep(1)

browser.find_element(By.XPATH,'//*[@id="log.login"]').click()

# 버스누르고 31-7 누르기
browser.find_element(By.XPATH,'//*[@id="container"]/shrinkable-layout/div/favorite-layout/favorite-list/favorite-list-tab-area/div/div/a[3]').click()
browser.find_element(By.XPATH,'//*[@id="container"]/shrinkable-layout/div/favorite-layout/favorite-list/div/favorite-movement-bookmark-list/div/bus-list-item/div/a').click()

