from models import House
import os

TEXT_TEMPLATE_PATH = 'data/email_template.txt'
HTML_TEMPLATE_PATH = 'data/email_template.html'


class TemplateModeNotSupported(Exception):
    pass


def render_template(house: House, mode: str):
    if mode == 'text':
        template = read_template_file(TEXT_TEMPLATE_PATH)
    elif mode == 'html':
        template = read_template_file(HTML_TEMPLATE_PATH)
    else:
        raise TemplateModeNotSupported(f'Template mode "{mode}" not supported.')

    template = template.replace('{title}', house.title)
    template = template.replace('{source}', house.source_name)
    template = template.replace('{url}', house.url)
    template = template.replace('{city}', house.city)
    template = template.replace('{price}', house.price_text)
    template = template.replace('{postal_code}', house.postal_code)
    template = template.replace('{description}', house.description)

    return template


def read_template_file(file_path: str):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'The text template for sending email at {file_path} not found')

    with open(file_path, 'r') as file:
        template = file.read()

    return template
