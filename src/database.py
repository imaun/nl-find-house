import json
import os
import sqlite3

from models import Source, House


class Database:
    def __init__(self):
        self._dbName = 'nl-house.db'
        self._connection = sqlite3.connect(self._dbName)
        self._cursor = self._connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.close()

    def migrate_db(self):
        print('Starting migrating the Db...')
        sql_source = """
            CREATE TABLE IF NOT EXISTS [Source]
            (
                [id] INTEGER PRIMARY KEY AUTOINCREMENT,
                [name] TEXT NOT NULL,
                [city] TEXT NOT NULL,
                [base_url] TEXT NOT NULL,
                [page_url] TEXT NOT NULL,
                [paging_format] TEXT,
                [start_page_index] INT NOT NULL DEFAULT(0),
                [limit_page_index] INT,
                [status] INTEGER NOT NULL DEFAULT(1),
                [create_date] DATETIME NOT NULL,
                [description] TEXT
            )
        """
        self._connection.execute(sql_source)

        sql_house = """
            CREATE TABLE IF NOT EXISTS [House]
            (
                [id] INTEGER PRIMARY KEY AUTOINCREMENT,
                [source_name] TEXT NOT NULL,
                [source_id] INTEGER NOT NULL,
                [url] TEXT NOT NULL,
                [image_url] TEXT,
                [title] TEXT NOT NULL,
                [city] TEXT,
                [house_type] TEXT NOT NULL,
                [price_text] TEXT,
                [price] INTEGER NOT NULL DEFAULT(0),
                [status] INTEGER NOT NULL DEFAULT(0),
                [create_date] DATETIME NOT NULL,
                [rooms] TEXT,
                [area] TEXT,
                [interior] TEXT,
                [description] TEXT,
                FOREIGN KEY (source_id) REFERENCES Source(id)
            )
        """
        self._connection.execute(sql_house)

        sql_user = """
            CREATE TABLE IF NOT EXISTS [User]
            (
                [id] INTEGER PRIMARY KEY AUTOINCREMENT,
                [username] TEXT NOT NULL,
                [password] TEXT,
                [telegramId] TEXT,
                [email] TEXT,
                [phone] TEXT,
                [create_date] DATETIME NOT NULL,
                [status] INTEGER NOT NULL DEFAULT(0)
            )
        """
        self._connection.execute(sql_user)

        sql_channel = """
            CREATE TABLE IF NOT EXISTS [Channel]
            (
                [id] INTEGER PRIMARY KEY AUTOINCREMENT,
                [title] TEXT,
                [channel_id] TEXT NOT NULL,
                [price_start] INTEGER NOT NULL DEFAULT(0),
                [price_end] INTEGER NOT NULL DEFAULT(0),
                [house_type] TEXT,
                [city] TEXT,
                [status] INTEGER NOT NULL DEFAULT(0),
                [create_date] DATETIME NOT NULL,
                [user_id] INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES User(id)
            )
        """
        self._connection.execute(sql_channel)

        sql_outbox = """
            CREATE TABLE IF NOT EXISTS [Outbox]
            (
                [id] INTEGER PRIMARY KEY AUTOINCREMENT,
                [create_date] DATETIME NOT NULL,
                [house_id] INTEGER NOT NULL,
                [user_id] INTEGER NOT NULL,
                [channel_id] INTEGER NOT NULL,
                FOREIGN KEY (house_id) REFERENCES house(id),
                FOREIGN KEY (user_id) REFERENCES User(id),
                FOREIGN KEY (channel_id) REFERENCES Channel(id)
            )
        """
        self._connection.execute(sql_outbox)
        print('Database {} migrated successfully...'.format(self._dbName))

    def seed_sources(self):
        print('[Db]-> Seeding sources...')
        file_path = 'data/sources.json'
        if not os.path.exists(file_path):
            raise FileNotFoundError('The source seed data at {} not found!'.format(file_path))

        with open(file_path, 'r') as file:
            data = json.load(file)

        sources = []
        for src in data:
            sources.append(Source(**src))

        for source in sources:
            self.add_source(source)
        print('[Db]-> Seeding sources completed.')

    def is_house_url_exists(self, url):
        print('[Db]-> Checking if House url exist: {}'.format(url))
        query = 'SELECT COUNT(id) FROM [house] WHERE [url] = ?'
        count = int(self._cursor.execute(query, [url]).fetchone()[0])
        return count > 0

    def add_source(self, source: Source):
        query = """
            INSERT INTO [Source] 
                ([name], [city], [base_url], [page_url], [paging_format], [start_page_index], [status], [description])
            VALUES
                (?, ?, ?, ? , ?, ?, ?, ?)
        """
        self._cursor.execute(query, [
            source.name, source.city, source.base_url, source.page_url,
            source.paging_format, source.start_page_index, source.status, source.description])
        print('[Db]->[Source] added: name:{} baseUrl:{}, page_url:{}'
              .format(source.name, source.base_url, source.page_url))

    def get_sources_by_name(self, name):
        query = 'SELECT * FROM [Source] WHERE [name] = ?'
        self._cursor.execute(query, [name])
        data = self._cursor.fetchall()

        sources = []
        for row in data:
            sources.append(Source(*row))
        print('[Db]-> Found {} source(s)!'.format(sources.count))

        return sources

    def get_source(self, name: str, page_url: str):
        query = 'SELECT * FROM [Source] WHERE [name] = ? AND [page_url] = ?'
        self._cursor.execute(query, [name, page_url])
        data = self._cursor.fetchone()

        if data:
            return Source(*data)
        return None

    def add_house(self, house: House):
        query = """
            INSERT INTO [House]
                (source_name, source_id, url, image_url, title, city, house_type,
                    price_text, price, status, create_date, rooms, area, interior,
                    description)
            VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self._cursor.execute(query, [
            house.source_name, house.source_id, house.url, house.image_url,
            house.title, house.city, house.house_type, house.price_text,
            house.price, house.status, house.create_date, house.rooms,
            house.area, house.interior, house.description])
        self._connection.commit()
        print('[Db]->[House] added: source:{}, title:{}, url:{}'
              .format(house.source_name, house.title, house.url))
