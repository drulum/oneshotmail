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

    def confirm_files_exist(self):
        """Takes a list of filenames, appends them to the base directory and confirms they exist.
        Raises a FileNotFound exception on the first filename that doesn't exist."""
        files = [self.file_from, self.file_subject, self.file_message, self.file_contacts]
        for file in files:
            if not Path.is_file(Path(self.base_dir, file)):
                raise FileNotFoundError(f'The file "{file}" was not found in the directory "{self.base_dir}".')

    def collect_message_parts(self):
        """Gets the static email data from the files."""
        with open(Path(self.base_dir, self.file_from)) as file:
            self.email_from = file.readline()
        with open(Path(self.base_dir, self.file_subject)) as file:
            self.email_subject = file.readline()
        with open(Path(self.base_dir, self.file_message)) as file:
            self.email_message = file.read()

    def trial_run(self):
        """Constructs the emails normally but send to a local test smtpd for printing to console.

        Start a local debugging smtp with the following command. May need to use sudo on Linux.
        python -m smtpd -c DebuggingServer -n localhost:1025"""
        with smtplib.SMTP('localhost', 1025) as server:
            self.send_emails(server)

    def email_run(self):
        """Connects to the live email server securely and send the emails."""
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(email_host, email_port, context=context) as server:
            server.login(email_host_user, email_host_password)
            self.send_emails(server)

    def send_emails(self, server):
        """Sends emails to the configured email server."""
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

    def construct(self):
        self.confirm_files_exist()
        self.collect_message_parts()

    def preview(self):
        self.construct()
        print(f'\nEmails will be sent from "{self.email_from}".')
        print(f'The subject line is "{self.email_subject}"')
        print(f'The message body is:\n{self.email_message}')

    def simple_test_run(self):
        """Runs through a full email construction & send test, but prints to a console using a local debugging smtp."""
        self.construct()
        self.trial_run()

    def simple_send(self):
        """Constructs & sends emails to the configured live smtp without further interaction from the user."""
        self.construct()
        self.email_run()


def display_menu():
    print('\nOne Shot Mail')
    print('=============\n')
    print('1. Preview the email that will be sent.')
    print('2. Trial run with files in the email preparation sub directory.')
    print('3. LIVE RUN with files in the email preparation sub directory.')
    print('0. Exit One Shot Mail.\n')


if __name__ == '__main__':
    try:
        one_shot = OneShot()
        display_menu()
        choice = input('Enter option: ')
        while True:
            if choice == '1':
                one_shot.preview()
                display_menu()
                choice = input('Enter option: ')
            elif choice == '2':
                one_shot.simple_test_run()
                break
            elif choice == '3':
                one_shot.simple_send()
                break
            elif choice == '0':
                print('\nGoodbye!')
                quit()
            else:
                choice = input('\nPlease ensure you select an option from the list: ')
    except FileNotFoundError as error:
        print(f'\n{error}')
        print('Please run the application again once this has been corrected.')
        quit()

    print('\nRun complete. All emails sent successfully.\nGoodbye!')
