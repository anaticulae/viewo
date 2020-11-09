# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import flask
import utila

import viewo.api
import viewo.api.pages
import viewo.api.pages.utils


@viewo.api.pages.api_pages.route(
    '/documents/<string(length=16):documentid>/pages',
    methods=['GET'],
)
@viewo.api.valid_document
@viewo.api.valid_pages
def pages(documentid):
    pages_raw = flask.request.args.get('range', None)
    if pages_raw:
        pagerange = utila.parse_pages(pages_raw)
    else:
        pagerange, pages_raw = None, ':'

    html = viewo.api.pages.utils.load_html(documentid, pagerange)
    uri = flask.url_for('api_pages.pages', documentid=documentid)
    if pagerange is not None:
        uri = flask.url_for(
            'api_pages.pages',
            documentid=documentid,
            range=pages_raw,
        )
    simple = {
        'html': html,
        'pages': pages_raw,
        'uri': uri,
    }
    dumped = flask.jsonify({
        'pages': simple,
    })
    return dumped
