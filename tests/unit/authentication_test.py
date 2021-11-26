"""This files provides the unit test for the authentication aspect of the site. - Tan Ngo
Simply run this file to verify the test"""

import pytest
from requests import HTTPError
import main

def test_create_invalidpass():
    # The email is valid, while the password is not (less than 8 characters).
    validemail = "sample@uncw.edu"
    invalidpass = "pass"
    # Since the password is too short, an error is thrown and the account is not created.
    with pytest.raises(expected_exception=HTTPError):
        main.authentication.sign_in_with_email_and_password(validemail, invalidpass)

def test_create_invalidemail():
    # The email is invalid because it is not an email, while the password is valid.
    invalidemail = "sample"
    validpass = "password"
    # Since the email is invalid, an error is thrown and the account is not created.
    with pytest.raises(expected_exception=HTTPError):
        main.authentication.sign_in_with_email_and_password(invalidemail, validpass)

def test_authenticate_valid():
    # The valid email and password is already registered with firebase
    validemail = "tdn5547@uncw.edu"
    validpass = "password"
    # Since the information is valid, the authentication should pass with no errors
    assert main.authentication.sign_in_with_email_and_password(validemail, validpass)

def test_authenticate_invalid():
    # The email and password is not registered with firebase
    invalidemail = "tdn5548@uncw.edu"
    invalidpass = "password1"
    # Since the account has not been created, it will throw an error as there is not a valid account
    with pytest.raises(expected_exception=HTTPError):
        main.authentication.sign_in_with_email_and_password(invalidemail, invalidpass)
