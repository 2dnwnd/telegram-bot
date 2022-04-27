from time import sleep

sleep(1)	# 1초 대기
sleep(0.5)	# 0.5초 대기

# 암시적 대기 (Implicit Waits)
from selenium import webdriver

driver = webdriver.Chrome()
driver.implicitly_wait(10)	# 암시적 대기 시간 10초 설정 (페이지 로드되면 작동)
driver.get("https://naver.com")


# 암시적 대기는 동적페이지에 문제 생길수도 있음(페이지는 로드 되었지만 원하는 요소가 없을 수도있다.)
# 해결방법
# 1. 페이지를 직접 스크롤한다
# 2. 명시적 대기를 건다
# 명시적 대기(Explicit Waits)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://naver.com")
try:
	element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "log.login"))
            # log.login 요소가 뜰때 까지 10초동안 대기
	)
finally:
	driver.quit()


# 페이지 스크롤
interval = 2

# 현재 문서 높이를 가져와서 저장
pre_height = driver.execute_script('return document.body.scrollHeight')

while True:
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')

    sleep(interval)

    curr_height = driver.execute_script('return document.body.scrollHeight')
    if curr_height == pre_height: #직전 높이와같으면, 높이변화가 없으면
        break
    
    pre_height = curr_height

# 맨위로 올리기
driver.execute_script('window.scrollTo(0,0)')