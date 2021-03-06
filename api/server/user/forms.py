# -*- coding: utf-8 -*-
# api/user/forms.py


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo

from api.server.models import User


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email(), Length(min=6, max=255)])
    password = PasswordField('password', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email(message=None), Length(min=6, max=255)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=6, max=255)])
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True


class ConfirmForm(FlaskForm):
    digit_code = StringField(
        'digit_code',
        validators=[DataRequired(), Length(min=4, max=4)]
    )

