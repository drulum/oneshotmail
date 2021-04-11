from oneshotmail import OneShotConsole


def test_defaults():
    """Using no parameters should invoke defaults."""
    console = OneShotConsole()
    assert console.choice is None
