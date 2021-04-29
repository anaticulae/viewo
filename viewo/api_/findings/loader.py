# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import flask
import iamraw
import link
import protocol
import protocol.finding
import utila

import viewo.api.pageviews.utils
import viewo.result.json


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


def fast_findings(
        documentid: str,
        pages: tuple = None,
        status=iamraw.ProblemStatus.OPEN,
) -> iamraw.PageFindings:
    documentpath = link.document(documentid)
    if documentpath is None:
        return None
    optimizedpath = link.optimized(documentid, done=True)
    findings = protocol.load_grouped(optimizedpath, pages=pages)
    for page in findings:
        page.content = [
            finding.number
            for finding in page.content
            if finding.solution.status == status
        ]
    findings = [item for item in findings if item.content]
    findings = sorted(findings, key=lambda x: x.page)
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


SKIP = {
    'active',
    'confidence',
}


def all_findings_raw(
        content,
        documentid: str,
        pages: tuple = None,
        payed: bool = True,
):
    public = viewo.api.pageviews.utils.public(documentid)
    simple = utila.simplify(content, removes=SKIP)
    simple = add_finding_uri(simple, documentid)
    simple = remove_unpayed(simple) if not payed and not public else simple
    pagerange, uri = paged(documentid, pages)
    raw = {
        'pagefindings': simple,
        'pages': pagerange,
        'uri': uri,
    }
    return raw


def finding_raw(finding: iamraw.Finding, documentid: str) -> dict:
    simple = utila.simplify(finding, removes=SKIP)
    simple['uri'] = flask.url_for(
        'api_findings.finding_get',
        documentid=documentid,
        findingid=finding.number,
    )
    return simple


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


def convert_style_markup(findings: iamraw.PageFinding) -> iamraw.PageFinding:
    for finding in findings.content:
        finding.solution.description = viewo.result.json.message_replace(
            finding.solution.description)
    return findings
