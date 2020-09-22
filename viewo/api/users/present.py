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
import viewo.api.users.utils
import viewo.config


@viewo.api.users.api_users.route('users', methods=['GET'])
def users():
    users_ = viewo.api.users.utils.users()
    simple = {
        'users': users_,
        'uri': flask.url_for('api_users.users'),
    }
    dumped = flask.jsonify({
        'users': simple,
    })
    return dumped
