# nl-find-house
Crawler to find a proper house in the Netherlands. For now it only supports Pararius, but you can easily add new sites to it.

# How to use
- First, make sure you have python installed on your machine.
- Clone this repo `git clone https://github.com/imaun/nl-find-house.git`
- Go to the src and run `pip install -r requirements.txt`
- Run `python app.py`

# Configure Crawler
In order to configure this app to crawl the data you really need, you can edit [sources.json](https://github.com/imaun/nl-find-house/blob/master/src/data/sources.json) file in your local machine.
 For example, if you are looking for a house in Utrecht, go to Paraius and search for Utrecht, copy the url from your browser (remember to follow to convension of `base_url` and the rest!) and add a new source for the app to crawl :

 ```json
{
    "id": 1,
    "name": "pararius",
    "city": "utrecht",
    "base_url": "https://www.pararius.com",
    "page_url": "/apartments/utrecht",
    "paging_format": "/page-%",
    "start_page_index": 1,
    "limit_page_index": 30,
    "status": 1,
    "description": null
  }
```

# How does it work?
This app uses selenium to automate and simulate user bahaviour in searching for homes. So when you are running this script, it will open up your chrome browser and starts to browse the urls you set in `sources.json` file. The reason for using selenuim and an actual browser is because of the fact that these websites are using protection against bots and crawlers that don't act like a real user using a normal browser!

After the crawling is completed, a SQLite database will be generated automatically `nl-house.db` located in the root directory. You can find the crawled pages there.

# What's nex
- I'm going to add support for other webiste like funda
- Ability to set min and max price for rents
- Send Email alerts for new items
- Send Telegram messages for new itesm in a Telegram channel

