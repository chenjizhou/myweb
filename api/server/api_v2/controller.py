# -*- coding: utf-8 -*-
import datetime

from flask import Blueprint, current_app, jsonify, make_response, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError

from api import db
from api.server.models import User
from api.server.response_code import RET
from api.server.user.utils import confirm_token, generate_confirmation_token_and_send_email

api_blueprint = Blueprint('user_v2', __name__, )


@api_blueprint.route('/register', methods=['POST'])
def register_user():
    data = request.get_json("data")
    try:
        user = User(
                email=data.get('email'),
                password=data.get('password'),
        )
        user_found = User.query.filter_by(email=data.get('email')).first()
        if user_found:
            return jsonify(errno=RET.REQERR, errmsg="Email already used.")
        # register user into database
        db.session.add(user)
        db.session.commit()
        # send email confirmation
        result = generate_confirmation_token_and_send_email(user)
        if result == 1:
            user = User.query.filter_by(id=user.id).first()
            user.email_sent = True
            user.confirmed_on = datetime.datetime.now()
            db.session.commit()
            current_app.logger.info("send confirmation mail to %s, at %s".format(
                    user.email,
                    user.confirmed_on.strftime("%Y-%m-%d %H:%M:%S")
            ))
            return make_response('Successfully registered. go to /login to login your account. ', 200)
        else:
            current_app.logger.error("send confirmation mail occurred a problem to %s, at %s".format(
                    user.email,
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            return jsonify(errno=RET.THIRDERR, errmsg="Confirmation email occurred a problem.")
    except IntegrityError:
        db.session.rollback()
        jsonify(errno=RET.DATAERR, errmsg="Registration occurred a problem.")


@api_blueprint.route('/login', methods=['POST'])
def login_user():
    data = request.get_json("data")
    if not data or not data.get('email') or not data.get('password'):
        return make_response('could not verify', 401, {'Authentication': 'login required"'})

    user = User.query.filter_by(email=data["email"]).first()
    if user and user.is_password_correct(data["password"]):
        token = create_access_token(identity=user.public_id)
        return jsonify({'token': token})
    return make_response('could not verify', 401, {'Authentication': '"login required"'})


@api_blueprint.route('/confirm', methods=['POST'])
@jwt_required
def confirm_email():
    if request.method == 'POST':
        # verify jwt_token
        current_user = get_jwt_identity()
        if not current_user:
            return jsonify(errno=RET.SESSIONERR, errmsg="Anonymous user.")
        user = User.query.filter_by(public_id=current_user).first_or_404()
        if user.confirmed:
            return jsonify(errno=RET.REQERR, errmsg="User already confirmed.")
        data = request.get_json("data")
        result = confirm_token(user.id, data.get("digit_code"))
        if result:
            user.confirmed = True
            user.confirmed_on = datetime.datetime.now()
            db.session.add(user)
            db.session.commit()
            return jsonify(errno=RET.OK, errmsg="confirm successfully.")
        else:
            return jsonify(errno=RET.REQERR, errmsg="Confirmation unsuccessful.")


# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
@api_blueprint.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
