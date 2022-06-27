# -*- coding: utf-8 -*-
# project/user/views.py

import datetime
from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

from api.models import User
from api import db
from api.response_code import RET
from .forms import LoginForm, RegisterForm
from api.digit_code_token import generate_confirmation_token_and_send_email, confirm_token

user_blueprint = Blueprint('user', __name__, )


@user_blueprint.route('/hello', methods=['GET'])
def hello():
    return "hello world"


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(
                email=form.email.data,
                password=form.password.data,
                confirmed=False
        )
        # register user into database
        db.session.add(user)
        db.session.commit()

        # send email confirmation
        result = generate_confirmation_token_and_send_email(user)

        if result == 1:
            return jsonify(errno=RET.OK, errmsg="validation email send with success")
        else:
            return jsonify(errno=RET.THIRDERR, errmsg="send email error")


@user_blueprint.route('/confirm/<digit_code>')
@login_required
def confirm_email(digit_code):
    if current_user.confirmed:
        return jsonify(errno=RET.REQERR, errmsg="User already confirmed.")
    result = confirm_token(current_user.id, digit_code)
    user = User.query.filter_by(email=current_user.email).first_or_404()
    if result:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
    else:
        return jsonify(errno=RET.REQERR, errmsg="The digit code is invalid or has expired.")
    return jsonify(errno=RET.OK, errmsg="Account validated with success")


@user_blueprint.route('/resend')
@login_required
def resend_confirmation():
    result = generate_confirmation_token_and_send_email(current_user)
    if result == 1:
        return jsonify(errno=RET.OK, errmsg="validation email send with success")
    else:
        return jsonify(errno=RET.THIRDERR, errmsg="send email error")


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return jsonify(errno=RET.OK, errmsg="login with success")
        else:
            return jsonify(errno=RET.PWDERR, errmsg="user mail or password is incorrect")


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify(errno=RET.OK, errmsg="logout with success")
