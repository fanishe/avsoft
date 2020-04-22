# Асинхронный парсер для создания карты сайта
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
from logs import Logger

main_list = []
social = ['vk', 'facebook', 'linkedin', 'twitter', 'callto', 'skype', 'tel', '#', 'mailto']

log = Logger(onprint=True)

async def connection(session, url):
    """ делает запрос, ожидает ответа и сразу же поднимается в случае статуса не-200 """

    log.info(f'set  connection\nurl - {url}')

    resp = await session.request(method="GET", url=url)
    resp.raise_for_status()
    html = await resp.text()
    return html

async def soup_d(html):
    """ Создает объект  BeautifulSoup """
    soup = BeautifulSoup(html, 'html.parser')
    return soup

async def parse_response(html, hostname):
    """ Парсит страницу HTML которая возвращается от сервера
        чистит ссылки от мусора и добавляет их в локальный список
     """
    log.debug('begin parse')
    soup = await soup_d(html)
    local_list = []
    all_links = soup.find_all('a')

    for link in all_links:
        # забирает href
        l = link.get('href')
        log.onprint = False
        log.debug(f'link - {l}')

        if l:
            # убираю аргументы из ссылок
            if '?' in l:
                l = l[:l.find('?')]
                log.debug(f'delete arguments {l}')

            if hostname in l:
                # отделить домен
                l = l.split(hostname)
                l = l[-1]
                log.debug(f'delete domain {l}')

            for s in social:
                # удалить ссылки на соцсеточки
                if s in l :
                    l = 'zero'

            # сохраняю в список
            if l not in local_list and l != 'zero' and len(l) > 1:
                local_list.append(l)
                log.debug(f'append to local list - {l}')
    return local_list

async def parse_local_list(local_list):
    """ берет ссылки из локального списка, и добавляет их в основной список
    """
    for link in local_list:
        if link not in main_list:
            main_list.append(link)
            log.debug(f'append to main list - {link}')

async def make_links(url, session):
    """ 
        Основной цикл для организации взаимодействия всех корутин
        Проблема с которой столкнулся
            начинает парсить ссылки на документы
                /images/image/img.png
            пришлось обработать три варианта возникновения такой проблемы
            их наверняка больше, и это вызовет ошибку при дальнейшей работе
            пытался решить эту проблему так же как и в parse_response
                for s in social:
            но итерация проходила только в первом случае, потом прерывалась
            пришлось сделать хардкодом
    """
    log.debug(f'set session with {url}')
    # parsed_url = urlparse(url)
    root_domain = urlparse(url).netloc
    # domain = parsed_url.geturl()

    try:
        # обработка ссылок на документы и картинки
        if 'png' in url or 'pdf' in url or 'jpg' in url:
            html = None
        else:
            html = await connection(session, url)
    except Exception as error:
        log.onprint=True
        log.error(f'{error}')
        log.onprint=False
        html = None

    if html:
        # запись в локальный список
        local_list = await parse_response(html, root_domain)
        # запись из локального списка в главный
        await  parse_local_list(local_list)

async def main(url):
    """ объединение всех функций в одну, чтобы можно было легко импортировать """
    start = time.time()
    log.debug(f'started')

    async with aiohttp.ClientSession() as session:
        # установка соединения
        # делаю список ссылок из главной страницы в основной список
        await make_links(url, session)

        tasks = []
        for m in main_list:
            # из основного списка, прикрепляю домен к укороченным ссылкам
            # создаю и запускаю таски
            url2 = f'{url}{m}'
            tasks.append(
                asyncio.ensure_future(make_links(url2, session))
            )
            await asyncio.gather(*tasks)

    end = time.time()
    log.onprint=True
    log.info(f'work time - {end - start}')

if __name__ == "__main__":
    print('This module should be imported. It used in async_main.py')