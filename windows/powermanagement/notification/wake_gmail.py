import os
import smtplib
from configparser import ConfigParser
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Read config file if present
config = ConfigParser()
config_file = os.path.join(os.path.dirname(__file__), "..", "..", "..", "common", "config.ini")
if os.path.exists(config_file):
    config.read(config_file)

# Mail variables
mail_host = config.get('mail', 'host') or 'smtp.gmail.com'
mail_port = config.getint('mail', 'port') or 587
mail_sender_address = config.get('mail', 'sender_address') or 'xxx@gmail.com'
mail_sender_pass = config.get('mail', 'sender_pass') or 'xxx'
mail_receiver_address = config.get('mail', 'receiver_address') or 'xxx@gmail.com'

# Setup message
subject = 'SERVER - wake from sleep'
content = 'Wake time: ' + datetime.today().strftime('%d/%m/%Y %H:%M:%S')
message = MIMEMultipart()
message['From'] = mail_sender_address
message['To'] = mail_receiver_address
message['Subject'] = subject
message.attach(MIMEText('\n'.join([l.lstrip() for l in content.split('\n')]), 'plain')) # Trim all leading spaces from multiline format

# Send mail
session = smtplib.SMTP(mail_host, mail_port)
session.starttls() # enable security
session.login(mail_sender_address, mail_sender_pass)
session.sendmail(mail_sender_address, mail_receiver_address, message.as_string())
session.quit()
