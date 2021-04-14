import csv
import os
import smtplib
import ssl

from email.message import EmailMessage
from pathlib import Path
from dotenv import load_dotenv


class OneShot:

    def __init__(self):
        # TODO: update defaults test
        self.mode_live = False
        self.base_dir = Path('./')
        self.email_dir = Path('email-preparation/')
        self.file_env = Path(self.base_dir, '.env')
        self.file_from = Path(self.email_dir, 'from.txt')
        self.file_subject = Path(self.email_dir, 'subject.txt')
        self.file_message = Path(self.email_dir, 'message.txt')
        self.file_contacts = Path(self.email_dir, 'contacts.csv')
        self.file_contacts_test = Path(self.email_dir, 'contacts-test.csv')
        self.email_host = None
        self.email_port = None
        self.email_host_user = None
        self.email_host_password = None
        self.email_from = None
        self.email_subject = None
        self.email_message = None
        self.emails_sent = []

    def confirm_files_exist(self):
        """Takes a list of filenames, appends them to the base directory and confirms they exist.
        Raises a FileNotFound exception on the first filename that doesn't exist."""
        directories = {'base_dir': self.base_dir, 'email_dir': self.email_dir}
        files = {'file_env': self.file_env, 'file_from': self.file_from, 'file_subject': self.file_subject,
                 'file_message': self.file_message, 'file_contacts': self.file_contacts,
                 'file_contacts_test': self.file_contacts_test}
        missing_directories = {}
        missing_files = {}
        for key, value in directories.items():
            if not Path.is_dir(value):
                missing_directories[key] = value
        for key, value in files.items():
            if not Path.is_file(value):
                missing_files[key] = value
        return missing_directories, missing_files

    def create_files(self, directories, files):
        for directory in directories:
            Path.mkdir(directories[directory])
        for file in files:
            Path.touch(files[file])
            with open(files[file], 'w') as fp:
                if file == 'file_env':
                    fp.write('EMAIL_HOST = mail.domain.dom\n')
                    fp.write('EMAIL_PORT = 465\n')
                    fp.write('EMAIL_HOST_USER = person@domain.dom\n')
                    fp.write('EMAIL_HOST_PASSWORD = supersecretpassword')
                elif file == 'file_from':
                    fp.write('Fist Last <email@domain.dom>')
                    fp.write('\n\nEnsure you delete all content in this file before writing your own to replace it.')
                elif file == 'file_subject':
                    fp.write("Type a short single line that will display in the recipient's inbox.")
                    fp.write('\n\nEnsure you delete all content in this file before writing your own to replace it.')
                elif file == 'file_message':
                    fp.write('Hello {name},\n\n')
                    fp.write('Write your message body here as you normally would over as many lines as you need to.\n')
                    fp.write('\nThe short name in the contacts.csv will appear wherever you place {name}!\n')
                    fp.write('\n--\nFirst Last\nFooter Company & Co.\nemail@domain.dom')
                    fp.write('\n\nEnsure you delete all content in this file before writing your own to replace it.')
                elif file == 'file_contacts':
                    fp.write('Short name,Full name,Email address\n')
                    fp.write('Steve,Steve Parrot,email@domain.dom\n')
                    fp.write('Linda,Linda Baker,email@domain.dom\n\n')
                    fp.write('The short name will be used to replace the {name} tag in the message.txt file. '
                             'The full name and email address fields will be combined to the format '
                             '"Linda Baker <email@domain.dom>" to ensure it displays correctly in the inbox.')
                    fp.write('\n\nEnsure you delete all but the first row of this file before adding your contacts.')
                elif file == 'file_contacts_test':
                    fp.write('Short name,Full name,Email address\n')
                    fp.write('Steve,Steve Parrot,email@domain.dom\n')
                    fp.write('Linda,Linda Baker,email@domain.dom\n\n')
                    fp.write('Use this file to send the email to 2 or 3 accounts you can access on '
                             'different providers. This will allow you to confirm a live send is working '
                             'before you send to the people you care about contacting.')
                    fp.write('\n\nEnsure you delete all but the first row of this file before adding your contacts.')

    def load_env(self):
        load_dotenv()
        self.email_host = os.getenv('EMAIL_HOST')
        self.email_port = os.getenv('EMAIL_PORT')
        self.email_host_user = os.getenv('EMAIL_HOST_USER')
        self.email_host_password = os.getenv('EMAIL_HOST_PASSWORD')

    def collect_message_parts(self):
        """Gets the static email data from the files."""
        with open(self.file_from) as file:
            self.email_from = file.readline()
        with open(self.file_subject) as file:
            self.email_subject = file.readline()
        with open(self.file_message) as file:
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
        with smtplib.SMTP_SSL(self.email_host, self.email_port, context=context) as server:
            server.login(self.email_host_user, self.email_host_password)
            self.send_emails(server)

    def send_emails(self, server):
        """Sends emails to the configured email server."""
        if self.mode_live:
            contacts = self.file_contacts
        else:
            contacts = self.file_contacts_test
        with open(contacts) as file:
            reader = csv.reader(file)
            next(reader)
            self.emails_sent.clear()
            for index, (short_name, full_name, email) in enumerate(reader, start=1):
                msg = EmailMessage()
                msg.set_content(self.email_message.format(name=short_name))
                msg['Subject'] = self.email_subject
                msg['From'] = self.email_from
                msg['To'] = f'{full_name} <{email}>'
                server.send_message(msg)
                self.emails_sent.append({'index': index, 'short_name': short_name,
                                         'full_name': full_name, 'email': email})

    def construct(self):
        self.confirm_files_exist()
        self.collect_message_parts()

    def simple_test_run(self):
        """Runs through a full email construction & send test, but prints to a console using a local debugging smtp."""
        self.construct()
        self.trial_run()

    def simple_send(self):
        """Constructs & sends emails to the configured live smtp without further interaction from the user."""
        self.construct()
        self.email_run()
