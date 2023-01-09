# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import flask
import flask_login
import utila
import viewo_api.user.data

import viewo.api.users.update
import viewo.config

payment = flask.Blueprint('payment', __name__)  # pylint:disable=invalid-name

VALID_CHOICE = {1, 2, 3, 4}
INVALID_MESSAGE = 'Invalid Choice'
NO_PRODUCT_CHOICE = 'Kein Produkt ausgewählt'


@payment.route('/payment', methods=['POST'])
def payment_ready():
    if not viewo.config.PAYMENT:
        # TODO: REFACTOR INTO DECORATOR?
        return 'payment system inactive.', 400
    # TODO: ADD ERROR HANDLING FOR INVALID CHOICE ETC.
    userid = flask_login.current_user.get_id()
    if userid:
        choice = flask.request.form.get('choice', None)
        if choice is None:
            flask.flash(NO_PRODUCT_CHOICE)
            return flask.render_template('public/payment/index.html')
        try:
            choice = utila.str2int(choice)
            assert choice in VALID_CHOICE
        except (ValueError, AssertionError):
            flask.flash(INVALID_MESSAGE)
            return flask.render_template('public/payment/index.html')
        viewo.api.users.update.user_pay(userid, choice)
    return flask.render_template('public/payment/done.html')


@payment.route('/payment', methods=['GET'])
def payment_overview():
    if not viewo.config.PAYMENT:
        # TODO: REFACTOR INTO DECORATOR?
        flask.flash('Bezahlsystem ist nicht aktiv.')
        return flask.redirect(flask.url_for('welcome.show_welcome'))
    userid = flask_login.current_user.get_id()
    if userid is None:
        return flask.render_template('public/payment/index.html')
    user = viewo_api.user.data.user_fromid(userid)
    if not user or not user.payed:
        return flask.render_template('public/payment/index.html')
    return flask.render_template('public/payment/done.html')
