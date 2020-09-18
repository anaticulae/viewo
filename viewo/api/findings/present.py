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
import viewo.api.findings
import viewo.api.findings.utils


@viewo.api.findings.api_findings.route(
    '/documents/<string:documentid>/findings',
    methods=['GET'],
)
@viewo.api.valid_document
def findings(documentid):
    collected = viewo.api.findings.utils.all_findings(documentid)
    if collected is None:
        return viewo.api.notfound(f'could not find: {documentid}')
    simple = viewo.api.findings.utils.all_findings_raw(collected, documentid)
    dumped = flask.jsonify({
        'findings': simple,
    })
    return dumped


@viewo.api.findings.api_findings.route(
    '/documents/<string:documentid>/findings/<string:findingid>',
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
