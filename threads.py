from threading import Thread
from parse_link import Parse_Link
from datetime import datetime


class My_Thread(Thread):
    def __init__(self, link, main_links, main_url):
        Thread.__init__(self)
        self.link = link
        self.main_links = main_links
        self.main_url = main_url

    def run(self):
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
            log.write_log(f'ERROR - {e} - {self.getName()} - { self.main_url }{ self.link}')


class Logger(object):
    def __init__(self, onprint = True):
        self.filename = 'parser.log'
        self.onprint = onprint

    def write_log(self, log):
        with open(self.filename, 'a+') as f:
            f.write(f'{datetime.now()} - {log}\n')
            if self.onprint:
                print(f'{log}\n')