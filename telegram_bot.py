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
import tokenid 


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

# 코로나 확진자수
def covid_num_crawling():
    url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%ED%99%95%EC%A7%84%EC%9E%90'
    soup = create_soup(url)
    
    result = soup.find('p', attrs={'class':'info_num'}).get_text()
    return result

# 코로나 뉴스 확인
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

# 코로나 이미지
def covid_image_crawling(image_num=5):
    if not os.path.exists("./코로나이미지"):
        os.mkdir("./코로나이미지")
 
    browser.implicitly_wait(3)
    # wait = WebDriverWait(browser, 10)
    browser.get("https://search.naver.com/search.naver?where=image&section=image&query=%EC%BD%94%EB%A1%9C%EB%82%98&res_fr=0&res_to=0&sm=tab_opt&color=&ccl=0&nso=so%3Ar%2Cp%3A1d%2Ca%3Aall&datetype=1&startdate=&enddate=&gif=0&optStr=d&nq=&dq=&rq=&tq=")
 
    # wait.until(EC.presence_of_element_located(By.XPATH, '//img[@class="_image _listImage"]'))
    images = browser.find_elements(By.XPATH, '//img[@class="_image _listImage"]')

    for image in images:
        img_url = image.get_attribute("src")
        req.urlretrieve(img_url, "./코로나이미지/{}.png".format(images.index(image)))
        if images.index(image) == image_num-1:
            break
    browser.close()

# 최신 영화 순위
def movie_chart_crawling():
    session=requests.Session()
    #영화 크롤링 사이트
    addr='https://movie.naver.com/movie/running/current.nhn'
    req=session.get(addr)
    soup=BeautifulSoup(req.text,'html.parser')
    titles=soup.find_all('dl',class_='lst_dsc')
    cnt=1
    output=" "
 
    # 영화제목 + 영화링크 + 영화설명
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

# 멜론차트 10위
def melon_chart_crawling():
    url = 'https://www.melon.com/chart/index.htm'
    soup = create_soup(url)
    title = soup.select('#frm > div div.ellipsis.rank01 > span > a')
    artist = soup.select('#frm > div div.ellipsis.rank02 > span')
 
    titles = []
    for index,song in enumerate(title):
        if index < 10:
            tts = str(index) + ' ' + song.get_text()
            titles.append(tts)
 
    artists = []
    for index, song in enumerate(artist):
        if index < 10:
            tts = song.get_text()
            artists.append(tts)
    
    # titles, artists 는 .text필드 없음, str로 파싱 후 title은 앞자리2번째부터
    output=" "
    # 10위까지 
    for i in range (0,10):
        # 0,1 없애기
        output+=str(i+1)+'위: '+str(titles[i][2:])+"-"+str(artists[i])+'\n'
            
    return output
    
# 날씨 정보
def weather_crawling():
    url="https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EC%8B%9C%ED%9D%A5+%EB%82%A0%EC%94%A8&oquery=%EB%82%A0%EC%94%A8&tqi=hP%2FGYdprvN8ssFZzsmGssssssM0-366507"
    soup = create_soup(url)
    
    cast = soup.find('p', attrs={'class':'summary'}).get_text()

    curr_temp = soup.find('div',attrs={'class':'temperature_text'}).get_text().strip()
    min_temp = soup.find('span',attrs={'class':'lowest'}).get_text()
    max_temp = soup.find('span',attrs={'class':'highest'}).get_text()

    morning_rain_rate = soup.find('span',attrs={'class':'rainfall'}).get_text()
    evening_rain_rate = soup.find('span',attrs={'class':'rainfall'}).get_text()

    # wind = soup.find('di',attrs={'class':'summary_list'}).get_text()

    pm10 = soup.find('li',attrs={'class':'item_today level2'}).get_text().strip()
    pm25 = soup.find('li',attrs={'class':'item_today level2'}).get_text().strip()
    uv = soup.find('li',attrs={'class':'item_today level1'}).get_text().strip()

     
    result = (cast+'\n'+'{} ({}/ {})'.format(curr_temp,min_temp,max_temp)
    +'\n'+'오전강수 확률 {} / 오후강수 확률 {}'.format(morning_rain_rate,evening_rain_rate)
    # +'\n'+'{}'.format(wind[4]+wind[5])
    +'\n'+'{}, {}, {}'.format(pm10, pm25, uv))
    
    return result

# 최신 인기 축구뉴스
def sports_news_crawling():
    url = 'https://sports.news.naver.com'
    browser.get('https://sports.news.naver.com/wfootball/index')
    browser.find_element_by_xpath('//*[@id="_sports_lnb_menu"]/div/ul[1]/li[5]/ul/li[1]/a').click()
    browser.implicitly_wait(3)
    browser.find_element_by_xpath('//*[@id="_sortTypeList"]/li[2]').click()
    time.sleep(3)

    soup = BeautifulSoup(browser.page_source,'lxml')

    result = ''
    news_list = soup.find('div',attrs={'class':'news_list'}).find('ul').find_all('li',limit=3)
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

# 인기 축구영상
def sports_video_crawling():
    browser.get('https://sports.news.naver.com/wfootball/index')
    browser.find_element_by_xpath('//*[@id="_sports_lnb_menu"]/div/ul[1]/li[5]/ul/li[2]/a').click()
    browser.find_element_by_xpath('//*[@id="daily_ranking"]/li[1]/a').click()

    soup = BeautifulSoup(browser.page_source,'lxml')
    
    result =''
    title = soup.find('div',attrs={'class':'video_summary'}).find('h3').get_text()
    # 현재 페이지링크를 저장
    link = browser.current_url
    # print(title)
    # print(url)
    result = title + '\n' + link
    # video_list = soup.find('ul',attrs={'id':'daily_ranking'}).find_all('li',limit=3)
    # for news in video_list:
        # title = news.find_all('a').get_text()
        # link = url+news.find_all('a')[a_idx]['href']
        # result += title + "\n" + link + "\n\n"
        # print(title)
        # print(link)
    return result



id = tokenid.id
token = tokenid.token


bot = telegram.Bot(token)
info_message = '''- 오늘 확진자 수 확인 : "코로나" 입력
- 코로나 관련 뉴스 : "뉴스" 입력
- 코로나 관련 이미지 : "이미지" 입력
- 최신 영화 순위 : "영화" 입력 
- 최신 노래 순위 : "노래" 입력
- 현재 날씨 : "날씨" 입력 
- 최신 인기 축구뉴스 :  "축구" 입력
- 인기 축구영상 : "축구영상" 입력  '''
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
        # bot.sendMessage(chat_id=id, text=info_message)
    # 코로나 관련 뉴스 답장
    elif (user_text == "뉴스"):
        covid_news = covid_news_crawling()
        bot.send_message(chat_id=id, text=covid_news)
        # bot.sendMessage(chat_id=id, text=info_message)
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
        # bot.sendMessage(chat_id=id, text=info_message)
    # 최신인기 영화 순위 정보 답장
    elif(user_text=="영화"):
        bot.send_message(chat_id=id, text="조회 중 입니다...")
        movie_chart=movie_chart_crawling()
        #출력은 위의 함수 내부에서 한다. (1개씩 보내는걸 5번한거)
        #bot.send_message(chat_id=id,text=movie_chart)
        # bot.sendMessage(chat_id=id,text=info_message)
    # 멜론차트 정보 답장
    elif( user_text=="노래"):
        bot.send_message(chat_id=id, text="조회 중 입니다...")
        melon_chart=melon_chart_crawling()
        bot.send_message(chat_id=id, text=melon_chart)
        bot.sendMessage(chat_id=id, text=info_message)
    # 현재 날씨 답장    
    elif(user_text=="날씨"):
        bot.send_message(chat_id=id, text="조회 중 입니다...")
        #n: neighbor
        n_weather=weather_crawling()
        bot.send_message(chat_id=id,text=n_weather)
        # bot.sendMessage(chat_id=id,text=info_message)    
    # 축구 관련 뉴스 답장
    elif(user_text=="축구"):
        bot.send_message(chat_id=id, text="조회 중 입니다...")
        sports_news = sports_news_crawling()
        bot.send_message(chat_id=id,text=sports_news) 
        # bot.sendMessage(chat_id=id,text=info_message)
    # 축구 관련 영상 답장
    elif(user_text=='축구영상'):
        bot.send_message(chat_id=id, text="조회 중 입니다...")
        sport_video = sports_video_crawling()
        bot.send_message(chat_id=id,text=sport_video)
        # bot.sendMessage(chat_id=id,text=info_message)


echo_handler = MessageHandler(Filters.text, handler)
dispatcher.add_handler(echo_handler)