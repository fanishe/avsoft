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

hostname = urlparse(mypage).hostname

list_links = []
social = ['vk', 'facebook', 'linkedin', 'twitter', 'callto', 'skype', 'tel']
for link in all_links:
    l = link.get('href')

    if l:

        if hostname in l:
            l = l.split(hostname)
            l = l[-1]
        
        for s in social:
            if s in l:
                l = 'zero'

        if l not in list_links and l != 'zero' and len(l) > 1:
            list_links.append(l)



list_links.sort()
with open('domains.txt', 'w') as f:
    for link in list_links:
        f.write(f"{link}\n")