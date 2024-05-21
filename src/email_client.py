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




class EmailClient:

    def send(self, house: House, target_email: str):
        message = MIMEMultipart('alternative')
        message['Subject'] = f'{house.title}'
        message['From'] = email_account
        message['To'] = target_email


