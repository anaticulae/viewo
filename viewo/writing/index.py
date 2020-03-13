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
import viewo.writing.content
import viewo.writing.reflinks

STATIC = os.path.join(viewo.config.writing(), '_static')

writing_ = flask.Blueprint('writing', __name__, static_folder=STATIC)  # pylint:disable=C0103


@writing_.route('/writing', defaults={'selected': 'index.html'})
@writing_.route('/writing/<path:selected>')
def view_result(selected: str = None):
    source = os.path.join(viewo.config.writing(), selected)
    if not os.path.exists(source):
        source = os.path.join(viewo.config.writing(), 'index.html')
    content = utila.file_read(source)

    content = viewo.writing.content.replace(content, source)

    content = viewo.writing.reflinks.replace(content)

    rendered = flask.render_template('public/writing.html', content=content)
    return rendered
