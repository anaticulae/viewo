# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import flask
import iamraw
import link
import utila

import viewo.api.pageviews.utils
import viewo.api_.findings.data


def fast_findings(
    documentid: str,
    pages: tuple = None,
    status=iamraw.ProblemStatus.OPEN,
) -> iamraw.PageFindings:
    documentpath = link.document(documentid)
    if documentpath is None:
        return None
    frontend = viewo.api_.findings.data.frontend(documentid)
    result = frontend.fastfindings(
        pages=pages,
        status=status,
    )
    return result


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
    simple = findingids_tostr(simple)
    pagerange, uri = paged(documentid, pages)
    raw = {
        'pagefindings': simple,
        'pages': pagerange,
        'uri': uri,
    }
    return raw


def finding_raw(finding: iamraw.Finding, documentid: str) -> dict:
    simple = utila.simplify(finding, removes=SKIP)
    simple = findingid_tostr(simple)
    simple['uri'] = flask.url_for(
        'api_findings.finding_get',
        documentid=documentid,
        findingid=finding.number,
    )
    return simple


def findingid_tostr(finding) -> dict:
    # convert finding number to string to handle larger integers in
    # json(max:2^35)
    finding['number'] = str(finding['number'])
    return finding


def findingids_tostr(pages):
    for page in pages:
        for finding in page['content']:
            findingid_tostr(finding)
    return pages


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
