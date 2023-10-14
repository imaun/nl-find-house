import requests
from bs4 import BeautifulSoup

url = 'https://www.pararius.com/apartments/amsterdam'

page = requests.get(url)
html = BeautifulSoup(page.content, 'html.parser')

search_result = html.find('ul', {"class": "search-list"})
items = search_result.find_all("li", {"class": "search-list__item"})
print(len(items))
for res in items:
    print(res, end="\n"*2)

print('end')