import aiohttp
import asyncio

import requests
from bs4 import BeautifulSoup


def getUrls():
    srcs = []
    with open('index.html', encoding='utf-8') as file:
        dom = BeautifulSoup(file.read(), 'html.parser')
        objects = dom.findAll('div', class_='Yl- MIw Hb7')
        for obj in objects:
            img = obj.findAll('img', class_='hCL kVc L4E MIw')[0]
            srcset = img['srcset']
            src = srcset.split(', ')[-1].split(' ')[0]
            srcs.append(src)
    return srcs


async def getImage(session: aiohttp.ClientSession, url, path):
    fileName = url.split('/')[-1]
    async with session.get(url) as response:
        with open(f'{path}/{fileName}', 'wb') as file:
            file.write(await response.read())


async def getImages(session, urls):
    tasks = [asyncio.create_task(getImage(session, url, 'img')) for url in urls]
    await asyncio.wait(tasks)


async def main():
    urls = getUrls()
    async with aiohttp.ClientSession() as session:
        await getImages(session, urls)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
