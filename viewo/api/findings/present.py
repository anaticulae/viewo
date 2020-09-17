# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import flask
import protocol

import viewo.api
import viewo.api.findings
import viewo.api.findings.utils


@viewo.api.valid_document
@viewo.api.findings.api_findings.route(
    '/documents/<string:documentid>/findings',
    methods=['GET'],
)
def findings(documentid):
    collected = viewo.api.findings.utils.all_findings(documentid)
    dumped = flask.jsonify({
        'findings': collected,
    })
    return dumped


@viewo.api.findings.api_findings.route(
    '/documents/<string:documentid>/findings/<string:findingid>',
    methods=['GET'],
)
@viewo.api.valid_document
def finding_get(documentid, findingid):
    collected = viewo.api.findings.utils.all_findings(documentid)
    selected = protocol.select_findings(collected, findingid)
    if not selected:
        return viewo.api.notfound(f'could not find: {findingid}')
    finding = selected[0]
    dumped = flask.jsonify({
        'finding': finding,
    })
    return dumped
