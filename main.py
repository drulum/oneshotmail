import csv
import os
import smtplib
import ssl
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

email_host = os.getenv('EMAIL_HOST')
email_port = os.getenv('EMAIL_PORT')
email_host_user = os.getenv('EMAIL_HOST_USER')
email_host_password = os.getenv('EMAIL_HOST_PASSWORD')

data_directory = 'email-preparation'

try:
    with open('./' + data_directory + '/' + 'from.txt') as fp:
        email_from = fp.readline()
except FileNotFoundError:
    print(f"I can't find your 'from.txt' file. Make sure it's in the '{data_directory}' folder!")
    quit()

try:
    with open('./' + data_directory + '/' + 'subject.txt') as fp:
        email_subject = fp.readline()
except FileNotFoundError:
    print(f"I can't find your 'subject.txt' file. Make sure it's in the '{data_directory}' folder!")
    quit()

try:
    with open('./' + data_directory + '/' + 'message.txt') as fp:
        email_message = fp.read()
except FileNotFoundError:
    print(f"I can't find your 'message.txt' file. Make sure it's in the '{data_directory}' folder!")
    quit()

context = ssl.create_default_context()

with smtplib.SMTP_SSL(email_host, email_port, context=context) as server:
    server.login(email_host_user, email_host_password)
    try:
        with open('./' + data_directory + '/' + 'contacts.csv') as file:
            reader = csv.reader(file)
            next(reader)
            for index, (short_name, full_name, email) in enumerate(reader, start=1):
                msg = EmailMessage()
                msg.set_content(email_message.format(name=short_name))
                msg['Subject'] = email_subject
                msg['From'] = email_from
                msg['To'] = f'{full_name} <{email}>'
                server.send_message(msg)
                print(f'{index}. Message sent to {short_name} at "{full_name} <{email}>".')
    except FileNotFoundError:
        print(f"I can't find your 'contacts.csv' file. Make sure it's in the '{data_directory}' folder!")
        quit()

print('\nRun complete. All emails sent successfully.')
