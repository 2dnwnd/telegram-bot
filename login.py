from selenium import webdriver

user_id = 'dnwnd1019'
user_pw = 'aa1216137'

browser = webdriver.Chrome()
browser.get('https://www.naver.com/')

browser.find_element_by_class_name('link_login').click()

browser.find_element_by_id('id').send_keys('user_id')
browser.find_element_by_id('pw').send_keys('user_pw')

browser.find_element_by_id('log.login').click()