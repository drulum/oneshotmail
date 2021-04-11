import os
from oneshotmail.mail import OneShot


class OneShotConsole:

    def __init__(self):
        self.choice = None

    def clear_screen(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def process_menu(self):
        self.clear_screen()
        print('One Shot Mail')
        print('=============\n')
        print('1. Preview the email that will be sent.')
        print('2. Trial run with files in the email preparation sub directory.')
        print('3. LIVE RUN with files in the email preparation sub directory.')
        print('0. Exit One Shot Mail.\n')
        self.choice = input('Enter option: ')

    def print_sent_emails(self, one_shot):
        print('\nEmails were sent to the following people:\n')
        for email in one_shot.emails_sent:
            print(f'{email["index"]}. {email["short_name"]} at "{email["full_name"]} <{email["email"]}>".')
        print('\nThe trial run should now have completed.')
        input('\nPress <return> to continue.')

    def run(self):
        one_shot = OneShot()
        while True:
            self.process_menu()
            if self.choice == '1':
                one_shot.construct()
                print(f'\nEmails will be sent from "{one_shot.email_from}".')
                print(f'\nThe subject line is "{one_shot.email_subject}"')
                print(f'\nThe message body is:\n{one_shot.email_message}')
                input('\nPress <return> to continue.')
            elif self.choice == '2':
                print('\nBefore continuing, carry out the following instructions.')
                print('\n1. Open a second console window.')
                print('   (Windows: Command Prompt. Linux: terminal)')
                print('\n2. In the new console window, enter the following command.')
                print('   (Linux: you may need to prefix with "sudo")')
                print('   python -m smtpd -c DebuggingServer -n localhost:1025')
                input('\nWhen you are ready to carry out the trial run, press <return>.')
                one_shot.simple_test_run()
                self.print_sent_emails(one_shot)
            elif self.choice == '3':
                print('\nOne Shot Mail will exit once all emails have been sent.')
                one_shot.simple_send()
                self.print_sent_emails(one_shot)
                break
            elif self.choice == '0':
                print('\nGoodbye!')
                quit()
            else:
                print('\nI did not recognise your selection. Please ensure you enter an option from the menu.')
                input('\nPress <return> to continue.')
