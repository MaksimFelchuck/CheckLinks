import asyncio
import logging
from itertools import repeat
from typing import NamedTuple
from urllib.parse import urlparse

import aiohttp
from bs4 import BeautifulSoup

logging.basicConfig(format='%(asctime)s|%(levelname)s|%(message)s',
                    level=logging.DEBUG)
tag_list = ["a", "link", "script", "source", "img", "div"]
attr_list = ["href", "href", "src", "srcset", "src", "href"]


class Link(NamedTuple):
    url: str
    domen: str
    depth: int


class LinkChecker:
    def __init__(self, root_link: Link):
        self.root_link = root_link.url
        self.checked_links = []

    async def check_root_url(self):
        logging.debug(f"Првоеряю {self.root_link.url}")
        await self.check_links(self.root_link)
        return self.checked_links

    async def check_links(self, link: Link) -> list[str]:
        if not link.depth:
            return None

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(link.url) as response:
                    logging.debug(f"{link.url} - статуст ответа {response.status}")
                    response.raise_for_status()
                    html = await response.text()

                    soup = BeautifulSoup(html, "html.parser")
                    coroutine_list = list(
                        map(self.check_tag, repeat(soup), tag_list, attr_list,
                            repeat(link)))
                    await asyncio.gather(*coroutine_list)
            except Exception as err:
                logging.warning(f"Найдена сломаная ссылка {link.url}")
                return None

    async def check_tag(self, soup: BeautifulSoup, tag_name: str, attr: str,
                        link: Link) -> list[str]:

        for tag in soup.find_all(tag_name):
            if tag.has_attr(attr):
                fetched_link = tag[attr]
                # self.checked_links.append(
                #     fetched_link) if fetched_link not in self.checked_links else None


if __name__ == "__main__":
    url = input("Ввeдите url: ")
    depth = input("Введите глубину: ")
    parsed_root_url = urlparse(url)

    root_link = Link(url=url, domen=parsed_root_url.netloc, depth=depth)
    checker = LinkChecker(root_link)
    logging.debug(f"Начинаю проверку. Корневой url: {url}")
    checked_links = asyncio.run(checker.check_root_url())
    print(len(checked_links))
