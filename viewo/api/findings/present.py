# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import flask
import flask_login
import utila
import viewo_api

import viewo.api
import viewo.api.findings
import viewo.api.pageviews.utils
import viewo.api.utils
import viewo.api_.findings.compare
import viewo.api_.findings.loader
import viewo.api_.findings.update


@viewo.api.findings.api_findings.route(
    '/documents/<string(length=16):documentid>/findings',
    methods=['GET'],
)
@viewo.api.valid_document
@viewo.api.valid_pages
def findings(documentid):
    pages_selected = pages(documentid)
    user = flask_login.current_user
    payed = not user.is_authenticated or user.payed
    collected = viewo.api_.findings.data.frontend(documentid).findings(
        pages=pages_selected,
        status=None,
    )
    simple = viewo.api_.findings.loader.all_findings_raw(
        collected,
        documentid,
        pages=pages_selected,
        payed=payed,
    )
    dumped = flask.jsonify({
        'findings': simple,
    })
    return dumped


@viewo.api.findings.api_findings.route(
    '/documents/<string(length=16):documentid>/findings/<string:findingid>',
    methods=['GET'],
)
@viewo.api.valid_document
@viewo.api.valid_finding
def finding_get(documentid, findingid):
    finding = viewo.api_.findings.data.frontend(documentid)[findingid]
    simple = viewo.api_.findings.loader.finding_raw(finding, documentid)
    dumped = flask.jsonify({
        'finding': simple,
    })
    return dumped


@viewo.api.findings.api_findings.route(
    '/documents/<string(length=16):documentid>/findings/compare/<string(length=16):partnerid>',
    methods=['GET'],
)
@viewo.api.valid_partner
@viewo.api.valid_document
def compare(documentid, partnerid):
    raw = flask.request.args.get('operation', 'all').lower()
    operation = viewo.api_.findings.compare.comperator_fromraw(raw)
    if not operation:
        return viewo_api.bad(f'invalid operation: {raw}')
    # comparation
    compared = viewo.api_.findings.compare.compare(
        documentid,
        partnerid,
        operation=operation,
    )
    if compared is None:
        # one or both documents does not exists
        return viewo_api.notfound(f'invalid docs: {documentid}/{partnerid}')
    # convert answer
    simple = viewo.api_.findings.compare.compare_raw(compared)
    result = {
        'compared': {
            'compared': simple,
            'current': documentid,
            'partnerid': partnerid,
        }
    }
    result['compared']['uri'] = flask.url_for(
        'api_findings.compare',
        documentid=documentid,
        partnerid=partnerid,
        operation=raw,
    )
    dumped = flask.jsonify(result)
    return dumped


SKIP = {
    'active',
    'confidence',
}


@viewo.api.findings.api_findings.route(
    '/documents/<string(length=16):documentid>/fastfindings',
    methods=['GET'],
)
@viewo.api.valid_document
@viewo.api.valid_pages
def fast_findings(documentid):
    pages_selected = pages(documentid)
    collected = viewo.api_.findings.loader.fast_findings(
        documentid,
        pages=pages_selected,
    )
    if collected is None:
        return viewo_api.notfound(f'could not find: {documentid}')
    simple = utila.simplify(collected, removes=SKIP)
    dumped = flask.jsonify(simple)
    return dumped


def pages(documentid: str) -> tuple:
    raw = flask.request.args.get('pages', None)
    if raw is None:
        return None
    pagecount = viewo.api.pageviews.utils.pagecount(documentid)
    selected = utila.parse_pages(raw, pagecount=pagecount)
    return selected
