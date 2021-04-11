from oneshotmail import OneShot
from pathlib import Path


def test_defaults():
    """Using no parameters should invoke defaults."""
    oneshot = OneShot()
    assert oneshot.base_dir == Path('email-preparation/')
    assert oneshot.file_from == 'from.txt'
    assert oneshot.file_subject == 'subject.txt'
    assert oneshot.file_message == 'message.txt'
    assert oneshot.file_contacts == 'contacts.csv'
    assert oneshot.email_from is None
    assert oneshot.email_subject is None
    assert oneshot.email_message is None
    assert oneshot.emails_sent == []
