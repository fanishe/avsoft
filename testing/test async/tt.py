"""Асинхронное получение ссылок, встроенных в HTML нескольких страниц."""
import asyncio
import logging
import re
import sys
from typing import IO
import urllib.error
import urllib.parse
import aiofiles
import aiohttp
from aiohttp import ClientSession

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
"""
Константа HREF_RE является регулярным выражением для извлечения того, 
что мы в конечном итоге ищем, тегов href в HTML:
"""
logger = logging.getLogger("areq")
logging.getLogger("chardet.charsetprober").disabled = True

HREF_RE = re.compile(r'href="(.*?)"')
"""
Сопрограмма fetch_html() является оберткой вокруг GET-запроса, 
чтобы выполнить запрос и декодировать полученную страницу HTML. 
Он делает запрос, ожидает ответа и сразу же поднимается в случае статуса не-200:
"""
async def fetch_html(url: str, session: ClientSession, **kwargs) -> str:
    """GET запрос оболочки для загрузки страницы HTML.
    kwargs передаются в session.request().
    """

    resp = await session.request(method="GET", url=url, **kwargs)
    resp.raise_for_status()

    logger.info("Got response [%s] for URL: %s", resp.status, url)

    html = await resp.text()
    return html

""" 
Если статус нормальный, то fetch_html() возвращает HTML страницы ("str"). 
Примечательно, что в этой функции не выполняется обработка исключений. 
Логика заключается в том, чтобы передать это исключение вызывающей стороне 
и разрешить его обработку там:
"""

async def parse(url: str, session: ClientSession, **kwargs) -> set:
    """Найти HREFs в HTML `url`."""
    found = set()
    try:
        html = await fetch_html(url=url, session=session, **kwargs)
    except (
        aiohttp.ClientError,
        aiohttp.http_exceptions.HttpProcessingError,
    ) as e:
        logger.error(
            "aiohttp exception for %s [%s]: %s",
            url,
            getattr(e, "status", None),
            getattr(e, "message", None),
        )
        return found

    except Exception as e:
        logger.exception(
            "Non-aiohttp exception occured:  %s", getattr(e, "__dict__", {})
        )
        return found

    else:
        for link in HREF_RE.findall(html):
            try:
                abslink = urllib.parse.urljoin(url, link)
            except (urllib.error.URLError, ValueError):
                logger.exception("Error parsing URL: %s", link)
                pass
            else:
                found.add(abslink)

        logger.info("Found %d links for %s", len(found), url)
        return found

""" 
Мы "ждем" session.request() и resp.text(), потому что они являются ожидаемыми сопрограммами.
В противном случае цикл запроса / ответа был бы длиннохвостой частью приложения, 
но с асинхронным вводом-выводом, fetch_html() позволяет циклу событий работать с другими легкодоступными заданиями, 
такими как парсинг и запись URL, которые уже был доставлен
"""
async def write_one(file: IO, url: str, **kwargs) -> None:
    """Записать найденные HREF из `url` в` file`."""
    res = await parse(url=url, **kwargs)
    if not res:
        return None
    async with aiofiles.open(file, "a") as f:
        for p in res:
            await f.write(f"{url}\t{p}\n")
        logger.info("Wrote results for source URL: %s", url)


""" Далее в цепочке сопрограмм идет parse(), который ожидает fetch_html() 
для заданного URL, а затем извлекает все теги href из HTML этой страницы, проверяя, 
что каждый из них корректен, и форматируя его как абсолютный путь.

Следует признать, что вторая часть parse() является блокирующей, 
но она состоит из быстрого соответствия регулярному выражению и обеспечения того, 
что обнаруженные ссылки превращаются в абсолютные пути.

В этом конкретном случае этот синхронный код должен быть быстрым и незаметным. 
Но просто помните, что любая строка в данной сопрограмме будет блокировать другие сопрограммы, 
если только эта строка не использует yield,await или return. Если анализ был более интенсивным процессом, 
вы можете рассмотреть возможность запуска этой части в своем собственном процессе с помощью loop.run_in_executor().

Затем сопрограмма write() принимает файловый объект и один URL-адрес и ожидает от parse() 
возврата set проанализированных URL-адресов, записывая каждый файл в файл асинхронно вместе с его исходным 
URL-адресом посредством использования. aiofiles, пакет для асинхронного ввода-вывода файла.

Наконец, bulk_crawl_and_write() служит основной точкой входа в цепочку сопрограмм скрипта. 
Он использует один сеанс, и задача создается для каждого URL, который в конечном итоге читается из urls.txt. """

async def bulk_crawl_and_write(file: IO, urls: set, **kwargs) -> None:
    """Сканирование и запись одновременно в `file` для нескольких`urls`."""
    async with ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(
                write_one(file=file, url=url, session=session, **kwargs)
            )
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    import pathlib
    import sys

    assert sys.version_info >= (3, 7), "Script requires Python 3.7+."
    here = pathlib.Path(__file__).parent

    with open(here.joinpath("urls.txt")) as infile:
        urls = set(map(str.strip, infile))

    outpath = here.joinpath("foundurls.txt")
    with open(outpath, "w") as outfile:
        outfile.write("source_url\tparsed_url\n")

    asyncio.run(bulk_crawl_and_write(file=outpath, urls=urls))

