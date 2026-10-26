# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Wrapper to bypass configos enviromental variables to enable
multiprocessed tests."""

import os

import configos
import flask
import utilo


def appconfig():
    try:
        return flask.current_app.config
    except RuntimeError:
        import viewo.__main__  # pylint:disable=import-outside-toplevel
        try:
            app = viewo.__main__.app
        except AttributeError:
            app = viewo.app.create_app()
            viewo.__main__.app = app
        with app.app_context():
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


configos.todo = todo
configos.ready = ready
configos.share = common


def init():
    installs = [
        common(),
        todo(),
        ready(),
        users(),
        visitors(),
    ]
    for item in installs:
        utilo.debug(item)
        os.makedirs(item, exist_ok=True)
