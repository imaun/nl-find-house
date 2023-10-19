class House:
    def __int__(self, id, source_name, source_id, url, image_url,
                title, city, house_type, price_text, price,
                status, create_date, rooms, area, interior, description):
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
    def __int__(self, id, name, city, url, status, description):
        self.id = id
        self.name = name
        self.city = city
        self.url = url
        self.status = status
        self.description = description


class User:
    def __int__(self, id, username, telegram_id, email, phone, status, create_date):
        self.id = id
        self.username = username
        self.telegram_id = telegram_id
        self.email = email
        self.phone = phone
        self.status = status
        self.create_date = create_date


class Channel:
    def __int__(self, id, title, channel_id, price_start, price_end,
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
