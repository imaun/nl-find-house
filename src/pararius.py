import requests
from bs4 import BeautifulSoup


class Pararius:
    def __int__(self, url):
        self._source = 'pararius'
        self._baseUrl = 'https://www.pararius.com'
        self._url = url

    def get_houses(self):
        page = requests.get(self._url)
        html = BeautifulSoup(page.content, 'html.parser')
        search_result = html.find('ul', {"class": "search-list"})
        items = search_result.find_all("li", {"class": "search-list__item"})
        print(f'Found {len(items)} on "{self._source}"... ')
        for item in items:
            e_title = item.find('h2', {"class": "listing-search-item__title"})
            title = e_title.text.strip()
            print(title)
            title_href = e_title.find('a').get('href')
            print(self._baseUrl + title_href)
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
            exit(0)
