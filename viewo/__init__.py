#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
import os
from os import environ
from os.path import join

from configo import environment
from configo import export
from flask import Blueprint
from flask import Flask
from flask import Response
from flask import abort
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from jinja2 import TemplateNotFound
from utila import error

from viewo.config import MAX_FILE_SIZE
from viewo.config import SECRET_KEY
from viewo.config import STATIC
from viewo.config import TEMPLATES
from viewo.documents import documents
from viewo.public import welcome
from viewo.result import result_
from viewo.upload import upload_

__version__ = '0.4.7'


def create_application(config=None) -> Flask:
    """Setup flask application

    1. Set template and static folder
    2. Configure application
    3. Setup global env
    4. Register blueprint for routing the user requests
    """
    # Flask determines template- and static-folder automatically.
    app_ = Flask(__name__)

    app_.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE
    app_.secret_key = SECRET_KEY

    configure(app_, config)
    init_error_handler(app_)

    app_.register_blueprint(documents)
    app_.register_blueprint(upload_)
    app_.register_blueprint(result_)
    app_.register_blueprint(welcome)

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
        common, todo, ready = environment()
        app_.config['COMMON'] = common
        app_.config['TODO'] = todo
        app_.config['READY'] = ready
    else:
        # Test environment
        # load the test config if passed in
        app_.config.update(config)
        try:
            export(config['COMMON'], config['TODO'], config['READY'])
        except KeyError:
            export('', '', '')


def init_error_handler(app: Flask):
    """Add errorhandler for unresolved resources

    Args:
        app(Flask): app to add errorhandler
    """

    @app.errorhandler(404)
    def not_found(_):
        return render_template('public/error.html', errorpage='Die Seite')


app = create_application()
