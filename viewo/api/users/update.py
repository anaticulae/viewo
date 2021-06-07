# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import flask
import viewo_api

import viewo.api.users
import viewo.api.users.data
import viewo.api.users.utils.password
import viewo.api.users.utils.user

PASSWORD_WRONG = 'WRONG PASSWORD'  # nosec
PASSWORD_INVALID = 'INVALID PASSWORD DEFINITION'  # nosec
PASSWORD_NEW_TOO_SHORT = 'NEW PASSWORD TOO SHORT'  # nosec
PASSWORD_NEW_TOO_LONG = 'NEW PASSWORD TOO LONG'  # nosec
PASSWORD_DOES_NOT_MATCH = 'NEW AND REPEAT DOES NOT MATCH'  # nosec
PASSWORD_UPDATED = 'updated'  # nosec


@viewo.api.users.api_users.route(
    '/users/<string:userid>',
    methods=['PUT'],
)
@viewo.api.valid_user
@viewo.api.login_required_api  # pylint:disable=R0911,R1260
def user_put(userid):
    # TODO: SECURE INPUT
    password = flask.request.form.get('password', None)
    user = viewo.api.users.utils.user.user_fromid(userid)
    try:
        if not viewo.api.users.data.verify_password(userid, password):
            return viewo_api.bad(PASSWORD_WRONG)
    except viewo.api.users.utils.password.PasswordError:
        # password does not match requirements
        return viewo_api.bad(PASSWORD_INVALID)

    email = flask.request.form.get('email', None)

    password_new = flask.request.form.get('password_new', None)
    password_new_repeat = flask.request.form.get('password_new_repeat', None)

    if not email and not password_new:
        return viewo_api.bad('nothing to update')

    if email is not None:
        # TODO: VALIDATE EMAIL
        user.email = email

    if password_new:
        try:
            viewo.api.users.utils.password.valid(password_new)
        except viewo.api.users.utils.password.PasswordTooShort:
            return viewo_api.bad(PASSWORD_NEW_TOO_SHORT)
        except viewo.api.users.utils.password.PasswordTooLong:
            return viewo_api.bad(PASSWORD_NEW_TOO_LONG)

    if password_new != password_new_repeat:
        return viewo_api.bad(PASSWORD_DOES_NOT_MATCH)

    if password_new:
        # hash password and update user
        hashed = viewo.api.users.utils.password.hashed(password_new)
        user.password = hashed

    if not viewo.api.users.utils.user.user_update(user):
        return viewo_api.bad('could not update user')
    return viewo_api.success(PASSWORD_UPDATED)


def user_pay(userid: str, choice: int):
    assert choice in (0, 1, 2, 3, 4), f'invalid choice: {choice}'
    userpath = viewo.api.users.data.userpath(userid)
    assert os.path.exists(userpath), f'invalid user path: {userpath}'
    user = viewo.api.users.data.load_user(userpath)
    user.payed = choice
    viewo.api.users.data.update_user(user)
