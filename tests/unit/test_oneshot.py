from oneshotmail import OneShot
from pathlib import Path


def test_defaults():
    """Using no parameters should invoke defaults."""
    oneshot = OneShot()
    assert oneshot.base_dir == Path('./')
    assert oneshot.email_dir == Path('email-preparation/')
    assert oneshot.file_env == Path(oneshot.base_dir, '.env')
    assert oneshot.file_from == Path(oneshot.email_dir, 'from.txt')
    assert oneshot.file_subject == Path(oneshot.email_dir, 'subject.txt')
    assert oneshot.file_message == Path(oneshot.email_dir, 'message.txt')
    assert oneshot.file_contacts == Path(oneshot.email_dir, 'contacts.csv')
    assert oneshot.email_host == None
    assert oneshot.email_port == None
    assert oneshot.email_host_user == None
    assert oneshot.email_host_password == None
    assert oneshot.email_from is None
    assert oneshot.email_subject is None
    assert oneshot.email_message is None
    assert oneshot.emails_sent == []
