# -*- coding: utf-8 -*-
import os

import pytest
from dotenv import load_dotenv
from sqlalchemy_utils import database_exists, create_database, drop_database
from api import create_app, db
from api.server.models import User

basedir = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(basedir, ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


@pytest.fixture(scope='module')
def new_user():
    user = User('hello@gmail.com', 'HereIsTheP@ssword')
    return user


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    if database_exists(flask_app.config["SQLALCHEMY_DATABASE_URI"]):
        drop_database(flask_app.config["SQLALCHEMY_DATABASE_URI"])

    create_database(flask_app.config["SQLALCHEMY_DATABASE_URI"])

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            # Create the database and the database table
            db.create_all()

            # Insert user data
            user1 = User(email='hellotest@gmail.com', password='HereIsTheP@ssword')
            user2 = User(email='hello@gmail.com', password='HereIsTheP@ssword')
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()

            yield testing_client  # this is where the testing happens!

    #db.drop_all()


@pytest.fixture(scope='function')
def login_default_user(test_client):
    test_client.post('/login',
                     data=dict(email='hello@gmail.com', password='HereIsTheP@ssword'),
                     follow_redirects=True)

    yield  # this is where the testing happens!

    test_client.get('/logout', follow_redirects=True)
