# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import flask
import viewo_api.user.data

import viewo.api
import viewo.api.users
import viewo.config


@viewo.api.users.api_users.route(
    '/users/<string(length=16):userid>',
    methods=['GET'],
)
@viewo.api.valid_user
@viewo.api.login_required_api
def user_get(userid: str):
    user = viewo_api.user.data.userpublic_fromid(userid)
    simple = {
        'user': user,
        'uri': flask.url_for('api_users.user_get', userid=userid)
    }
    dumped = flask.jsonify(simple)
    return dumped


@viewo.api.users.api_users.route('users', methods=['GET'])
def users():
    userx = viewo_api.user.data.userlist_raw()
    simple = {
        'users': userx,
        'uri': flask.url_for('api_users.users'),
    }
    dumped = flask.jsonify({
        'users': simple,
    })
    return dumped
