# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from flask import Blueprint
from flask import render_template
from jinja2 import TemplateNotFound

welcome = Blueprint('welcome', __name__)  # pylint:disable=invalid-name


@welcome.route('/', defaults={'page': 'home'})
@welcome.route('/<page>')
def show_welcome(page):
    """Route public pages which are visible without any permissions."""
    try:
        return render_template('public/%s.html' % page)
    except TemplateNotFound:
        return render_template('public/error.html', errorpage=page)
