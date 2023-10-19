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
