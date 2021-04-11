from console import OneShotConsole

try:
    console = OneShotConsole()
    console.run()
except FileNotFoundError as error:
    print(f'\n{error}')
    print('Please run the application again once this has been corrected.')
    quit()

print('\nRun complete. All emails sent successfully.\n\nGoodbye!')
