from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from logs import Logger
# from datetime import datetime


class Parse_Link(object):
    """
    Главное действующее лицо в этой пьесе
        - создает список
        - парсит страницу
            * находит все бъекты <a></a>
            * забирает href
            * если в списке нет этой ссылки
              и эта ссылка не ведет в соцсети 
              и не текстовый якорь:
                    убирает параметры после ?
                    убирает домен
                    добавляет ее
        - и записывает все ссылки в файл
          чтобы генератор дерева My_Tree() мог их прочесть
    """
    def __init__(self, url):
        self.url = url
        self.list_links = []
        self.filename = 'parsed_links.txt'
        self.social = ['vk', 'facebook', 'linkedin', 'twitter', 'callto', 'skype', 'tel', '#']

    def make_links(self):
        log = Logger(onprint=False)

        log.write_log(f'start urlopen {self.url}')
        
        page = urlopen(self.url)
        hostname = urlparse(self.url).hostname

        log.write_log(f'start soup {self.url}')
        soup = BeautifulSoup(page, 'html.parser')

        # log.write_log(f' ')
        # поиск ссылок
        all_links = soup.find_all('a')

        for link in all_links:
            # забирает href
            l = link.get('href')

            if l:
                # убираю аргументы из ссылок
                if '?' in l:
                    l = l[:l.find('?')]

                if hostname in l:
                    # отделить домен
                    l = l.split(hostname)
                    l = l[-1]

                for s in self.social:
                    # удалить ссылки на соцсеточки
                    if s in l :
                        l = 'zero'

                # сохраняю в список
                if l not in self.list_links and l != 'zero' and len(l) > 1:
                    self.list_links.append(l)

        log.write_log(f'finish make_links in {self.url}')



    def write_to_file(self):
        # запись в файл
        with open(self.filename, 'w') as f:
            for link in self.list_links:
                f.write(f"{link}\n")
