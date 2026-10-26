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
import qvlink
import utilo

import viewo.api.pageviews.utils
import viewo.api_.findings.data
import viewo.config
import viewo.result.loader.pagenumbers


def fast_findings(
    documentid: str,
    pages: tuple = None,
    status=iamraw.ProblemStatus.OPEN,
) -> iamraw.PageFindings:
    documentpath = qvlink.document(documentid)
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
    simple = utilo.simplify(content, removes=SKIP)
    simple = add_finding_uri(simple, documentid)
    simple = remove_unpayed(simple) if not payed and not public else simple
    simple = findingids_tostr(simple)
    simple = add_pagenumbers(simple, documentid)
    pagerange, uri = paged(documentid, pages)
    raw = {
        'pagefindings': simple,
        'pages': pagerange,
        'uri': uri,
    }
    return raw


def finding_raw(finding: iamraw.Finding, documentid: str) -> dict:
    simple = utilo.simplify(finding, removes=SKIP)
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
        allowed = viewo.api.pageviews.utils.free_view(
            page['page'],
            payment=viewo.config.PAYMENT,
        )
        if allowed:
            # if PAYMENT is disabled, all pages are allowed
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


def add_pagenumbers(simple, documentid):
    for pagefinding in simple:
        pagefinding['pdfpage'] = pagefinding['page']
        userpage = viewo.result.loader.pagenumbers.userpage(
            pdfpage=pagefinding['page'],
            documentid=documentid,
        )
        pagefinding['page'] = userpage
    return simple


def paged(documentid, pages):
    uri = flask.url_for('api_findings.findings', documentid=documentid)
    pagerange = ':'
    if pages is not None:
        pages = utilo.simplify_pages(pages)
        uri = flask.url_for(
            'api_findings.findings',
            documentid=documentid,
            pages=pages,
        )
        pagerange = pages
    return pagerange, uri
