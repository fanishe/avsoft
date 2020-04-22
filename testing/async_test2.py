import asyncio
import os
import async_timeout
import aiohttp

async def corutine_download(session,url):
    with async_timeout.timeout(10):
        print(1)
        async with session.get(url) as response:
            file_name=os.path.basename(url)

            with open(file_name,'wb') as file:
                while True:
                    chunk=await response.content.read(1024)
                    if not chunk:
                        break
                    file.write(chunk)
                print(file_name)
            return await response.release()

async def main(loop):
    urls=["http://www.irs.gov/pub/irs-pdf/f1040.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040a.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040ez.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040es.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040sb.pdf"]

    async with aiohttp.ClientSession(loop=loop) as session:
        
        tasks=[corutine_download(session,url) for url in urls]
        await asyncio.gather(*tasks)

if __name__=='__main__':
    loop=asyncio.get_event_loop()
    loop.run_until_complete(main(loop))