# https://ru.stackoverflow.com/questions/716614/Парсинг-внутренних-ссылок-сайта

from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
import lxml

# DOMAIN =  "python-scripts.com"
DOMAIN =  "avsw.ru"
HOST = 'https://' + DOMAIN
FORBIDDEN_PREFIXES = ['#', 'tel:', 'mailto:']
links = set()  # множество всех ссылок


def add_all_links_recursive(url, maxdepth=2):
    # print('{:>5}'.format(len(links)), url[len(HOST):])
    # извлекает все ссылки из указанного `url`
    # и рекурсивно обрабатывает их
    # глубина рекурсии не более `maxdepth`

    # список ссылок, от которых в конце мы рекурсивно запустимся
    links_to_handle_recursive = []

    # получаем html код страницы
    request = requests.get(url)
    # парсим его с помощью BeautifulSoup
    soup = BeautifulSoup(request.content, 'lxml')

    # рассматриваем все теги <a>
    for tag_a in soup.find_all('a'):
        # получаем ссылку, соответствующую тегу
        link = tag_a['href']

        # если ссылка не начинается с одного из запрещённых префиксов
        if all(not link.startswith(prefix) for prefix in FORBIDDEN_PREFIXES):

            # проверяем, является ли ссылка относительной
            # например, `/oplata` --- это относительная ссылка
            # `http://101-rosa.ru/oplata` --- это абсолютная ссылка
            if link.startswith('/') and not link.startswith('//'):

                # преобразуем относительную ссылку в абсолютную
                link = HOST + link

            # проверяем, что ссылка ведёт на нужный домен
            # и что мы ещё не обрабатывали такую ссылку
            if urlparse(link).netloc == DOMAIN and link not in links:
                links.add(link)
                links_to_handle_recursive.append(link)

    if maxdepth > 0:
        for link in links_to_handle_recursive:
            add_all_links_recursive(link, maxdepth=maxdepth - 1)

def main():
    add_all_links_recursive(HOST + '/')

    list_links = list(links)
    list_links.sort()
    for link in list_links:
        print(link)

if __name__ == '__main__':
    main()