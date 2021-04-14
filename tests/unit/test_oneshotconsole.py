from oneshotmail import OneShotConsole
from pathlib import Path


def test_defaults():
    """Using no parameters should invoke defaults."""
    console = OneShotConsole()
    assert console.start_test_mail == Path('TestMailServer.bat')
    assert console.start_oneshotmail == Path('OneShotMail.bat')
