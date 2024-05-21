import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from models import House

email_account = os.getenv('NLH_EMAIL_ACCOUNT')
email_password = os.getenv('NLH_EMAIL_PASSWORD')
email_server = os.getenv('NLH_EMAIL_SERVER')
email_port = os.getenv('NLH_EMAIL_PORT')


def read_text():
    file_path = 'data/email_template.txt'
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'The text template for sending email at {file_path} not found')

    with open(file_path, 'r') as file:
        template = file.read()


def replace_params(house: House, template: str):
    template = template.replace('{title}', house.title)
    template = template.replace('{source}', house.source_name)
    template = template.replace('{url}', house.url)
    template = template.replace('{city}', house.city)
    template = template.replace('{price}', house.price_text)
    template = template.replace('{postal_code}', house.postal_code)
    template = template.replace('{description}', house.description)

    return template

def send(house: House, target_email: str):
    message = MIMEMultipart('alternative')
    message['Subject'] = f'{house.title}'
    message['From'] = email_account
    message['To'] = target_email

    text_template = read_text()
    body = replace_params(house, text_template)



