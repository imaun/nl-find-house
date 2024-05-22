import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from models import House
import template_render

email_account = os.getenv('NLH_EMAIL_ACCOUNT')
email_password = os.getenv('NLH_EMAIL_PASSWORD')
email_server = os.getenv('NLH_EMAIL_SERVER')
email_port = os.getenv('NLH_EMAIL_PORT')


def send(house: House, target_email: str):
    message = MIMEMultipart('alternative')
    message['Subject'] = f'{house.title}'
    message['From'] = email_account
    message['To'] = target_email
    text_body = template_render.render_template(house, mode='text')
    html_body = template_render.render_template(house, mode='html')
    text_email = MIMEText(text_body, 'plain')
    text_body = MIMEMultipart(html_body, 'html')




