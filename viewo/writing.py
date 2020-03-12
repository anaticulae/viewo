# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import flask
import utila

import viewo.config

STATIC = os.path.join(viewo.config.writing(), '_static')

writing_ = flask.Blueprint('writing', __name__, static_folder=STATIC)  # pylint:disable=C0103

CSS = f'<link href="/_static/wclub.css" rel="stylesheet" type="text/css">'
JS = """<script type="text/javascript" src="/_static/jquery.js"></script>
<script type="text/javascript" id="documentation_options" data-url_root="./" src="_static/documentation_options.js"></script>
    <script type="text/javascript" src="_static/jquery.js"></script>
    <script type="text/javascript" src="_static/underscore.js"></script>
    <script type="text/javascript" src="_static/doctools.js"></script>
    <script type="text/javascript" src="_static/language_data.js"></script>
    <script type="text/javascript" src="_static/translations.js"></script>"""
# CSS = '<link href="{{ url_for(\'static\', filename=\'static/wclub.css\') }}" rel="stylesheet" type="text/css">'

# <img src="{{ url_for('static', filename='images/logo.jpg') }}" width="100%"


@writing_.route('/writing', defaults={'selected': 'index.html'})
@writing_.route('/writing/<path:selected>')
def view_result(selected: str = None):
    source = os.path.join(viewo.config.writing(), selected)
    if not os.path.exists(source):
        source = os.path.join(viewo.config.writing(), 'index.html')
    content = utila.file_read(source)

    # strip body
    content = viewo.config.content(content)

    if source == os.path.join(viewo.config.writing(), 'index.html'):
        # HACK: fix main links
        content = content.replace('action="search.html"', 'action="writing/search.html"') # yapf:disable
        content = content.replace('href="#', 'href="index.html#')
        content = content.replace('href="', 'href="writing/')

    content = f'{CSS}\n{JS}\n{content}'
    rendered = flask.render_template('public/writing.html', content=content)
    return rendered
    # return rendered
