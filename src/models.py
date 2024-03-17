from datetime import datetime


class House:
    def __init__(self, id: int = None, source_name: str = None, source_id: int = None, url: str = None,
                 image_url: str = None, title: str = None, city: str = None, house_type: str = None,
                 price_text: str = None, price: int = None, status: int = None, create_date: datetime = None,
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
        if create_date is None:
            create_date = datetime.now()
        self.create_date = create_date
        self.rooms = rooms
        self.area = area
        self.interior = interior
        self.description = description


class Source:
    def __init__(self, id: int = None, name: str = None, city: str = None, base_url: str = None,
                 page_url: str = None, paging_format: str = None, start_page_index: int = None,
                 limit_page_index: int = None, status: int = None, create_date: datetime = None,
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
        if create_date is None:
            self.create_date = datetime.now()
        self.description = description


class User:
    def __init__(self, id, username, telegram_id, email, phone, status, create_date):
        self.id = id
        self.username = username
        self.telegram_id = telegram_id
        self.email = email
        self.phone = phone
        self.status = status
        self.create_date = create_date


class Channel:
    def __init__(self, id, title, channel_id, price_start, price_end,
                 house_type, cities, status, create_date, user_id):
        self.id = id
        self.title = title
        self.channel_id = channel_id
        self.price_start = price_start
        self.price_end = price_end
        self.house_type = house_type
        self.cities = cities
        self.status = status
        self.create_date = create_date
        self.user_id = user_id


class OutboxMessage:
    def __init__(self, id, house_id, user_id, channel_id, create_date):
        self.id = id
        self.house_id = house_id
        self.user_id = user_id
        self.channel_id = channel_id
        self.create_date = create_date
