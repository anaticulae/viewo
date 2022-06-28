# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import flask
import flask_login
import utila

import viewo.api
import viewo.api.documents
import viewo.api.pageviews
import viewo.api.pageviews.utils


@viewo.api.pageviews.api_pageviews.route(
    f'/documents/{viewo.api.documents.DOCUMENTID}/pageviews',
    methods=['GET'],
)
@viewo.api.valid_document
@viewo.api.valid_pages
def pageviews(documentid):
    pagerange, pages = paged()
    user = flask_login.current_user
    payed = not user.is_authenticated or user.payed
    html = viewo.api.pageviews.utils.load_html(
        documentid,
        pagerange,
        payed=payed,
    )
    simple = {
        'html': html,
        'pages': pages,
        'uri': flask.request.url,
    }
    dumped = flask.jsonify({
        'pageviews': simple,
    })
    return dumped


def paged():
    pages = flask.request.args.get('pages', None)
    if pages:
        pagerange = utila.parse_pages(pages)
    else:
        pagerange, pages = None, ':'
    return pagerange, pages
