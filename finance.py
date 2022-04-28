import requests
from bs4 import BeautifulSoup

url = 'https://finance.naver.com'
res = requests.get(url)
res.raise_for_status()

soup = BeautifulSoup(res.text, 'lxml')
kospi = soup.find('span',attrs={'class':'num_quot up'})
print('오늘 코스피 지수 :', kospi.get_text())

from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.headless = True
browser = webdriver.Chrome(options=options)
browser.get(url)

browser.find_element(By.XPATH, '//*[@id="content"]/div[1]/div[1]/div[2]/ul/li[2]/a')
print('-------상승율 TOP종목---------------------')
up_datas = soup.find('tbody',attrs={'id':'_topItems2'}).find_all('tr')
for idx, data in enumerate(up_datas):
    print(idx+1, data.get_text().strip())
    print()

print('------하락율 TOP종목----------------------')
browser.find_element(By.XPATH, '//*[@id="content"]/div[1]/div[1]/div[2]/ul/li[3]/a')
down_datas = soup.find('tbody',attrs={'id':'_topItems3'}).find_all('tr')
for idx, data in enumerate(down_datas):
    print(idx+1, data.get_text().strip())
    print()


print('-------시가총액 상위----------------------')
browser.find_element(By.XPATH, '//*[@id="content"]/div[1]/div[1]/div[2]/ul/li[4]/a')
top_datas = soup.find('tbody',attrs={'id':'_topItems4'}).find_all('tr')
for idx, data in enumerate(top_datas):
    print(idx+1, data.get_text().strip())
    print()