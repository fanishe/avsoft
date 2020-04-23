from threading import Thread
from parse_link import Parse_Link
from datetime import datetime
from logs import Logger
from queue import Queue

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
            log.debug(f'{self.getName()} CREATED')
            url = f'{ self.main_url }{ self.link}'
            log.info(f'{self.getName()} BEGIN PARSE {url}')
            
            parser = Parse_Link(url)
            parser.make_links()
            
            links = parser.list_links

            for link in links:
                if link not in self.main_links:
                    self.main_links.append(link)
                    log.info(f'{self.getName()} ADD {link}')

        except Exception as e:
            log = Logger()
            log.error(f'{self.getName()} {e} - { self.main_url }{ self.link}')


class Worker(Thread):
    """ Запускает поток из предоставленной очереди заданий """
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        log = Logger(onprint=True)
        while True:
            log.info(f'{self.getName()} - STARTED')
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception as e:
                log.error(f'{self.getName()} - {e}')
            finally:
                # задание выполнено 
                self.tasks.task_done()
                log.info(f'{self.getName()} - DONE')


class ThreadPool:
    """ Пул потоков получаючщий задания из очереди """
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads):
            Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        """ Добавить задание в очередь """
        self.tasks.put((func, args, kargs))

    def map(self, func, args_list):
        """ Добавить список заданий в очередь """
        for args in args_list:
            self.add_task(func, args)

    def wait_completion(self):
        """ Дождаться выполнения всех заданий и завершить потоки в очереди """
        self.tasks.join()
