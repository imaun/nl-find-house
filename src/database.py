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
                [Id] INTEGER PRIMARY KEY AUTOINCREMENT,
                [Name] TEXT NOT NULL,
                [City] TEXT NOT NULL,
                [Url] TEXT NOT NULL,
                [Status] INTEGER NOT NULL DEFAULT(1),
                [Description] TEXT
            )
        """
        self._connection.execute(sql_source)

        sql_house = """
            CREATE TABLE IF NOT EXISTS [House]
            (
                [Id] INTEGER PRIMARY KEY AUTOINCREMENT,
                [SourceName] TEXT NOT NULL,
                [SourceId] INTEGER NOT NULL,
                [Url] TEXT NOT NULL,
                [Image_Url] TEXT,
                [Title] TEXT NOT NULL,
                [City] TEXT,
                [House_Type] TEXT NOT NULL,
                [Price_Text] TEXT,
                [Price] INTEGER NOT NULL DEFAULT(0),
                [Status] INTEGER NOT NULL DEFAULT(0),
                [Create_Date] DATETIME NOT NULL,
                [Rooms] TEXT,
                [Area] TEXT,
                [Interior] TEXT,
                [Description] TEXT,
                FOREIGN KEY (SourceId) REFERENCES Source(Id)
            )
        """
        self._connection.execute(sql_house)

        sql_user = """
            CREATE TABLE IF NOT EXISTS [User]
            (
                [Id] INTEGER PRIMARY KEY AUTOINCREMENT,
                [Username] TEXT NOT NULL,
                [TelegramId] TEXT,
                [Email] TEXT,
                [Phone] TEXT,
                [Create_Date] DATETIME NOT NULL,
                [Status] INTEGER NOT NULL DEFAULT(0)
            )
        """
        self._connection.execute(sql_user)

        sql_channel = """
            CREATE TABLE IF NOT EXISTS [Channel]
            (
                [Id] INTEGER PRIMARY KEY AUTOINCREMENT,
                [Title] TEXT,
                [ChannelId] TEXT NOT NULL,
                [Price_Start] INTEGER NOT NULL DEFAULT(0),
                [Price_End] INTEGER NOT NULL DEFAULT(0),
                [House_Type] TEXT,
                [Cities] TEXT,
                [Status] INTEGER NOT NULL DEFAULT(0),
                [Create_Date] DATETIME NOT NULL,
                [UserId] INTEGER NOT NULL,
                FOREIGN KEY (UserId) REFERENCES User(Id)
            )
        """
        self._connection.execute(sql_channel)

        sql_outbox = """
            CREATE TABLE IF NOT EXISTS [Outbox]
            (
                [Id] INTEGER PRIMARY KEY AUTOINCREMENT,
                [Create_Date] DATETIME NOT NULL,
                [HouseId] INTEGER NOT NULL,
                [UserId] INTEGER NOT NULL,
                [ChannelId] INTEGER NOT NULL,
                FOREIGN KEY (HouseId) REFERENCES House(Id),
                FOREIGN KEY (UserId) REFERENCES User(Id),
                FOREIGN KEY (ChannelId) REFERENCES Channel(Id)
            )
        """
        self._connection.execute(sql_outbox)

    def is_house_url_exists(self, url):
        query = 'SELECT COUNT(Id) FROM [House] WHERE [Url] = ?'
        count = int(self._cursor.execute(query, [url]).fetchone()[0])
        return count == 0

    def get_source_by_name(self, name):
        query = 'SELECT * FROM [Source] WHERE [Name] = ?'
        self._cursor.execute(query, [name])
        data = self._cursor.fetchall()[0]
        return Source(*data)

    def insert_house(self, house: House):
        query = """
            INSERT INTO [House]
                (SourceName, SourceId, Url, ImageUrl, Title, City, House_Type,
                    Price_Text, Price, Status, Create_Date, Rooms, Area, Interior,
                    Description)
            VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self._cursor.execute(query, [
            house.source_name,
            house.source_id,
            house.url,
            house.image_url,
            house.title,
            house.city,
            house.house_type,
            house.price_text,
            house.price,
            house.status,
            house.create_date,
            house.rooms,
            house.area,
            house.interior,
            house.description
        ])
        self._connection.commit()
