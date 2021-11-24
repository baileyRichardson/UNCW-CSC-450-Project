
import pytest
def test_send_email():
    from Mail import send_email

    # does it send emails
    assert send_email("baileyr0826@gmailcom", "baileyr0826@gmail.com", 1)