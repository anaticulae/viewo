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

import viewo.api.users.utils.user
import viewo.user


@viewo.user.viewo_user.route('/account')
@flask_login.login_required
def show_account():
    return flask.render_template('private/account/index.html')


@viewo.user.viewo_user.route('/account/delete')
@flask_login.login_required
def delete_account_ask():
    return flask.render_template('private/account/delete.html')


@viewo.user.viewo_user.route('/account/delete', methods=['POST'])
@flask_login.login_required
def delete_account_execute():
    # TODO: ADD DELETE BEHAVIOR
    flask_login.logout_user()
    flask.flash('Daten erfolgreich gelöscht.')
    return flask.redirect(flask.url_for('welcome.show_welcome'))


@viewo.user.viewo_user.route('/account/change')
@flask_login.login_required
def account_change():
    current = user()
    email = current.email or ''
    rendered = flask.render_template(
        'private/account/change.html',
        user=current.userid,
        email=email,
    )
    return rendered


@viewo.user.viewo_user.route('/account/dialogs')
@flask_login.login_required
def dialogs_overview():
    rendered = flask.render_template('private/dialog/index.html')
    return rendered


def user():
    userid = flask_login.current_user.get_id()
    current = viewo.api.users.utils.user.user_fromid(userid)
    return current
