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
    flask_login.logout_user()
    flask.flash('Daten erfolgreich gelöscht.')
    return flask.redirect(flask.url_for('welcome.show_welcome'))
