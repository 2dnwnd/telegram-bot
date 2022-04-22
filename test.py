from turtle import title
import telegram
import requests
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request as req
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


def create_soup(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
    res = requests.get(url,headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text,'lxml')
    return soup

def covid_image_crawling(image_num=5):
    if not os.path.exists("./코로나이미지"):
       os.mkdir("./코로나이미지")
 
    browser.implicitly_wait(10)
    wait = WebDriverWait(browser, 10)
    
    browser.get("https://search.naver.com/search.naver?where=image&section=image&query=%EC%BD%94%EB%A1%9C%EB%82%98&res_fr=0&res_to=0&sm=tab_opt&color=&ccl=0&nso=so%3Ar%2Cp%3A1d%2Ca%3Aall&datetype=1&startdate=&enddate=&gif=0&optStr=d&nq=&dq=&rq=&tq=")
    # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.photo_group._listGrid div.thumb img")))
    # img = browser.find_elements_by_css_selector("div.photo_group._listGrid div.thumb img")
    
    wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="main_pack"]/section[2]/div/div[1]/div[1]/div[1]/div/div[1]/a/img')))
    images = browser.find_elements(By.XPATH, '//img[@class="_image _listImage"]')

    for image in images:
        img_url = image.get_attribute("src")
        print(img_url)
        # req.urlretrieve(img_url, "./코로나이미지/{}.png".format(img.index(i)))
        image_res = requests.get(img_url)
        image_res.raise_for_status()
        with open('{}.png'.format(images.index(image)), 'wb') as f:
            if img_url == 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7':
                continue
            f.write(image_res.content)
            
        if images.index(image) == image_num-1:
            break
    browser.close()

    # browser.get("https://search.naver.com/search.naver?where=image&section=image&query=%EC%BD%94%EB%A1%9C%EB%82%98&res_fr=0&res_to=0&sm=tab_opt&color=&ccl=0&nso=so%3Ar%2Cp%3A1d%2Ca%3Aall&datetype=1&startdate=&enddate=&gif=0&optStr=d&nq=&dq=&rq=&tq=")
    # wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="main_pack"]/section[2]/div/div[1]/div[1]/div[1]/div/div[1]/a/img')))

    # images = browser.find_all('img',attrs={'class':'_image _listImage'})

    # for idx, image in enumerate(images):    
    #     image_url = image['src']
    #     print(image_url)   
    #     image_res = requests.get(image_url)
    #     image_res.raise_for_status()

    #     with open('{}.png'.format(idx+1), 'wb') as f:
    #         f.write(image_res.content)
    
    #     if idx >= 9:
    #         break

def covid_num_crawling():
    url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%ED%99%95%EC%A7%84%EC%9E%90'
    soup = create_soup(url)
    # code = req.urlopen('https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%ED%99%95%EC%A7%84%EC%9E%90')
    #html 방식으로 파싱
    # soup = BeautifulSoup(code, "html.parser")
    #정보 get
    # info_num = soup.select("div.status_info p")
    # result = info_num[0].get_text() #=> 확진자
    result = soup.find('p', attrs={'class':'info_num'}).get_text()
    return result

def covid_news_crawling():
    # code = req.urlopen("https://search.naver.com/search.naver?where=news&sm=tab_jum&query=%EC%BD%94%EB%A1%9C%EB%82%98")
    # soup = BeautifulSoup(code, "html.parser")
    url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query=%EC%BD%94%EB%A1%9C%EB%82%98'
    soup = create_soup(url)
    output_result =''
    news_list = soup.find_all('a',attrs={'class':'news_tit'}, limit=3)
    for news in news_list:
        title = news.get_text()
        news_url = news['href']
        output_result += title + "\n" + news_url + "\n\n"
    return output_result

    # news_list = soup.find('ul', attrs={'class':'list_news'}).find_all('li', limit= 3)
    # for news in news_list:
    #     title = news.div.div.div.a.get_text()
    #     news_url = news.div.div.div.a['href']
    #     print(title)
    #     print(news_url)

    # title_list = soup.select("a.news_tit")
    # output_result = ""
    # for i in title_list:
    #     title = i.text
    #     news_url = i.attrs["href"]
    #     output_result += title + "\n" + news_url + "\n\n"
    #     if title_list.index(i) == 2:
    #         break
    # return output_result
    
def movie_chart_crawling():
    session=requests.Session()
    #영화 크롤링 사이트
    addr='http://movie.naver.com/movie/running/current.nhn'
    req=session.get(addr)
    soup=BeautifulSoup(req.text,'html.parser')
    titles=soup.find_all('dl',class_='lst_dsc')
    cnt=1
    output=" "
 
    # # 영화제목+ 링크가 순서대로 5개 출력되고 각 영화별 설명이 짤막하게 들어가고 + 출력까지 
    # for title in titles:
    #     output+=str(cnt)+'위: '+title.find('a').text+'\n'+addr+title.find('a')['href']+'\n'
    #     #여기서 푸쉬해서 5개 각 저옵가 메세지로 출력되게끔
    #     bot.send_message(chat_id=id,text=output)
    #     output="" 
    #     cnt+=1
    #     if cnt==6:
    #         break
    #return output
    
def melon_chart_crawling():
    url = 'https://www.melon.com/chart/index.htm'
 
    browser.get(url)
    melon = browser.page_source
    soup = BeautifulSoup(melon, 'html.parser')
    # title = soup.select('#frm > div div.ellipsis.rank01 > span > a')
    title = soup.find_all('div',attrs={'class':'ellipsis.rank01'})
    # artist = soup.select('#frm > div div.ellipsis.rank02 > span')
    artist = soup.find_all('div',attrs={'class':'ellipsis.rank01'})
 
    titles = []
    for i,j in enumerate(title):
        if i < 10:
            tts = str(i) + ' ' + j.get_text()
            titles.append(tts)
 
    artists = []
    for i, j in enumerate(artist):
        if i < 10:
            tts = j.get_text()
            artists.append(tts)
 
    key_val = [titles, artists]
    # rank_text = dict(zip(*key_val))
    print(artist)
    #titles, artists 는 .text필드 없음, str로 파싱 후 title은 앞자리2번째부터
    output=" "
    #10개. 더 구하고싶으면 더 조절
    # for i in range (0,10):
        
    #     output+=str(i+1)+'위: '+str(titles[i][2:])+"-"+str(artists[i])+'\n'

    # print(output)     
    return output

def weather_crawling():
    url="https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EC%8B%9C%ED%9D%A5+%EB%82%A0%EC%94%A8&oquery=%EB%82%A0%EC%94%A8&tqi=hP%2FGYdprvN8ssFZzsmGssssssM0-366507"
    soup = create_soup(url)

    cast = soup.find('p', attrs={'class':'summary'}).get_text()

    curr_temp = soup.find('div',attrs={'class':'temperature_text'}).get_text().strip()
    min_temp = soup.find('span',attrs={'class':'lowest'}).get_text()
    max_temp = soup.find('span',attrs={'class':'highest'}).get_text()

    morning_rain_rate = soup.find('span',attrs={'class':'rainfall'}).get_text()
    evening_rain_rate = soup.find('span',attrs={'class':'rainfall'}).get_text()

    pm10 = soup.find('li',attrs={'class':'item_today level1'}).get_text().strip()
    pm25 = soup.find('li',attrs={'class':'item_today level3'}).get_text().strip()

    print(cast)
    print('{} ({}/ {})'.format(curr_temp,min_temp,max_temp))
    print('오전강수 확률 {} / 오후강수 확률 {}'.format(morning_rain_rate,evening_rain_rate))
    print('{}, {}'.format(pm10, pm25))
    print()

def sports_news_crawling():
    url = 'https://sports.news.naver.com'
    browser.get('https://sports.news.naver.com/wfootball/index')
    browser.find_element_by_xpath('//*[@id="_sports_lnb_menu"]/div/ul[1]/li[5]/ul/li[1]/a').click()
    browser.implicitly_wait(3)
    browser.find_element_by_xpath('//*[@id="_sortTypeList"]/li[2]').click()
    time.sleep(3)

    soup = BeautifulSoup(browser.page_source,'lxml')

    result = ''
    news_list = soup.find('div',attrs={'class':'news_list'}).find('ul').find_all('li',limit=5)
    for news in news_list:
        a_idx = 0
        img = news.find('img')
        if img:
            a_idx = 1

        title = news.find_all('a')[a_idx].get_text()
        link = url+news.find_all('a')[a_idx]['href']
        result += title + "\n" + link + "\n\n"
        # print(title)
        # print(link)
    return result

def sports_video_crawling():
    browser.get('https://sports.news.naver.com/wfootball/index')
    browser.find_element_by_xpath('//*[@id="_sports_lnb_menu"]/div/ul[1]/li[5]/ul/li[2]/a').click()
    browser.find_element_by_xpath('//*[@id="daily_ranking"]/li[1]/a').click()

    soup = BeautifulSoup(browser.page_source,'lxml')
    
    result =''
    title = soup.find('div',attrs={'class':'video_summary'}).find('h3').get_text()
    link = browser.current_url
    print(title)
    print(link)
    # result = title + link
    # video_list = soup.find('ul',attrs={'id':'daily_ranking'}).find_all('li',limit=3)
    # for news in video_list:
        # title = news.find_all('a').get_text()
        # link = url+news.find_all('a')[a_idx]['href']
        # result += title + "\n" + link + "\n\n"
        # print(title)
        # print(link)
    # return result


options = webdriver.ChromeOptions()
# 백그라운드로 실행
# options.add_argument('headless')
# options.headless = True
# options.add_argument('window-size=1920x1080')

browser = webdriver.Chrome(options=options)

if __name__ == '__main__':    
    # covid_image_crawling()
    # movie_chart_crawling()
    # covid_news_crawling()
    # melon_chart_crawling()
    # weather_crawling()
    # sports_news_crawling()
    sports_video_crawling()
