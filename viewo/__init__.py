#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
import os
from os import environ
from os.path import join

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
from utila import logging_error
from werkzeug.utils import secure_filename

from viewo.config import MAX_FILE_SIZE
from viewo.config import SECRET_KEY
from viewo.config import STATIC
from viewo.config import TEMPLATES
from viewo.config import environment
from viewo.public import welcome
from viewo.upload import upload

__version__ = '0.0.0'


def create_application(config=None) -> Flask:
    # TODO: viewo.viewo?
    app_ = Flask('viewo.viewo', template_folder=TEMPLATES, static_folder=STATIC)
    app_.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE
    app_.secret_key = SECRET_KEY

    if config is None:
        # load the instance config, if it exists, when not testing
        todo, ready = environment()
        app_.config['TODO'] = todo
        app_.config['READY'] = ready
    else:
        # load the test config if passed in
        app_.config.update(config)

    # # Working folder for pdf analyzing
    # app_.config['TODO'] = todo
    # app_.config['READY'] = ready

    app_.register_blueprint(upload)
    app_.register_blueprint(welcome)
    return app_


app = create_application()
