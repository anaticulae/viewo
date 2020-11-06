# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import flask

viewo_user = flask.Blueprint('viewo_user', __name__)  # pylint:disable=invalid-name

__all__ = ['viewo_user', 'account', 'auth', 'loginmanager', 'register']
