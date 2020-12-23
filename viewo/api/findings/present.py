# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import flask
import flask_login
import utila

import viewo.api
import viewo.api.findings
import viewo.api.findings.utils
import viewo.api.pageviews.utils
import viewo.api.utils


@viewo.api.findings.api_findings.route(
    '/documents/<string(length=16):documentid>/findings',
    methods=['GET'],
)
@viewo.api.valid_document
@viewo.api.valid_pages
def findings(documentid):
    pages_selected = pages(documentid)
    collected = viewo.api.findings.utils.all_findings(
        documentid,
        pages=pages_selected,
    )
    if collected is None:
        return viewo.api.notfound(f'could not find: {documentid}')
    user = flask_login.current_user
    payed = not user.is_authenticated or user.payed
    simple = viewo.api.findings.utils.all_findings_raw(
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
    finding = viewo.api.findings.utils.load_finding(documentid, findingid)
    simple = viewo.api.findings.utils.finding_raw(finding, documentid)
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
    operation_raw = flask.request.args.get('operation', 'all').lower()
    try:
        operation = viewo.api.findings.utils.Comperator[operation_raw.upper()]
    except KeyError:
        return viewo.api.bad(f'invalid operation: {operation_raw}')
    # comparation
    compared = viewo.api.findings.utils.compare(
        documentid,
        partnerid,
        operation=operation,
    )
    # convert answer
    simple = viewo.api.findings.utils.compare_raw(compared)
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
        operation=operation_raw,
    )
    dumped = flask.jsonify(result)
    return dumped


def pages(documentid: str) -> tuple:
    raw = flask.request.args.get('pages', None)
    if raw is None:
        return None
    pagecount = viewo.api.pageviews.utils.pagecount(documentid)
    selected = utila.parse_pages(raw, pagecount=pagecount)
    return selected
