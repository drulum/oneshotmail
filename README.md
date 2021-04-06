Use Case
========
Occasionally you may be required to send the same email to a number of people. This may be for regulatory reasons for a solicitor or accountant, or simply a group of family members you need to coordinate with. Using something like MailChimp would be overkill and allowing the option to unsubscribe would cause a problem for future required emails.

The emails need to be sent through a legitimate mail server, ideally the same server and account you normally use in order to reduce the risk they will be considered SPAM.

**DO NOT USE THIS SCRIPT TO SPAM PEOPLE!**

For emails that are not ***required*** to be sent, use a mailing list instead and ensure people are on it by choice and can unsubscribe easily.

Setup
=====
Rename **.env-template** to **.env** and add the necessary information for your mail server.

You will need the following files. Either create them yourself or rename those provided with **-template**.
- **from.txt** - Single line with no spaces at the start or end in the format ```Sender Name <sender@address.com>```
- **subject.txt** - Single line with no spaces at the start or end to be used as the email subject.
- **message.txt** - Plain text over multiple lines as required. Personalise the email using ```{name}``` where you want to display the recipient's short name.
- **contacts.csv** - First line should contain ```Short name,Full name,Email address``` with each subsequent line being the information for a single recipient. No spaces before or after the commas. The To field will be constructed as ```Full Name <Email address>```

Testing before sending
======================

I haven't added a TEST option to the script yet, so this next bit is really for my own benefit at present. For now you can manually adjust the script if you understand it.

Start local smtpd on Windows for testing with the following command. On Linux you may need to precede the command with ```sudo```

```commandline
python -m smtpd -c DebuggingServer -n localhost:1025
```
