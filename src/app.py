from database import Database
from pararius import Pararius

__Pararius = 'pararius'

with Database() as db:
    db.migrate_db()
    db.seed_sources()
    sources = db.get_sources_by_name(__Pararius)

for src in sources:
    print('Starting to crawl {} in city {} with url {}'
          .format(src.name, src.city, src.page_url))
    if src.name == __Pararius:
        pararius = Pararius(src)
        pararius.crawl()

print('Finished!')
print('Exiting...')

