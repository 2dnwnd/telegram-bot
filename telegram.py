import telegram
import requests
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request as req
import os
import time
# 셀레니움 로딩 대기
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
# 백그라운드로 실행
# options.add_argument('headless')
options.headless = True
options.add_argument('window-size=1920x1080')

browser = webdriver.Chrome(options=options)

def create_soup(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
    res = requests.get(url,headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text,'lxml')
    return soup

def covid_num_crawling():
    url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%ED%99%95%EC%A7%84%EC%9E%90'
    soup = create_soup(url)
    
    result = soup.find('p', attrs={'class':'info_num'}).get_text()
    return result

def covid_news_crawling():

    url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query=%EC%BD%94%EB%A1%9C%EB%82%98'
    soup = create_soup(url)
    output_result =''
    news_list = soup.find_all('a',attrs={'class':'news_tit'}, limit=3)
    for news in news_list:
        title = news.get_text()
        news_url = news['href']
        output_result += title + "\n" + news_url + "\n\n"
    return output_result

def covid_image_crawling(image_num=5):
    if not os.path.exists("./코로나이미지"):
        os.mkdir("./코로나이미지")
 
    browser.implicitly_wait(3)
    wait = WebDriverWait(browser, 10)
    browser.get("https://search.naver.com/search.naver?where=image&section=image&query=%EC%BD%94%EB%A1%9C%EB%82%98&res_fr=0&res_to=0&sm=tab_opt&color=&ccl=0&nso=so%3Ar%2Cp%3A1d%2Ca%3Aall&datetype=1&startdate=&enddate=&gif=0&optStr=d&nq=&dq=&rq=&tq=")
 
    wait.until(EC.presence_of_all_elements_located(By.XPATH, '//img[@class="_image _listImage"]'))
    images = browser.find_elements(By.XPATH, '//img[@class="_image _listImage"]')

    for image in images:
        img_url = image.get_attribute("src")
        req.urlretrieve(img_url, "./코로나이미지/{}.png".format(images.index(image)))
        if images.index(image) == image_num-1:
            break
    browser.close()

def movie_chart_crawling():
    session=requests.Session()
    #영화 크롤링 사이트
    addr='https://movie.naver.com/movie/running/current.nhn'
    req=session.get(addr)
    soup=BeautifulSoup(req.text,'html.parser')
    titles=soup.find_all('dl',class_='lst_dsc')
    cnt=1
    output=" "
 
    # 영화제목+ 링크가 순서대로 5개 출력되고 각 영화별 설명이 짤막하게 들어가고 + 출력까지 
    for title in titles:
        output+=str(cnt)+'위: '+title.find('a').text+'\n'+addr+title.find('a')['href']+'\n'
        print(output)
        #여기서 푸쉬해서 5개 각 저옵가 메세지로 출력되게끔
        bot.send_message(chat_id=id,text=output)
        output="" 
        cnt+=1
        if cnt==6:
            break
    #return output 




token = '5221097095:AAGJaWVAU0i0eWf7FHI7ioGRzgB9pHlVdqs'
id = '5160184450'

bot = telegram.Bot(token)
info_message = '''- 오늘 확진자 수 확인 : "코로나" 입력
- 코로나 관련 뉴스 : "뉴스" 입력
- 코로나 관련 이미지 : "이미지" 입력
- 최신 영화 순위 : "영화" 입력  '''
bot.sendMessage(chat_id=id, text=info_message)

# updater
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
# 봇
updater.start_polling()

# 챗봇 답장
def handler(update, context):
    user_text = update.message.text # 사용자가 보낸 메세지를 변수에 저장
    # 오늘 확진자 수 답장
    if (user_text == '코로나'):
        covid_num = covid_num_crawling()
        bot.send_message(chat_id=id, text='오늘 확진자 수: {}명'.format(covid_num))
        bot.sendMessage(chat_id=id, text=info_message)
    # 코로나 관련 뉴스 답장
    elif (user_text == "뉴스"):
        covid_news = covid_news_crawling()
        bot.send_message(chat_id=id, text=covid_news)
        bot.sendMessage(chat_id=id, text=info_message)
    # 코로나 관련 이미지 답장
    elif (user_text == "이미지"):
        bot.send_message(chat_id=id, text="최신 이미지 크롤링 중...")
        covid_image_crawling(image_num=10)
        # 이미지 한장만 보내기
        # bot.send_photo(chat_id=id, photo=open("./코로나이미지/0.png", 'rb'))
        # 이미지 여러장 묶어서 보내기
        photo_list = []
        for i in range(len(os.walk("./코로나이미지").__next__()[2])): 
            photo_list.append(telegram.InputMediaPhoto(open("./코로나이미지/{}.png".format(i), "rb")))
        bot.sendMediaGroup(chat_id=id, media=photo_list)
        bot.sendMessage(chat_id=id, text=info_message)

    elif(user_text=="영화"):
        bot.send_message(chat_id=id, text="조회 중 입니다...")
        movie_chart=movie_chart_crawling()
        #출력은 위의 함수 내부에서 한다.
        #bot.send_message(chat_id=id,text=movie_chart)
        bot.sendMessage(chat_id=id,text=info_message)

    

echo_handler = MessageHandler(Filters.text, handler)
dispatcher.add_handler(echo_handler)