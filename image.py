import requests
from bs4 import BeautifulSoup


url = 'https://search.naver.com/search.naver?where=image&section=image&query=%EC%BD%94%EB%A1%9C%EB%82%98&res_fr=0&res_to=0&sm=tab_opt&color=&ccl=0&nso=so%3Ar%2Cp%3A1d%2Ca%3Aall&datetype=1&startdate=&enddate=&gif=0&optStr=d&nq=&dq=&rq=&tq='
res = requests.get(url)
res.raise_for_status()
soup = BeautifulSoup(res.text, 'lxml')

images = soup.find_all('img',attrs={'class':'_image _listImage'})

# print(images['src'])

for idx, image in enumerate(images):    
    image_url = image['src']
    print(image_url)   
    image_res = requests.get(image_url)
    image_res.raise_for_status()

    with open('{}.png'.format(idx+1), 'wb') as f:
        f.write(image_res.content)
    
    if idx >= 9:
        break