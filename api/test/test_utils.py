# -*- coding: utf-8 -*-

from api.server.models import User
from api.server.user.utils import generate_confirmation_token_and_send_email


def test_generate_confirmation_token_and_send_email(test_client):

    user = User.query.filter_by(email="hello@gmail.com").first()
    res = generate_confirmation_token_and_send_email(user)

    assert res
