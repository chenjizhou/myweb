# -*- coding: utf-8 -*-
import random
from api import redis_store
from api.server import constants
from api.server.response_code import RET
from flask import current_app, jsonify, url_for
from api.server.help.MailHelper import send_email


def generate_confirmation_token_and_send_email(user):
    # generate 4 digits code
    email_digit_code = "%04d" % random.randint(0, 9999)
    try:
        # store the email_digit_code into redis
        redis_store.setex("email_digit_code_%s" % user.id, constants.EMAIL_DIGIT_CODE_REDIS_EXPIRES, email_digit_code)
    except Exception as e:
        # log the error
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="generate email digit code error")
    try:
        # send email_digit_code by email
        result = send_email(user.email, email_digit_code, int(constants.EMAIL_DIGIT_CODE_REDIS_EXPIRES / 60))
    except Exception as e:
        # log the error
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="SMTP error")

    return result


def confirm_token(user_id, digit_code):
    try:
        # get the email_digit_code into redis
        real_digit_code = redis_store.get("email_digit_code_%s" % user_id)
    except Exception as e:
        # log the error
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="get email digit code error")
    if int(real_digit_code) == int(digit_code):
        return True
    else:
        return False


def generate_url(endpoint, token):
    return url_for(endpoint, token=token, _external=True)
