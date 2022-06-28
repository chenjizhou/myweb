# -*- coding: utf-8 -*-
# @package helper.MailHelper
# This module contains functions to send mail

import os
import smtplib
from email.message import EmailMessage

from flask import current_app

from api.server import constants


##
# @param receiver           The receiver email address.
# @param digit_code         The digit code.
# @param valid_duration     The digit code's available duration / minutes.
#
# @result                   A boolean indicating if the message has been sent.
#
def send_email(receiver, digit_code, valid_duration):
    sender = 'me@sender.com'
    smtp_host = os.environ.get('SMTP_HOST', '127.0.0.1')

    msg = EmailMessage()
    msg.set_content('Hello, your code is %s, it is valid for %s minutes'.format(digit_code, valid_duration))
    msg['Subject'] = 'Register email verification'
    msg['From'] = sender
    msg['To'] = receiver

    try:
        smtp_obj = smtplib.SMTP()
        smtp_obj.connect(smtp_host, constants.SMTP_PORT)
        smtp_obj.send_message(msg)
        smtp_obj.quit()
        current_app.logger.info("Validation mail sent to {} using server {}".format(str(receiver), smtp_host))
        print("digit_code : %s" % digit_code)
        return True
    except smtplib.SMTPException as e:
        current_app.logger.exception("Error on sending mail to : %s" % str(receiver))
        print("Error: sending mail: {}".format(str(e)))
        return False
    except Exception as e:
        current_app.logger.exception(str(e))
        return False
