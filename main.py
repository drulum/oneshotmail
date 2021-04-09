import csv
import os
import smtplib
import ssl
from email.message import EmailMessage
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

email_host = os.getenv('EMAIL_HOST')
email_port = os.getenv('EMAIL_PORT')
email_host_user = os.getenv('EMAIL_HOST_USER')
email_host_password = os.getenv('EMAIL_HOST_PASSWORD')


class OneShot:

    def __init__(self):
        self.base_dir = Path('email-preparation/')
        self.file_from = 'from.txt'
        self.file_subject = 'subject.txt'
        self.file_message = 'message.txt'
        self.file_contacts = 'contacts.csv'
        self.email_from = None
        self.email_subject = None
        self.email_message = None

        # Ensure the files exist in the email-preparation subdir before continuing.
        self.confirm_files_exist([self.file_from, self.file_subject, self.file_message, self.file_contacts])

        # Collect the data that does not change.
        self.create_message()

        # Send the constructed emails.
        self.send_emails()

    def confirm_files_exist(self, files):
        """Takes a list of filenames, appends them to the base directory and confirms they exist.
        Raises a FileNotFound exception on the first filename that doesn't exist."""
        for file in files:
            if not Path.is_file(Path(self.base_dir, file)):
                raise FileNotFoundError(f'The file "{file}" was not found in the directory "{self.base_dir}".')

    def create_message(self):
        with open(Path(self.base_dir, self.file_from)) as file:
            self.email_from = file.readline()
        with open(Path(self.base_dir, self.file_subject)) as file:
            self.email_subject = file.readline()
        with open(Path(self.base_dir, self.file_message)) as file:
            self.email_message = file.read()

    def send_emails(self):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(email_host, email_port, context=context) as server:
            server.login(email_host_user, email_host_password)
            with open(Path(self.base_dir, self.file_contacts)) as file:
                reader = csv.reader(file)
                next(reader)
                for index, (short_name, full_name, email) in enumerate(reader, start=1):
                    msg = EmailMessage()
                    msg.set_content(self.email_message.format(name=short_name))
                    msg['Subject'] = self.email_subject
                    msg['From'] = self.email_from
                    msg['To'] = f'{full_name} <{email}>'
                    server.send_message(msg)
                    print(f'{index}. Message sent to {short_name} at "{full_name} <{email}>".')


if __name__ == '__main__':
    try:
        one_shot = OneShot()
    except FileNotFoundError as err:
        print(err)
        print('Please run the application again once this has been corrected.')
        quit()

    print('\nRun complete. All emails sent successfully.')
