# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import flask
import iamraw
import viewo_api

import viewo.api
import viewo.api.documents
import viewo.api.findings
import viewo.api_.findings.data
import viewo.api_.findings.update
import viewo.result.update


@viewo.api.findings.api_findings.route(
    f'/documents/{viewo.api.documents.DOCUMENTID}/findings/<string:findingid>',
    methods=['PUT'],
)
@viewo.api.valid_document
@viewo.api.valid_finding
def finding_put(documentid, findingid):
    status = flask.request.form.get('status', None)
    try:
        status = int(status)
    except ValueError:
        return viewo_api.bad(f'invalid status: {status}')
    try:
        # TODO: CHANGE <string:...?
        findingid = int(findingid)
    except ValueError:
        return viewo_api.bad(f'invalid findingid: {findingid}')
    if status not in (0, 1, 2, 3, 4):
        return viewo_api.bad(f'invalid status: {status}')
    status: iamraw.ProblemStatus = viewo.result.update.problem_fromint(status)
    if not viewo.api_.findings.data.frontend(documentid).update_status(
            findingid,
            status,
    ):
        return viewo_api.bad(f'could not update finding: {findingid} {status}')
    return viewo_api.success('updated')
