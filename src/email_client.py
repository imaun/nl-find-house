import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from models import House
import template_render

email_account = os.getenv('NLH_EMAIL_ACCOUNT')
email_password = os.getenv('NLH_EMAIL_PASSWORD')
email_server = os.getenv('NLH_EMAIL_SERVER')
email_port = int(os.getenv('NLH_EMAIL_PORT'))


def send(house: House, target_email: str):
    message = MIMEMultipart('alternative')
    message['Subject'] = f'{house.title}'
    message['From'] = email_account
    message['To'] = target_email
    text_body = template_render.render_template(house, mode='text')
    html_body = template_render.render_template(house, mode='html')
    text_part = MIMEText(text_body, 'plain')
    html_part = MIMEMultipart(html_body, 'html')
    message.attach(text_part)
    message.attach(html_part)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(email_server, email_port, context=context) as server:
        server.login(email_account, email_password)
        server.sendmail(
            email_account, target_email, message.as_string()
        )





