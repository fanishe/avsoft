from parse_link import Parse_Link
from trees import My_Tree
from threads import My_Thread, Logger
import time
import sys
import asyncio
import aiohttp
from bs4 import BeautifulSoup


var = sys.argv[1:]
# TODO:
    # Что делает код
    # линкер делает запросы
    # парсер парсит полученное и сохраняет ссылки
    # как это должно работать
        # линкер отправляет запросы на все ссылки из главного списка
        # линкер ждет пока парсер закончит
        # главный цикл
            # запускает линкер
            # если пришел ответ отдает его парсеру



# def main():
    # объект для записи логов и вывода в консоль
    # pass

log = Logger()
log.write_log(f'START NEW SESSION')

# принимает ссылку через терминал
# если ничего нет берет основной урл
if not var:
    link = "https://avsw.ru"
else:
    link = var[0]
# https://aiohttp.readthedocs.io/en/stable/client_quickstart.html

async def get_html(link):
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as resp:
            log.write_log(f'response - {resp.status}')
            # print(await resp.text())

async def parse_html(link):
    response = await get_html(link)
    social = ['vk', 'facebook', 'linkedin', 'twitter', 'callto', 'skype', 'tel', '#']
    list_links = []
    soup = BeautifulSoup(response, 'html.parser')
    all_links = soup.find_all('a')

    for link in all_links:
        # забирает href
        l = link.get('href')

        if l:
            # убираю аргументы из ссылок
            if '?' in l:
                l = l[:l.find('?')]

            # if hostname in l:
            #     # отделить домен
            #     l = l.split(hostname)
            #     l = l[-1]

            for s in  social:
                # удалить ссылки на соцсеточки
                if s in l :
                    l = 'zero'

            # сохраняю в список
            if l not in  list_links and l != 'zero' and len(l) > 1:
                 list_links.append(l)
                 print(l)
    return list_links





if __name__ == "__main__":
    asyncio.run(parse_html(link))

    