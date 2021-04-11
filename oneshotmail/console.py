import os
from mail import OneShot


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
                # TODO: Display information on launching debugging smtpd and require <return> to continue.
                one_shot.simple_test_run()
                input('\nPress <return> to continue.')
            elif self.choice == '3':
                print('\nOne Shot Mail will exit once all emails have been sent.\n')
                one_shot.simple_send()
                break
            elif self.choice == '0':
                print('\nGoodbye!')
                quit()
            else:
                print('\nI did not recognise your selection. Please ensure you enter an option from the menu.')
                input('\nPress <return> to continue.')
