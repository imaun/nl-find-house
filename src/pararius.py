import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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
        # Set up the web browser
        browser_options = Options()
        # browser_options.add_argument('--headless')
        # browser_options.add_argument('--start-maximized')
        browser_options.add_argument('--disable-extensions')
        browser_options.add_argument("--enable-javascript")
        # browser_options.add_argument('--no-sandbox')  # for linux only
        self._browser = webdriver.Chrome(options=browser_options)

    def get_url(self):
        # Add / if baseUrl does not ends with it
        url: str = self._baseUrl.rstrip('/') + '/' + self._page_url.lstrip('/')
        if self._page_index == self._start_page_index:
            return url
        return url + self._paging_format.replace('%', str(self._page_index))

    def crawl(self):
        with Database() as db:
            for pageNo in range(self._start_page_index, self._limit_page_index):

                time.sleep(1)
                url = self.get_url()
                self._browser.get(url)
                page_source = self._browser.page_source
                print(url)
                html = BeautifulSoup(page_source, 'html.parser')
                print(html)
                search_result = html.find('ul', {"class": "search-list"})
                print(search_result)
                items = search_result.find_all("li", {"class": "search-list__item"})
                print(f'Found {len(items)} on "{self._sourceName}"... ')

                for item in items:
                    try:
                        e_title = item.find('h2', {"class": "listing-search-item__title"})
                        # if we can't find any title matching this element,
                        # it means it's an ad or not what we're looking for!
                        if e_title is None:
                            continue

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

                        h = House(0, self._sourceName, self._source_id, item_url, picture, title, self._city,
                                  'apartment', price_text, price, 1, datetime.now(), rooms, area, interior,
                                  None, None, None, None)

                        db.add_house(h)
                    except Exception as err:
                        print('[{}] Error: {}'.format(self._sourceName, err))
                        continue

        self._browser.quit()
