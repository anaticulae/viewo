# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import flask
import flask_bootstrap

import viewo
import viewo.__patch__
import viewo.config
import viewo.path
import viewo.tracking
import viewo.user.loginmanager
from viewo.api.documents import *  # pylint:disable=wildcard-import
from viewo.api.findings import *  # pylint:disable=wildcard-import
from viewo.api.pageviews import *  # pylint:disable=wildcard-import
from viewo.api.result import result_
from viewo.api.users import *  # pylint:disable=wildcard-import
from viewo.api.visitors import *  # pylint:disable=wildcard-import
from viewo.api.waiting import waiting_
from viewo.api.writing import writing_
from viewo.user import *  # pylint:disable=wildcard-import
from viewo.view.documents import documents_
from viewo.view.legal import legal_
from viewo.view.payment import payment
from viewo.view.welcome import welcome


def create_application(config=None) -> flask.Flask:
    """Setup flask application

    1. Set template and static folder
    2. Configure application
    3. Setup global env
    4. Register blueprint for routing the user requests
    """
    # Flask determines template- and static-folder automatically.
    appi = flask.Flask(__name__)

    appi.config['MAX_CONTENT_LENGTH'] = viewo.config.MAX_FILE_SIZE
    appi.secret_key = viewo.config.SECRET_KEY

    appi.config.setdefault('BOOTSTRAP_SERVE_LOCAL', True)
    flask_bootstrap.Bootstrap(app=appi)

    configure(appi, config)
    init_error_handler(appi)

    # view
    appi.register_blueprint(viewo_user)
    appi.register_blueprint(documents_)
    appi.register_blueprint(legal_)
    appi.register_blueprint(result_)
    appi.register_blueprint(waiting_)
    appi.register_blueprint(welcome)
    appi.register_blueprint(writing_)
    appi.register_blueprint(payment)

    # data API
    appi.register_blueprint(api_documents, url_prefix=viewo.config.API_PREFIX)
    appi.register_blueprint(api_findings, url_prefix=viewo.config.API_PREFIX)
    appi.register_blueprint(api_pageviews, url_prefix=viewo.config.API_PREFIX)
    appi.register_blueprint(api_users, url_prefix=viewo.config.API_PREFIX)
    appi.register_blueprint(api_visitors, url_prefix=viewo.config.API_PREFIX)

    viewo.user.loginmanager.create_loginmanager(appi)

    # track every user request
    appi.before_request(viewo.tracking.before_each_request)

    return appi


def configure(appi, config):
    """Set environment for application. Decide between test environment and
    production environment

    Args:
        appi(Flask): application to configure, which holds config
        config(dict): vars to export as global environment
    """
    if config is None:
        # Production environment
        # load the instance config, if it exists
        common_, todo_, ready_ = configo.environment()
        appi.config['COMMON'] = common_
        appi.config['TODO'] = todo_
        appi.config['READY'] = ready_
    else:
        # Test environment
        # load the test config if passed in
        appi.config.update(config)


def init_error_handler(app: flask.Flask):  # pylint:disable=W0621
    """Add errorhandler for unresolved resources

    Args:
        app(Flask): app to add errorhandler
    """

    @app.errorhandler(404)
    def not_found(_):  # pylint:disable=W0612,W0613
        return flask.render_template('public/error.html', errorpage='Die Seite')
