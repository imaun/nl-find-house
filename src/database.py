import sqlite3
from models import Source, House


class Database:
    def __init__(self):
        self._dbName = 'nl-house.db'
        self._connection = sqlite3.connect(self._dbName)
        self._cursor = self._connection.cursor()

    def migrate_db(self):
        sql_source = """
            CREATE TABLE IF NOT EXISTS [Source]
            (
                [id] INTEGER PRIMARY KEY AUTOINCREMENT,
                [name] TEXT NOT NULL,
                [city] TEXT NOT NULL,
                [base_url] TEXT NOT NULL,
                [page_url] TEXT NOT NULL,
                [paging_format] TEXT,
                [status] INTEGER NOT NULL DEFAULT(1),
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

    def is_house_url_exists(self, url):
        query = 'SELECT COUNT(id) FROM [house] WHERE [url] = ?'
        count = int(self._cursor.execute(query, [url]).fetchone()[0])
        return count == 0

    def add_source(self, source: Source):
        query = """
            INSERT INTO [Source] 
                ([name], [city], [base_url], [page_url], [paging_format], [status], [description])
            VALUES
                (?, ?, ?, ? , ?, ?, ?)
        """
        self._cursor.execute(query, [
            source.name, source.city, source.base_url,
            source.page_url, source.status, source.description])

    def get_source_by_name(self, name):
        query = 'SELECT * FROM [Source] WHERE [name] = ?'
        self._cursor.execute(query, [name])
        data = self._cursor.fetchone()
        # if exists
        if data: return Source(*data)
        # try to create default source
        return Source(*data)

    def insert_house(self, house: House):
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
