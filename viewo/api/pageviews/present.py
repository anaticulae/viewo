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
import viewo.api.pageviews
import viewo.api.pageviews.utils


@viewo.api.pageviews.api_pageviews.route(
    '/documents/<string(length=16):documentid>/pageviews',
    methods=['GET'],
)
@viewo.api.valid_document
@viewo.api.valid_pages
def pageviews(documentid):
    pages_raw = flask.request.args.get('pages', None)
    if pages_raw:
        pagerange = utila.parse_pages(pages_raw)
    else:
        pagerange, pages_raw = None, ':'

    html = viewo.api.pageviews.utils.load_html(documentid, pagerange)
    uri = flask.url_for('api_pageviews.pageviews', documentid=documentid)
    if pagerange is not None:
        uri = flask.url_for(
            'api_pageviews.pageviews',
            documentid=documentid,
            pages=pages_raw,
        )
    simple = {
        'html': html,
        'pages': pages_raw,
        'uri': uri,
    }
    dumped = flask.jsonify({
        'pageviews': simple,
    })
    return dumped
