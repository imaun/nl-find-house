import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from models import Source
from models import House


class Funda:
    def __init__(self, source: Source)-> object:
        self._sourceName: str = source.name
        self._sourceId: int = source.id
        self._city: str = source.city
        self._baseUrl: str = source.base_url
        self._pageUrl: str = source.page_url
        self._pagingFormat: str = source.paging_format
        self._startPageIndex: int = source.start_page_index
        self._pageIndex: int = source.start_page_index
        self._limitPageIndex: int = source.limit_page_index
        # Setup the web browser
        browser_options = Options()
        browser_options.add_argument('--disable-extensions')
        browser_options.add_argument('--enable-javascript')
        self._browser = webdriver.Chrome(options=browser_options)



