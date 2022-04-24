from selenium import webdriver
import tokenid

id = tokenid.user_id
pw = tokenid.user_pw

browser = webdriver.Chrome()
browser.get('https://www.naver.com/')

browser.find_element_by_class_name('link_login').click()

browser.find_element_by_id('id').send_keys('user_id')
browser.find_element_by_id('pw').send_keys('user_pw')

browser.find_element_by_id('log.login').click()