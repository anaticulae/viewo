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
import utila

import viewo.api.users.data
import viewo.api.users.update

payment = flask.Blueprint('payment', __name__)  # pylint:disable=invalid-name


@payment.route('/payment', methods=['POST'])
def payment_ready():
    # TODO: ADD ERROR HANDLING FOR INVALID CHOICE ETC.
    userid = flask_login.current_user.get_id()
    if userid:
        choice = flask.request.form['choice']
        # TODO: ADD ERROR HANDLER
        choice = utila.str2int(choice)
        viewo.api.users.update.user_pay(userid, choice)
    return flask.render_template('public/payment/done.html')


@payment.route('/payment', methods=['GET'])
@flask_login.login_required
def payment_overview():
    userid = flask_login.current_user.get_id()
    if userid is None:
        return flask.render_template('public/payment/index.html')
    user = viewo.api.users.data.user_fromid(userid)
    if not user or not user.payed:
        return flask.render_template('public/payment/index.html')
    return flask.render_template('public/payment/done.html')
