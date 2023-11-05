import sqlite3


class Database:
    def __init__(self):
        self._dbName = 'nl-house.db'
        self._connection = sqlite3.connect(self._dbName)
        self._cursor = self._connection.cursor()

    def migrate(self):
        sql_house = """
            CREATE TABLE IF NOT EXISTS [House]
            (
                [Id] TEXT NOT NULL PRIMARY KEY,
                [Source] TEXT NOT NULL,
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
                [Description] TEXT
            )
        """
        self._connection.execute(sql_house)

        sql_user = """
            CREATE TABLE IF NOT EXISTS [User]
            (
                [Id] TEXT NOT NULL PRIMARY KEY,
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
                [Id] TEXT NOT NULL PRIMARY KEY,
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
                [Id] TEXT NOT NULL PRIMARY KEY,
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