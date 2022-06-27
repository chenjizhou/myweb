# coding=utf-8
from api import db
from datetime import datetime
from werkzeug.security import generate_password_hash


class BaseModel(object):
    """set create and update time in BaseModel"""
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())


class User(BaseModel, db.Model):
    """ user model """

    __tablename__ = 'mw_user'

    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    email_sent = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, email, password, confirmed, confirmed_on=None, email_sent=None):
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.registered_on = datetime.now()
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on
        self.email_sent = email_sent

    @property
    def password(self):
        """do not allow to read the password attribute"""
        raise AttributeError("not allow to read password")

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id