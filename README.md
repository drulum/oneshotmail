Use Case
========
Occasionally you may be required to send the same email to a number of people. This may be for regulatory reasons for a solicitor or accountant, or simply a group of family members you need to coordinate with. Using something like MailChimp would be overkill and allowing the option to unsubscribe would cause a problem for future required emails.

The emails need to be sent through a legitimate mail server, ideally the same server and account you normally use in order to reduce the risk they will be considered SPAM.

**DO NOT USE THIS SCRIPT TO SPAM PEOPLE!**

For emails that are not ***required*** to be sent, use a mailing list instead and ensure people are on it by choice and can unsubscribe easily.

Setup
=====

TODO: something about venv and requirements.txt

The base directory has the file **.env-template**. Rename this to **.env** and add the necessary information for your mail server.

You will need the following files. Either create them yourself or rename those provided in the **email-preparation** folder with **-template**.
- **from.txt** - Single line with no spaces at the start or end in the format ```Sender Name <sender@address.com>```
- **subject.txt** - Single line with no spaces at the start or end to be used as the email subject.
- **message.txt** - Plain text over multiple lines as required. Personalise the email using ```{name}``` where you want to display the recipient's short name.
- **contacts.csv** - First line should contain ```Short name,Full name,Email address``` with each subsequent line being the information for a single recipient. No spaces before or after the commas. The To field will be constructed as ```Full Name <Email address>```

Running main.py directly
========================

This will provide you with a simple console application allowing you to choose whether to carry out a trial run or send the emails. Both options use the files stored in the **email-preparation** folder and require no further interaction.

In order to carry out a trial run, issue the following command in a separate console. On Linux you may need to precede the command with ```sudo```. The emails will be constructed normally and then printed to the console running the smtpd DebuggingServer.

```commandline
python -m smtpd -c DebuggingServer -n localhost:1025
```

Calling the class from your own application
===========================================

Import the class normally, adjusting for how and where you have the file on your system.

```python
from main import OneShot
```

Create an instance of the class.

```python
mailshot = OneShot()
```

Once you have activated an smtpd DebuggingServer (see previous section), you can carry out a test run with the ```mailshot.simple_test_run()``` method. Alternatively you can send the emails by calling ```mailshot.simple_send()```. Neither of these methods require further interaction to complete.

If you prefer to control the flow manually you can do so by calling the remaining methods as required.

TODO: document the class methods fully once complete.