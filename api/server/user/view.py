# -*- coding: utf-8 -*-
# project/user/views.py

import datetime
from flask import Blueprint, request, jsonify, render_template, flash, current_app, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError

from api.server.models import User
from api import db
from api.server.response_code import RET
from .forms import RegisterForm, ConfirmForm, LoginForm
from api.server.user.utils import generate_confirmation_token_and_send_email, confirm_token

user_blueprint = Blueprint('user', __name__, )


@user_blueprint.route('/', methods=['GET', 'POST'])
def home():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        try:
            user = User(
                email=form.email.data,
                password=form.password.data,
            )
            # register user into database
            db.session.add(user)
            db.session.commit()
            # send email confirmation
            result = generate_confirmation_token_and_send_email(user)
            login_user(user)
            if result == 1:
                user = User.query.filter_by(id=user.id).first()
                user.email_sent = True
                user.confirmed_on = datetime.datetime.now()
                db.session.commit()
                current_app.logger.info("send confirmation mail to %s, at %s".format(
                    user.email,
                    user.confirmed_on.strftime("%Y-%m-%d %H:%M:%S")
                ))
                flash('A confirmation email has sent to you.', 'success')
                return redirect(url_for('user.confirm_email'))
            else:
                current_app.logger.error("send confirmation mail occurred a problem to %s, at %s".format(
                    user.email,
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ))
                flash('Confirmation email occurred a problem.', 'danger')
        except IntegrityError:
            db.session.rollback()
            flash('Registration occurred a problem.', 'danger')

    users = User.query.all()
    return render_template('home.html', form=form, users=users)


@user_blueprint.route('/confirm/', methods=['GET', 'POST'])
@login_required
def confirm_email():
    form = ConfirmForm(request.form)
    if form.validate_on_submit():
        if current_user.confirmed:
            return jsonify(errno=RET.REQERR, errmsg="User already confirmed.")
        result = confirm_token(current_user.id, form.digit_code.data)
        user = User.query.filter_by(email=current_user.email).first_or_404()
        if result:
            user.confirmed = True
            user.confirmed_on = datetime.datetime.now()
            db.session.add(user)
            db.session.commit()
            flash('Your account has been confirmed', 'success')
            return redirect(url_for('user.confirm_success'))
        else:
            flash('The digit code is invalid or has expired.', 'danger')

    return render_template('confirmation.html', form=form, current_user=current_user)


@user_blueprint.route('/confirm_success/')
@login_required
def confirm_success():
    users = User.query.all()
    return render_template('congratulation.html', users=users, current_user=current_user)


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out.', 'success')
    return redirect(url_for('user.home'))


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # If the User is already logged in, don't allow them to try to log in again
    if current_user.is_authenticated:
        flash('Already logged in!  Redirecting to your User Profile page...', "warning")
        return redirect(url_for('user.profile'))

    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.is_password_correct(form.password.data):
                db.session.add(user)
                db.session.commit()
                login_user(user)
                flash('Thanks for logging in, {}!'.format(current_user.email), "info")
                return redirect(url_for('user.profile'))

        flash('ERROR! Incorrect login credentials.', "danger")
    return render_template('login.html', form=form)


@user_blueprint.route('/profile')
@login_required
def profile():
    return render_template('profile.html')
