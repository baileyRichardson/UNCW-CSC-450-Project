"""This files provides the unit test for the userManager file. - Tan Ngo
Simply run this file to verify the test"""

import pytest
from userManager import userManager

def test_instantiate_user():
    # The email that a user is created with.
    email = "example1@gmail.com"
    # instantiating a new user with above email.
    newUser = userManager(email)
    # the instantiated object will have the correct email it was created with.
    assert newUser.get_email() == "example1@gmail.com"

def test_instantiate_user_notemail():
    # notemail contains an int, not a string that represent an email.
    notemail = 1234
    # Cannot instantitate a new user object with a string.
    with pytest.raises(expected_exception=AttributeError):
        userManager(notemail)
