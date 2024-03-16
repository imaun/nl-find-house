from database import Database
from pararius import Pararius

db = Database()
db.migrate_db()

db.seed_sources()

sources = db.get_sources_by_name('pararius')
for src in sources:
    print('Starting to crawl {} in city {} with url {}'
          .format(src.name, src.city, src.page_url))

prius = Pararius(url='https://www.pararius.com/apartments/amsterdam')

houses = prius.get_houses()

print('finished')

