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
    '/documents/<string:documentid>/findings/<string:findingid>',
    methods=['PUT'],
)
@viewo.api.valid_document
@viewo.api.valid_finding
def finding_put(documentid, findingid):
    status = flask.request.form.get('status', None)
    try:
        status = int(status)
    except ValueError:
        return viewo.api.bad(f'invalid status: {status}')
    if status not in (0, 1, 2, 3, 4):
        return viewo.api.bad(f'invalid status: {status}')
    if not viewo.api.findings.utils.update_finding_status(
            documentid,
            findingid,
            status,
    ):
        return viewo.api.bad(f'could not update')
    return viewo.api.success('updated')
