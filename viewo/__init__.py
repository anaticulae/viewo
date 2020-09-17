#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import os

import configo
import flask

import viewo.__patch__
import viewo.config
from viewo.api.documents import *
from viewo.api.findings import *
from viewo.api.public import welcome
from viewo.api.result import result_
from viewo.api.upload import upload_
from viewo.api.waiting import waiting_
from viewo.api.writing import writing_
from viewo.view.documents import documents_

__version__ = '0.20.3'

API_PREFIX = '/api/v0'


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
    app_.register_blueprint(documents_)
    app_.register_blueprint(upload_)
    app_.register_blueprint(result_)
    app_.register_blueprint(welcome)
    app_.register_blueprint(waiting_)
    app_.register_blueprint(writing_)

    # data API
    app_.register_blueprint(api_documents, url_prefix=API_PREFIX)
    app_.register_blueprint(api_findings, url_prefix=API_PREFIX)

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
        common, todo, ready = configo.environment()
        app_.config['COMMON'] = common
        app_.config['TODO'] = todo
        app_.config['READY'] = ready
    else:
        # Test environment
        # load the test config if passed in
        app_.config.update(config)
        try:
            configo.export(config['COMMON'], config['TODO'], config['READY'])
        except KeyError:
            configo.export('', '', '')


def init_error_handler(app: flask.Flask):  # pylint:disable=W0621
    """Add errorhandler for unresolved resources

    Args:
        app(Flask): app to add errorhandler
    """

    @app.errorhandler(404)
    def not_found(_):  # pylint:disable=W0612,W0613
        return flask.render_template('public/error.html', errorpage='Die Seite')


app = create_application()  # pylint:disable=C0103
