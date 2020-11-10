# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import flask

import viewo.api.users
import viewo.api.users.utils.password
import viewo.api.users.utils.user


@viewo.api.users.api_users.route(
    '/users/<string:userid>',
    methods=['PUT'],
)
@viewo.api.valid_user
def user_put(userid):
    # TODO: SECURE INPUT
    email = flask.request.form.get('email', None)
    password = flask.request.form.get('password', None)

    if email is None and password is None:
        return viewo.api.bad(f'could not update email or password')

    user = viewo.api.users.utils.user.user_fromid(userid)
    if email is not None:
        # TODO: VALIDATE EMAIL
        user.email = email
    if password is not None:
        try:
            viewo.api.users.utils.password.valid(password)
        except viewo.api.users.utils.password.PasswordTooLong:
            return viewo.api.bad('password too long')
        except viewo.api.users.utils.password.PasswordTooShort:
            return viewo.api.bad('password too short')
        user.password = password

    if not viewo.api.users.utils.user.user_update(user):
        return viewo.api.bad('could not update user')
    return viewo.api.success('updated')
