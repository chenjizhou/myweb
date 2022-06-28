"""
This file (test_models.py) contains the unit tests for the models.py file.
"""
from api.server.models import User
import pytest


def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, password_hashed, authenticated, and active fields are defined correctly
    """
    user = User('helloworld@gmail.com', 'ThisIsAPassword')
    assert user.email == 'helloworld@gmail.com'
    assert user.password_hash != 'ThisIsAPassword'
    assert not user.confirmed
    assert not user.email_sent
    assert user.__repr__() == '<User: helloworld@gmail.com>'
    assert user.is_authenticated
    assert user.is_active
    assert not user.is_anonymous


def test_new_user_with_fixture(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email and password_hashed fields are defined correctly
    """
    assert new_user.email == 'hello@gmail.com'
    assert new_user.password_hash != 'HereIsTheP@ssword'


def test_setting_password(new_user):
    """
    GIVEN an existing User
    WHEN the password for the user is set
    THEN check the password is stored correctly and not as plaintext
    """

    with pytest.raises(AttributeError) as exc_info:
        raise Exception(new_user.password)
    assert exc_info.value.args[0] == 'not allow to read password'


def test_user_id(new_user):
    """
    GIVEN an existing User
    WHEN the ID of the user is defined to a value
    THEN check the user ID returns a string (and not an integer) as needed by Flask-WTF
    """
    new_user.id = 17
    assert isinstance(new_user.get_id(), str)
    assert not isinstance(new_user.get_id(), int)
    assert new_user.get_id() == '17'

