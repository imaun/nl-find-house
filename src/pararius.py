import requests
from bs4 import BeautifulSoup
from database import Database
from models import House
from models import Source


class Pararius:
    def __init__(self, source: Source) -> object:
        self._sourceName: str = 'pararius'
        self._source_id: int = source.id
        self._city: str = source.city
        self._baseUrl: str = source.base_url
        self._page_url: str = source.page_url
        self._paging_format: str = source.paging_format
        self._start_page_index: int = source.start_page_index
        self._page_index: int = source.start_page_index  # Pararius start page number
        self._limit_page_index: int = source.limit_page_index

    def get_url(self):
        # Add / if baseUrl does not ends with it
        url: str = self._baseUrl.rstrip('/') + '/' + self._page_url.lstrip('/')
        if self._page_index == self._start_page_index:
            return url
        return url + self._paging_format.replace('%', str(self._page_index))

    def crawl(self):
        for pageNo in range(self._start_page_index, self._limit_page_index):

            url = self.get_url()
            page = requests.get(url)
            print(url)
            html = BeautifulSoup(page.content, 'html.parser')
            search_result = html.find('ul', {"class": "search-list"})
            items = search_result.find_all("li", {"class": "search-list__item"})
            print(f'Found {len(items)} on "{self._sourceName}"... ')

            with Database() as db:
                for item in items:
                    e_title = item.find('h2', {"class": "listing-search-item__title"})
                    if e_title is None: continue

                    title = e_title.text.strip()
                    title_href = e_title.find('a').get('href')
                    item_url = self._baseUrl + title_href

                    print('[{}] found a new house: {}'.format(self._sourceName, item_url))
                    if db.is_house_url_exists(item_url):
                        print('Skipping the house with url: {} because already exists!'.format(item_url))
                        continue

                    picture = item.find('img', {"class": "picture__image"}).get('src')
                    print('[{}] picture: {}'.format(self._sourceName, picture))

                    address = item.find('div', {"class": "listing-search-item__sub-title'"}).text.strip()
                    print('[{}] address: {}'.format(self._sourceName, address))

                    price_text = item.find("div", {"class": "listing-search-item__price"}).text.strip()
                    price = int(price_text[1:].split(' ')[0].replace(',', ''))
                    print('[{}] price: {}'.format(self._sourceName, price))

                    area_elm = item.find('li', {
                        "class": "illustrated-features__item illustrated-features__item--surface-area"})
                    area = area_elm.text.strip() if area_elm is not None else None
                    print(area)

                    rooms_elm = item.find('li', {
                        "class": "illustrated-features__item illustrated-features__item--number-of-rooms"})
                    rooms = rooms_elm.text.strip() if rooms_elm is not None else None
                    print(rooms)

                    interior_elm = item.find('li', {
                        "class": "illustrated-features__item illustrated-features__item--interior"})
                    interior = interior_elm.text.strip() if interior_elm is not None else None

                    h = House(0, self._sourceName, self._source_id, url, picture, title, self._city,
                              'apartment', price_text, price, 1, None, rooms, area, interior, None)

                    db.add_house(h)