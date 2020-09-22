# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import flask

agb_ = flask.Blueprint('agb', __name__)  # pylint:disable=C0103


@agb_.route('/agb', methods=['GET'])
def view():
    return flask.render_template('public/agb.html')
