import requests
from bs4 import BeautifulSoup
from database import Database
from models import House
from models import Source


class Pararius:
    def __init__(self, source: Source) -> object:
        self._sourceName: str = 'pararius'
        self._source_id: int = source.id
        self._baseUrl: str = source.base_url
        self._page_url: str = source.page_url
        self._paging_format: str = source.paging_format
        self._start_page_index: int = source.start_page_index
        self._page_index: int = source.start_page_index  # Pararius start page number
        self._db = Database()

    def get_url(self):
        # Add / if baseUrl does not ends with it
        url: str = self._baseUrl.rstrip('/') + '/' + self._page_url
        if self._page_index == self._start_page_index:
            return url
        return url + self._paging_format.replace('%', str(self._page_index))

    def crawl(self):
        url = self.get_url()
        page = requests.get(url)
        html = BeautifulSoup(page.content, 'html.parser')
        search_result = html.find('ul', {"class": "search-list"})
        items = search_result.find_all("li", {"class": "search-list__item"})
        print(f'Found {len(items)} on "{self._sourceName}"... ')
        for item in items:
            h = House()
            e_title = item.find('h2', {"class": "listing-search-item__title"})
            h.title = e_title.text.strip()
            title_href = e_title.find('a').get('href')
            item_url = self._baseUrl + title_href

            print('[{}] found a new house: {}'.format(self._sourceName, item_url))
            if self._db.is_house_url_exists(item_url):
                print('Skipping the house with url: {} because already exists!'.format(item_url))
                continue

            picture = item.find('img', {"class": "picture__image"}).get('src')
            print('[{}] picture: {}'.format(self._sourceName, picture))

            address = item.find('div', {"class": "listing-search-item__sub-title'"}).text.strip()
            print('[{}] address: {}'.format(self._sourceName, address))

            price_text = item.find("div", {"class": "listing-search-item__price"}).text.strip()
            price = int(price_text[1:].split(' ')[0].replace(',', ''))
            print('[{}] price: {}'.format(self._sourceName, price))

            area = item.find('li', {
                "class": "illustrated-features__item illustrated-features__item--surface-area"}).text.strip()
            print(area)
            rooms = item.find('li', {
                "class": "illustrated-features__item illustrated-features__item--number-of-rooms"}).text.strip()
            print(rooms)
            interior = item.find('li', {
                "class": "illustrated-features__item illustrated-features__item--interior"}).text.strip()
            print(interior)

    def add(self, url, title, image_url, city, house_type,
            price_text, price, rooms, area, interior, desc):
        h = House()
        h.title = title
        h.source_name = self._sourceName
        h.source_id = self._source_id
        h.url = url
        h.image_url = image_url
        h.city = city
        h.house_type = house_type
        h.price_text = price_text
        h.price = price
        h.rooms = rooms
        h.area = area
        h.interior = interior
        h.description = desc
        self._db.add_house(h)
