from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class Parse_Link(object):
    def __init__(self, url):
        self.url = url
        self.list_links = []
        self.filename = 'parsed_links.txt'
        self.social = ['vk', 'facebook', 'linkedin', 'twitter', 'callto', 'skype', 'tel']

    def make_links(self):
        page = urlopen(self.url)
        hostname = urlparse(self.url).hostname
        soup = BeautifulSoup(page, 'html.parser')
        all_links = soup.find_all('a')

        for link in all_links:
            l = link.get('href')

            if l:
                if hostname in l:
                    l = l.split(hostname)
                    l = l[-1]

                for s in self.social:
                    if s in l:
                        l = 'zero'

                if l not in self.list_links and l != 'zero' and len(l) > 1:
                    self.list_links.append(l)
        self.list_links.sort()

    def write_to_file(self):
        with open(self.filename, 'w') as f:
            for link in self.list_links:
                f.write(f"{link}\n")