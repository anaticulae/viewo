# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import flask
import flask_login

import viewo.api.users.data
import viewo.user


@viewo.user.viewo_user.route('/login')
def show_login():
    return flask.render_template('public/login.html')


@viewo.user.viewo_user.route('/logout')
@flask_login.login_required
def show_logout():
    flask_login.logout_user()
    flask.flash('Logout erfolgreich.')
    return flask.render_template('public/login.html')


@viewo.user.viewo_user.route('/login', methods=['POST'])
def check_login():
    if flask_login.current_user.is_authenticated:
        # user is already logged in
        return flask.redirect(flask.url_for('documents.view_documents'))

    user = flask.request.form['user']
    password = flask.request.form['password']

    # verify
    if not viewo.api.users.data.verify_password(user, password):
        flask.flash('Benutzerdaten fehlerhaft.')
        # ask user again
        return flask.render_template(
            'public/login.html',
            user=user,
            password=password,
        )

    # login
    user = open_user(user)
    flask_login.login_user(user)
    flask.flash('Login erfolgreich.')

    # forward to next page
    forward = flask.request.args.get('next')
    if forward is None:
        return flask.redirect(flask.url_for('documents.view_documents'))
    return flask.redirect(forward)


def open_user(user: str) -> 'viewo.user.FlaskUser':
    return viewo.user.FlaskUser(identifier=user)
