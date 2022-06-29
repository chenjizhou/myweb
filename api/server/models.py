# coding=utf-8
from api import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import uuid


class BaseModel(object):
    """set create and update time in BaseModel"""
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())


class User(BaseModel, db.Model):
    """ user model """

    __tablename__ = 'mw_user'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(255))
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    email_sent = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, email, password, confirmed=False, confirmed_on=None, email_sent=None):
        self.email = email
        self.public_id = str(uuid.uuid4())
        self.password_hash = generate_password_hash(password)
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on
        self.email_sent = email_sent

    @property
    def password(self):
        """do not allow to read the password attribute"""
        raise AttributeError("not allow to read password")

    def is_password_correct(self, password_plaintext: str):
        return check_password_hash(self.password_hash, password_plaintext)

    @property
    def is_authenticated(self):
        """Return True if the user has been successfully registered."""
        return True

    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True

    @property
    def is_anonymous(self):
        """Always False, as anonymous users aren't supported."""
        return False

    def get_id(self):
        """Return the user ID as a unicode string (`str`)."""
        return str(self.id)

    def __repr__(self):
        return '<User: {0}>'.format(self.email)
