# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import flask
import flask_login
import utila
import viewo_api.user.data

import viewo.api.users.update

payment = flask.Blueprint('payment', __name__)  # pylint:disable=invalid-name

VALID_CHOICE = {1, 2, 3, 4}
INVALID_MESSAGE = 'Invalid Choice'


@payment.route('/payment', methods=['POST'])
def payment_ready():
    # TODO: ADD ERROR HANDLING FOR INVALID CHOICE ETC.
    userid = flask_login.current_user.get_id()
    if userid:
        try:
            choice = flask.request.form['choice']
            choice = utila.str2int(choice)
            assert choice in VALID_CHOICE
        except (ValueError, AssertionError):
            flask.flash(INVALID_MESSAGE)
            return flask.render_template('public/payment/index.html')
        viewo.api.users.update.user_pay(userid, choice)
    return flask.render_template('public/payment/done.html')


@payment.route('/payment', methods=['GET'])
def payment_overview():
    userid = flask_login.current_user.get_id()
    if userid is None:
        return flask.render_template('public/payment/index.html')
    user = viewo_api.user.data.user_fromid(userid)
    if not user or not user.payed:
        return flask.render_template('public/payment/index.html')
    return flask.render_template('public/payment/done.html')
