from database import Database

db = Database()
db.migrate_db()

print('Database has migrated successfully...')