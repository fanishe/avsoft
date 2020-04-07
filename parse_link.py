from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Источник
# https://coderoad.ru/46446457/Создание-sitemap-с-помощью-python

# Тестовая карта сайта
# https://pythonworld.ru/karta-sajta

# mypage = "https://pythonworld.ru/"
mypage = "https://avsw.ru"
# mypage = "http://fanishe.pythonanywhere.com/index"
page = urlopen(mypage)

soup = BeautifulSoup(page,'html.parser')

all_links = soup.find_all('a')

for link in all_links:
    print(link.get('href'))

parsed = urlparse(mypage)
hostname = parsed.hostname
print('hostname is ', hostname)
