# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import flask


def success(message: str = 'completed', **args):
    result = flask.jsonify({
        'message': message,
        **args,
    })
    return result, 200


def notfound(message: str):
    result = flask.jsonify({
        'error': 'not found',
        'message': message,
    })
    return result, 404


def bad(message: str):
    result = flask.jsonify({
        'error': 'bad request',
        'message': message,
    })
    return result, 400


def internal(message: str):
    result = flask.jsonify({
        'error': 'internal',
        'message': message,
    })
    return result, 500
