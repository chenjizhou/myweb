# -*- coding: utf-8 -*-
"""
This file (test_user.py) contains the functional tests for the `user` blueprint.

These tests use GETs and POSTs to different URLs to check for the proper behavior
of the `user` blueprint.
"""
from api.server.user.utils import generate_confirmation_token_and_send_email
from api.server.models import User


def test_login_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Email' in response.data
    assert b'Password' in response.data


def test_valid_login_logout(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/login',
                                data=dict(email='hellotest@gmail.com', password='HereIsTheP@ssword'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Thanks for logging in, hellotest@gmail.com!' in response.data
    assert b'Logout' in response.data
    """
    GIVEN a Flask application configured for testing
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'You were logged out.' in response.data
    assert b'Logout' not in response.data
    assert b'login' in response.data
    assert b'register' in response.data


def test_invalid_login(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted to with invalid credentials (POST)
    THEN check an error message is returned to the user
    """
    response = test_client.post('/login',
                                data=dict(email='hellotest@gmail.com', password='NotCorrectPassword'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'ERROR! Incorrect login credentials.' in response.data
    assert b'Logout' not in response.data
    assert b'login' in response.data
    assert b'register' in response.data


def test_login_already_logged_in(test_client, login_default_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted to (POST) when the user is already logged in
    THEN check an error message is returned to the user
    """
    response = test_client.post('/login',
                                data=dict(email='hello@gmail.com', password='HereIsTheP@ssword'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Already logged in!  Redirecting to your User Profile page...' in response.data
    assert b'Logout' in response.data
    assert b'Login' not in response.data
    assert b'Register' not in response.data


def test_valid_registration(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' page is posted to (POST)
    THEN check the response is valid and the user is logged in
    """
    response = test_client.post('/',
                                data=dict(email='register.test@gmail.com',
                                          password='HereIsTheP@ssword',
                                          confirm='HereIsTheP@ssword'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'hello, register.test@gmail.com' in response.data
    assert b'Logout' in response.data
    assert b'Login' not in response.data
    assert b'Register' not in response.data

    """
    GIVEN a Flask application configured for testing
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200

    assert b'You were logged out.' in response.data
    assert b'Logout' not in response.data
    assert b'login' in response.data
    assert b'register' in response.data


def test_invalid_registration(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' page is posted to with invalid credentials (POST)
    THEN check an error message is returned to the user
    """
    response = test_client.post('/',
                                data=dict(email='register.test_invalid@gmail.com',
                                          password='HereIsTheP@ssword',
                                          confirm='HereIsThePassword'),   # Does NOT match!
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Thanks for registering, register.test_invalid@gmail.com!' not in response.data
    assert b'Passwords must match.' in response.data
    assert b'Logout' not in response.data
    assert b'login' in response.data
    assert b'register' in response.data


def test_duplicate_registration(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' page is posted to (POST) using an email address already registered
    THEN check an error message is returned to the user
    """
    # Register the new account
    test_client.post('/',
                     data=dict(email='register.test123@gmail.com',
                               password='HereIsTheP@ssword',
                               confirm='HereIsTheP@ssword'),
                     follow_redirects=True)
    # Try registering with the same email address
    response = test_client.post('/',
                                data=dict(email='register.test123@gmail.com',
                                          password='HereIsAnotherP@ssword',
                                          confirm='HereIsAnotherP@ssword'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Email already registered' in response.data
    assert b'Thanks for registering, register.test123@gmail.com!' not in response.data
