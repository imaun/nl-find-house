from database import Database

db = Database()
db.migrate()

print('Database migrated successfully...')
db.migrate_db()

print('Database has migrated successfully...')
