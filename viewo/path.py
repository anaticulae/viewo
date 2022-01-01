# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Wrapper to bypass configo enviromental variables to enable
multiprocessed tests."""

import os

import configo
import flask
import utila


def appconfig():
    try:
        return flask.current_app.config
    except RuntimeError:
        import viewo.__main__  # pylint:disable=import-outside-toplevel
        with viewo.__main__.app.app_context():
            return flask.current_app.config


def common():
    return appconfig()['COMMON']


def todo():
    return appconfig()['TODO']


def ready():
    return appconfig()['READY']


def users():
    result = os.path.join(common(), 'users')
    os.makedirs(result, exist_ok=True)
    return result


def visitors():
    result = os.path.join(common(), 'visitors')
    os.makedirs(result, exist_ok=True)
    return result


configo.todo = todo
configo.ready = ready
configo.share = common


def init():
    installs = [
        common(),
        todo(),
        ready(),
        users(),
        visitors(),
    ]
    for item in installs:
        utila.debug(item)
        os.makedirs(item, exist_ok=True)
