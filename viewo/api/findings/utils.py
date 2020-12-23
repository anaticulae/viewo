# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import flask
import iamraw
import link
import protocol.finding
import utila

import viewo.api.pageviews.utils
import viewo.api.utils
import viewo.result.json
import viewo.result.update


def all_findings(documentid: str, pages: tuple = None):
    documentpath = link.document(documentid)
    if documentpath is None:
        return None
    optimizedpath = link.optimized(documentid, done=True)
    if os.path.exists(optimizedpath):
        findings = protocol.load_grouped(optimizedpath, pages=pages)
    else:
        utila.error('using outdated finding collector!')
        findings = protocol.findings_from_path(documentpath)
        # skip non selected findings
        findings = [
            finding for finding in findings
            if not utila.should_skip(finding.page, pages)
        ]
    findings = [convert_style_markup(page) for page in findings]
    return findings


def load_finding(documentid, findingid):
    # TODO: EXPERIMENTAL
    findingid = str(findingid)
    documentpath = link.document(documentid)
    for _, findings in protocol.finding.iter_findings(documentpath):
        for finding in findings:
            if str(finding.number) == findingid:
                return finding
    return None


def all_findings_raw(
        content,
        documentid: str,
        pages: tuple = None,
        payed: bool = True,
):
    simple = viewo.api.utils.simple_recursive(content)
    simple = add_finding_uri(simple, documentid)
    simple = remove_unpayed(simple) if not payed else simple
    pagerange, uri = paged(documentid, pages)
    raw = {
        'pagefindings': simple,
        'pages': pagerange,
        'uri': uri,
    }
    return raw


def remove_unpayed(simple):
    for page in simple:
        allowed = viewo.api.pageviews.utils.free_view(page['page'])
        if allowed:
            continue
        for finding in page['content']:
            finding['solution']['title'] = 'Vollzugriff erforderlich'
            finding['solution']['description'] = 'Vollzugriff erforderlich'
    return simple


def add_finding_uri(simple, documentid):
    for page in simple:
        for finding in page['content']:
            finding['uri'] = flask.url_for(
                'api_findings.finding_get',
                documentid=documentid,
                findingid=finding['number'],
            )
    return simple


def paged(documentid, pages):
    uri = flask.url_for('api_findings.findings', documentid=documentid)
    pagerange = ':'
    if pages is not None:
        pages = utila.simplify_pages(pages)
        uri = flask.url_for(
            'api_findings.findings',
            documentid=documentid,
            pages=pages,
        )
        pagerange = pages
    return pagerange, uri


def finding_raw(finding: iamraw.Finding, documentid: str) -> dict:
    simple = viewo.api.utils.simple_recursive(finding)
    simple['uri'] = flask.url_for(
        'api_findings.finding_get',
        documentid=documentid,
        findingid=finding.number,
    )
    return simple


def update_finding_status(documentid: str, findingid: int, status: int):
    source = link.document(documentid)
    status = viewo.result.update.problem_fromint(status)
    before = protocol.finding_status(source, findingid)
    if not protocol.finding_status_update(source, findingid, status):
        utila.error(f'could not update: {findingid} status: {status}')
        return False
    viewo.result.update.update_bookkeeping(source, status, before)
    return True


def convert_style_markup(findings: iamraw.PageFinding) -> iamraw.PageFinding:
    for finding in findings.content:
        finding.solution.description = viewo.result.json.message_replace(
            finding.solution.description)
    return findings
