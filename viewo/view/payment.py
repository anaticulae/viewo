# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import flask

payment = flask.Blueprint('payment', __name__)  # pylint:disable=invalid-name


@payment.route('/payment', methods=['POST'])
def start_payment():
    return flask.render_template('public/payment.html', payed=True)
