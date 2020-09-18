# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import flask

import viewo.api
import viewo.api.pages
import viewo.api.pages.utils


@viewo.api.pages.api_pages.route(
    '/documents/<string:documentid>/pages',
    methods=['GET'],
)
@viewo.api.valid_document
def pages(documentid):
    simple = {'html': viewo.api.pages.utils.load_html(documentid)}
    simple['uri'] = flask.url_for('api_pages.pages', documentid=documentid)

    dumped = flask.jsonify({
        'pages': simple,
    })
    return dumped
