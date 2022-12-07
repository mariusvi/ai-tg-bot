from abc import ABC, abstractmethod
from typing import List, Optional

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from scraper.models.item import Item, ItemLink, GroupLink


class BaseScraper(ABC):
    __items_per_page__: int = 0
    __domain__: str = ""

    @abstractmethod
    def _retrieve_items_list(self, pages_count: int, keyword: str) -> List[ItemLink]:
        pass

    async def _get_page_content(self, query: str) -> Optional[BeautifulSoup]:
        print(f"{self.__domain__}/{query}")
        resp = requests.get(f"{self.__domain__}/{query}")
        if resp.status_code == 200:
            return BeautifulSoup(resp.content, features="html.parser")
        raise Exception("Cannot reach content!")


    async def scrape(self, keyword: str) -> List[Item]:
        categories_links: List[Optional[GroupLink]] = await self._retrieve_categories_list()
        
        scraped_items_links: List[Optional[ItemLink]] = []
        for categorie in categories_links[6:7]:
            items_links: List[Optional[ItemLink]] = await self._retrieve_items_list(categorie.url)
            scraped_items_links.append(items_links)

        scrapped_items_data: List[Item] = []
        for item_link_group in tqdm(scraped_items_links):
            for item_link in item_link_group:
                data = await self._retrieve_item_data(item_link.url)
                scrapped_items_data.append(data)
        
        print(scrapped_items_data[:5])

        return scrapped_items_data
