import os
import sys

from oneshotmail.mail import OneShot
from pathlib import Path


class OneShotConsole:

    def __init__(self):
        # FIXME: need to form launcher names based on OS
        self.start_test_mail = Path('TestMailServer.bat')
        self.start_oneshotmail = Path('OneShotMail.bat')

    def launchers_exist(self):
        files = {'start_test_mail': self.start_test_mail, 'start_oneshotmail': self.start_oneshotmail}
        missing_files = {}
        for key, value in files.items():
            if not Path.is_file(value):
                missing_files[key] = value
        return missing_files

    def create_launchers(self, files):
        if os.name == 'nt':
            for file in files:
                Path.touch(files[file])
                with open(files[file], 'w') as fp:
                    if file == 'start_test_mail':
                        fp.write('@echo off')
                        fp.write('\ncmd /k "python -m smtpd -c DebuggingServer -n localhost:1025"')
                        fp.write('\npause')
                    elif file == 'start_oneshotmail':
                        fp.write('@echo off\n')
                        fp.write(r'cmd /k "venv\Scripts\activate & python -m oneshotmail & deactivate & exit"')
                        fp.write('\npause')
        else:
            for file in files:
                # TODO: Need to set scrips as user executable.
                Path.touch(files[file])
                with open(files[file], 'w') as fp:
                    if file == 'start_test_mail':
                        fp.write('echo "Test mail server is ready."\n')
                        fp.write('python -m smtpd -c DebuggingServer -n localhost:1025')
                    elif file == 'start_oneshotmail':
                        fp.write('./venv/bin/activate\n')
                        fp.write('python -m oneshotmail\n')
                        fp.write('deactivate\n')
                        fp.write('exit')

    def clear_screen(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def process_menu(self, one_shot):
        while True:
            self.clear_screen()
            print('One Shot Mail')
            print('=============\n')
            print('1. Preview the email that will be sent.')
            print('2. Trial run with files in the email preparation sub directory.')
            print('3. LIVE RUN with files in the email preparation sub directory.')
            if one_shot.mode_live:
                print('\nYou are currently using your LIVE RUN contacts file.')
                print('C. Change to your TEST RUN contacts file.')
            else:
                print('\nYou are currently using your TEST RUN contacts file.')
                print('C. Change to your LIVE RUN contacts file.')
            print('\nTwo scripts can be created to start the test email server and this application.')
            print('L. Generate launcher scripts.')
            print('\n0. Exit One Shot Mail.\n')
            choice = input('Enter option: ')
            if choice == '1':
                one_shot.construct()
                print(f'\nEmails will be sent from "{one_shot.email_from}".')
                print(f'\nThe subject line is "{one_shot.email_subject}"')
                print(f'\nThe message body is:\n{one_shot.email_message}')
                input('\nPress <return> to continue.')
            elif choice == '2':
                print('\nBefore continuing, carry out the following instructions.')
                print('\n1. Open a second console window.')
                print('   (Windows: Command Prompt. Linux: terminal)')
                print('\n2. In the new console window, enter the following command.')
                print('   (Linux: you may need to prefix with "sudo")')
                print('   python -m smtpd -c DebuggingServer -n localhost:1025')
                input('\nWhen you are ready to carry out the trial run, press <return>.')
                one_shot.simple_test_run()
                self.print_sent_emails(one_shot)
            elif choice == '3':
                print('\nBeginning the send process. It may take a few minutes before it completes, please be patient.')
                one_shot.load_env()
                one_shot.simple_send()
                self.print_sent_emails(one_shot)
            elif choice == '0':
                print('\nGoodbye!')
                sys.exit()
            elif choice in ['C', 'c']:
                if one_shot.mode_live:
                    one_shot.mode_live = False
                    print('\nThe TEST contacts file will now be used.')
                    input('\nPress <return> to continue.')
                else:
                    one_shot.mode_live = True
                    print('\nThe LIVE contacts file will now be used.')
                    input('\nPress <return> to continue.')
            elif choice in ['L', 'l']:
                files = self.launchers_exist()
                if files:
                    self.create_launchers(files)
                    print('\nThe launchers have been created. Test them and edit paths if necessary.')
                    input('\nPress <return> to continue.')
                else:
                    print('\nIt seems both launcher scripts already exist, so no action has been taken.')
                    print('\nTo re-create them delete them from your One Shot Mail directory then choose '
                          'this option again.')
                    input('\nPress <return> to continue.')
            else:
                print('\nI did not recognise your selection. Please ensure you enter an option from the menu.')
                input('\nPress <return> to continue.')

    def print_sent_emails(self, one_shot):
        print('\nEmails were sent to the following people:\n')
        for email in one_shot.emails_sent:
            print(f'{email["index"]}. {email["short_name"]} at "{email["full_name"]} <{email["email"]}>".')
        print('\nThe trial run should now have completed.')
        input('\nPress <return> to continue.')

    def run(self):
        one_shot = OneShot()
        # Check the required directories and files exist.
        directories, files = one_shot.confirm_files_exist()
        # If any directories or files do not exist, ask the user if they should be created.
        if directories or files:
            if directories:
                for directory in directories:
                    print('Directory: ', directories[directory])
            if files:
                for file in files:
                    print('File: ', files[file])
            choice = None
            while choice not in ['Y', 'y', 'N', 'n', '']:
                choice = input('Would you like these to be created for you? [Y/n] ')
            if choice in ['Y', 'y', '']:
                one_shot.create_files(directories, files)
                # Advise the user they need to edit the newly created files before continuing.
                print('\nThe files have been created but are currently empty.\n\nPlease add the necessary '
                      'information to each before you re-run this application.')
                sys.exit()
            else:
                # If the files don't exist, the program can't do anything useful.
                print("\nThe program can't continue until these files exist.\n\nPlease either re-run this "
                      "program and allow it to generate the files for you or create them yourself before re-running.")
                sys.exit()

        self.process_menu(one_shot)
