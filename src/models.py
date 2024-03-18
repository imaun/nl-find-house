from datetime import datetime


class House:
    def __init__(self, id: int = None, source_name: str = None, source_id: int = None, url: str = None,
                 image_url: str = None, title: str = None, city: str = None, house_type: str = None,
                 price_text: str = None, price: int = None, status: int = 1, create_date: datetime = datetime.now(),
                 rooms: str = None, area: str = None, interior: str = None, description: str = None):
        self.id = id
        self.source_name = source_name
        self.source_id = source_id
        self.url = url
        self.image_url = image_url
        self.title = title
        self.city = city
        self.house_type = house_type
        self.price_text = price_text
        self.price = price
        self.status = status
        self.create_date = create_date
        self.rooms = rooms
        self.area = area
        self.interior = interior
        self.description = description


class Source:
    def __init__(self, id: int = None, name: str = None, city: str = None, base_url: str = None,
                 page_url: str = None, paging_format: str = None, start_page_index: int = None,
                 limit_page_index: int = None, status: int = 1, create_date: datetime = datetime.now(),
                 description: str = None):
        self.id = id
        self.name = name
        self.city = city
        self.base_url = base_url
        self.page_url = page_url
        self.paging_format = paging_format
        self.start_page_index = start_page_index
        self.limit_page_index = limit_page_index
        self.status = status
        self.create_date = create_date
        self.description = description


class User:
    def __init__(self, id: int = None, username: str = None, telegram_id: str = None,
                 email: str = None, phone: str = None, status: int = 1, create_date: datetime = datetime.now()):
        self.id = id
        self.username = username
        self.telegram_id = telegram_id
        self.email = email
        self.phone = phone
        self.status = status
        self.create_date = create_date


# Channels can be Telegram channels or EmailAccounts
class Channel:
    def __init__(self, id: int = None, title: str = None, channel_id: str = None, channel_type: str = None,
                 price_start: int = None, price_end: int = None, house_type: str = None, city: str = None,
                 status: int = 1, create_date: datetime = datetime.now(), user_id: int = None):
        self.id = id
        self.title = title
        self.channel_id = channel_id
        self.channel_type = channel_type
        self.price_start = price_start
        self.price_end = price_end
        self.house_type = house_type
        self.city = city
        self.status = status
        self.create_date = create_date
        self.user_id = user_id


class OutboxMessage:
    def __init__(self, id: int = None, house_id: int = None, user_id: int = None,
                 channel_id: str = None, create_date: datetime = datetime.now()):
        self.id = id
        self.house_id = house_id
        self.user_id = user_id
        self.channel_id = channel_id
        self.create_date = create_date
