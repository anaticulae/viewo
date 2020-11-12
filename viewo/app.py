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
from viewo.view.welcome import welcome


def create_application(config=None) -> flask.Flask:
    """Setup flask application

    1. Set template and static folder
    2. Configure application
    3. Setup global env
    4. Register blueprint for routing the user requests
    """
    # Flask determines template- and static-folder automatically.
    app_ = flask.Flask(__name__)

    app_.config['MAX_CONTENT_LENGTH'] = viewo.config.MAX_FILE_SIZE
    app_.secret_key = viewo.config.SECRET_KEY

    configure(app_, config)
    init_error_handler(app_)

    # view
    app_.register_blueprint(viewo_user)
    app_.register_blueprint(documents_)
    app_.register_blueprint(legal_)
    app_.register_blueprint(result_)
    app_.register_blueprint(waiting_)
    app_.register_blueprint(welcome)
    app_.register_blueprint(writing_)

    # data API
    app_.register_blueprint(api_documents, url_prefix=viewo.config.API_PREFIX)
    app_.register_blueprint(api_findings, url_prefix=viewo.config.API_PREFIX)
    app_.register_blueprint(api_pageviews, url_prefix=viewo.config.API_PREFIX)
    app_.register_blueprint(api_users, url_prefix=viewo.config.API_PREFIX)
    app_.register_blueprint(api_visitors, url_prefix=viewo.config.API_PREFIX)

    viewo.user.loginmanager.create_loginmanager(app_)

    # track every user request
    app_.before_request(viewo.tracking.before_each_request)

    return app_


def configure(app_, config):
    """Set environment for application. Decide between test environment and
    production environment

    Args:
        app_(Flask): application to configure, which holds config
        config(dict): vars to export as global environment
    """
    if config is None:
        # Production environment
        # load the instance config, if it exists
        common_, todo_, ready_ = configo.environment()
        app_.config['COMMON'] = common_
        app_.config['TODO'] = todo_
        app_.config['READY'] = ready_
    else:
        # Test environment
        # load the test config if passed in
        app_.config.update(config)


def init_error_handler(app: flask.Flask):  # pylint:disable=W0621
    """Add errorhandler for unresolved resources

    Args:
        app(Flask): app to add errorhandler
    """

    @app.errorhandler(404)
    def not_found(_):  # pylint:disable=W0612,W0613
        return flask.render_template('public/error.html', errorpage='Die Seite')
