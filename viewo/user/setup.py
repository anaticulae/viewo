# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import flask_login

import viewo.user


def create_loginmanager(app):
    loginmanager = flask_login.LoginManager()
    loginmanager.login_view = 'viewo_user.show_login'
    loginmanager.init_app(app)

    loginmanager._user_callback = load_user  # pylint:disable=W0212


def load_user(userid):
    return viewo.user.FlaskUser(identifier=userid)
