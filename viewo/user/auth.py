# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import flask
import flask.globals
import flask_login
import flask_wtf
import viewo_api
import viewo_api.user.data
import wtforms
import wtforms.validators

import viewo.user


@viewo.user.viewo_user.route('/login')
def show_login():
    return flask.render_template('private/login.html', form=LoginForm())


@viewo.user.viewo_user.route('/logout')
@flask_login.login_required
def show_logout():
    flask_login.logout_user()
    # remove public password
    viewo_api.password_public_set('')
    flask.flash('Logout erfolgreich.')
    return flask.redirect(flask.url_for('viewo_user.show_login'))


@viewo.user.viewo_user.route('/login', methods=['POST'])
def check_login():
    if flask_login.current_user.is_authenticated:
        # user is already logged in
        return flask.redirect(flask.url_for('documents.view_documents'))

    user = flask.request.form['user']
    password = flask.request.form['password']

    # verify
    if not viewo_api.password_verify(user, password):
        flask.flash('Benutzerdaten fehlerhaft.')
        # ask user again
        return flask.render_template(
            'private/login.html',
            form=LoginForm(user=user, password=password),
        )

    # login
    viewo_api.login(user, password, False)

    # forward to next page
    forward = flask.request.args.get('next')
    if forward is None:
        return flask.redirect(flask.url_for('documents.view_documents'))
    return flask.redirect(forward)


def open_user(user: str) -> 'viewo.user.FlaskUser':
    return viewo_api.user.data.FlaskUser(identifier=user)


def public_password():
    return flask.globals.session.get('password_raw', '')


class LoginForm(flask_wtf.FlaskForm):
    user = wtforms.StringField(
        'Benutzer:',
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min=8, max=64),
        ],
    )
    password = wtforms.PasswordField(
        'Passwort:',
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min=8, max=64),
        ],
    )
    submit = wtforms.SubmitField('Anmelden')

    def __init__(self, user='', password='', **kwargs):
        super().__init__(**kwargs)
        self.user.default = user
        self.password.default = password
