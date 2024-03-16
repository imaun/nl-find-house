from database import Database
from pararius import Pararius

db = Database()
db.migrate_db()

print('Database migrated successfully...')
db.migrate_db()

print('Database has migrated successfully...')

prius = Pararius(url='https://www.pararius.com/apartments/amsterdam')

houses = prius.get_houses()

print('finished')

