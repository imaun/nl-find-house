import requests
from bs4 import BeautifulSoup
from database import Database
from models import House


class Pararius:
    def __int__(self, url):
        self._sourceName = 'pararius'
        self._baseUrl = 'https://www.pararius.com'
        self._url = url
        self._db = Database()
        self._source = self._db.get_source_by_name(self._sourceName)

    def get_houses(self):
        page = requests.get(self._url)
        html = BeautifulSoup(page.content, 'html.parser')
        search_result = html.find('ul', {"class": "search-list"})
        items = search_result.find_all("li", {"class": "search-list__item"})
        print(f'Found {len(items)} on "{self._sourceName}"... ')
        for item in items:
            h = House()
            e_title = item.find('h2', {"class": "listing-search-item__title"})
            title = e_title.text.strip()
            print(title)
            title_href = e_title.find('a').get('href')
            item_url = self._baseUrl + title_href
            if self._db.is_house_url_exists(item_url):
                continue
            print(item_url)
            picture = item.find('img', {"class": "picture__image"}).get('src')
            print(picture)
            address = item.find('div', {"class": "listing-search-item__sub-title'"}).text.strip()
            print(address)
            price_text = item.find("div", {"class": "listing-search-item__price"}).text.strip()
            price = int(price_text[1:].split(' ')[0].replace(',', ''))
            print(price)
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
        h.source_id = self._source.id
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
        self._db.insert_house(h)
        print(f'The House "{h.title}" successfully added to the database.')
