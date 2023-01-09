# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import flask
import utila

import viewo.cache
import viewo.config
import viewo.writing.content
import viewo.writing.reflinks

DOC_PATH = viewo.config.writing()

writing_ = flask.Blueprint('writing', __name__, static_folder=DOC_PATH)  # pylint:disable=C0103


@writing_.route('/writing', defaults={'selected': 'index.html'})
@writing_.route('/writing/<path:selected>')
@viewo.cache.memoize()
def view_writing(selected: str = None):
    source = os.path.join(DOC_PATH, selected)
    if not os.path.exists(source):
        errorpage = f'writing/{selected}'.lower()
        return flask.render_template('public/error.html', errorpage=errorpage)

    result = utila.file_read(source)

    result = viewo.writing.content.replace(result, source)
    result = viewo.writing.reflinks.replace(result)

    rendered = flask.render_template('public/writing.html', writing=result)
    rendered = fix_search(rendered)
    return rendered


HACK = """<script type="text/javascript">$('#fallback').hide();</script>"""


def fix_search(content: str) -> str:
    if HACK not in content:
        return content
    content = content.replace(HACK, '')
    content = content + HACK
    return content
