# Клиентское API
import aiohttp
import asyncio

def f(loop):
    response = yield from aiohttp.request(
        'GET', 'http://python.org',
        loop = loop
    )
    body = yield from response.read()
    return body

loop = asyncio.get_event_loop()
loop.run_until_complete(f(loop))

