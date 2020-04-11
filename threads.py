from threading import Thread
from parse_link import Parse_Link
from datetime import datetime


class My_Thread(Thread):
    """ Поток для генерации ссылок 
        Принимает
            - главную ссылку
                в случае если найдет укороченные ссылки
                /pages/page1
                прикрепит главную ссылку в начало
                domain.com/pages/page1
            - основной список
                для добавления новых найденных ссылок
            - ссылка из списка, которые нашел до этого Parse_Link()
         """
    def __init__(self, link, main_links, main_url):
        Thread.__init__(self)
        self.link = link
        self.main_links = main_links
        self.main_url = main_url

    def run(self):
        """
        run()
            - Создает логер
            - Генерирует ссылку 
        создает Parse_Link()
            - находит все ссылки
            - сохраняет их в список
            - итерация по списку
                если ссылки нет в главном списке:
                    добавляет
        Если ссылка дала ошибку:
            сохраняю ее в лог
        """
        log = Logger(onprint=False)
        try:
            log.write_log(f'{self.getName()} CREATED')
            url = f'{ self.main_url }{ self.link}'
            log.write_log(f'{self.getName()} BEGIN PARSE {url}')
            
            parser = Parse_Link(url)
            parser.make_links()
            
            links = parser.list_links

            for link in links:
                if link not in self.main_links:
                    self.main_links.append(link)
                    log.write_log(f'{self.getName()} ADD {link}')

        except Exception as e:
            log = Logger()
            log.write_log(f'{self.getName()} ERROR - {e} - { self.main_url }{ self.link}')


class Logger(object):
    """
    простой объект для ведения логов
    если onprint TRUE:
        в консоль ничего не выводит
    """
    def __init__(self, onprint = True):
        self.filename = 'parser.log'
        self.onprint = onprint

    def write_log(self, log):

        with open(self.filename, 'a+') as f:
            f.write(f'{datetime.now()} - {log}\n')
            
            if self.onprint:
                print(f'{log}\n')