# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import flask
import iamraw
import link
import protocol.finding
import utila

import viewo.api.utils


def all_findings(documentid: str):
    documentpath = link.document(documentid)  # pylint:disable=E1101
    if documentpath is None:
        return None
    findings = protocol.findings_from_path(documentpath)
    return findings


def load_finding(documentid, findingid):
    # TODO: EXPERIMENTAL
    findingid = str(findingid)
    documentpath = link.document(documentid)  # pylint:disable=E1101
    for _, findings in protocol.finding.iter_findings(documentpath):
        for finding in findings:
            if str(finding.number) == findingid:
                return finding
    return None


def all_findings_raw(pages, documentid: str):
    simple = viewo.api.utils.simple_recursive(pages)
    for page in simple:
        for finding in page['content']:
            finding['uri'] = flask.url_for(
                'api_findings.finding_get',
                documentid=documentid,
                findingid=finding['number'],
            )
    raw = {
        'pages': simple,
        'uri': flask.url_for('api_findings.findings', documentid=documentid),
    }
    return raw


def finding_raw(finding: iamraw.Finding, documentid: str) -> dict:
    simple = viewo.api.utils.simple_recursive(finding)
    simple['uri'] = flask.url_for(
        'api_findings.finding_get',
        documentid=documentid,
        findingid=finding.number,
    )
    return simple


def update_finding_status(documentid: str, findingid: int, status: int):
    source = link.document(documentid)  # pylint:disable=E1101
    status = viewo.result.update.problem_fromint(status)
    before = protocol.finding_status(source, findingid)
    if not protocol.finding_status_update(source, findingid, status):
        utila.error(f'could not update: {findingid} status: {status}')
        return False
    viewo.result.update.update_bookkeeping(source, status, before)
    return True
