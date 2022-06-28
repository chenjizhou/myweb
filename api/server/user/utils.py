# -*- coding: utf-8 -*-
import os
import random

import redis
from flask import current_app, jsonify, url_for

from api.server import constants
from api.server.help.MailHelper import send_email
from api.server.response_code import RET
from api.server.config import config_map


def generate_confirmation_token_and_send_email(user):
    # generate 4 digits code
    email_digit_code = "%04d" % random.randint(0, 9999)
    email_digit_code_prefix = os.getenv("EMAIL_DIGIT_CODE_PREFIX") if \
        os.getenv("EMAIL_DIGIT_CODE_PREFIX") is not None else "email_digit_code_"

    # todo check why redis_store is None during test integration
    from api import redis_store
    if not redis_store:
        env = os.getenv("ENVIRONMENT") if os.getenv("ENVIRONMENT") is not None else "develop"
        config_class = config_map.get(env)
        redis_store = redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT)

    try:
        # store the email_digit_code into redis
        redis_store.setex(email_digit_code_prefix + user.get_id(), constants.EMAIL_DIGIT_CODE_REDIS_EXPIRES, email_digit_code)
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
