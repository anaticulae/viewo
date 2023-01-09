# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import flask
import jinja2
import link

import viewo.api.documents.present
import viewo.cache
import viewo.optimize

welcome = flask.Blueprint('welcome', __name__)  # pylint:disable=invalid-name


@welcome.route('/<page>')
@viewo.cache.memoize()
def show_page(page):
    """Route public pages which are visible without any permissions."""
    try:
        return flask.render_template(f'public/{page}.html')
    except jinja2.TemplateNotFound:
        return flask.render_template('public/error.html', errorpage=page)


@welcome.route('/')
@viewo.cache.cached()
def show_welcome():
    public = viewo.api.documents.present.load_documents(
        owner=link.PUBLIC_OWNER,
        state=link.State.DONE,
    )
    rendered = flask.render_template('public/home.html', documents=public)
    return rendered
