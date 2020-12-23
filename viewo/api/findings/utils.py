# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import enum
import os
import typing

import flask
import iamraw
import link
import protocol.finding
import utila

import viewo.api.pageviews.utils
import viewo.api.utils
import viewo.result.json
import viewo.result.update

ComparedFinding = collections.namedtuple(
    'ComparedFinding',
    'page, current, other',
)
ComparedListFinding = typing.List[ComparedFinding]


class Comperator(enum.Enum):
    ALL = enum.auto()
    EQUAL = enum.auto()
    DIFF = enum.auto()


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


def compare(
        documentid: str,
        partnerid: str,
        operation: Comperator = Comperator.ALL,
) -> ComparedListFinding:
    documentpath = link.document(documentid)
    if documentpath is None:
        return None
    partnerpath = link.document(partnerid)
    if partnerpath is None:
        return None
    if documentid == partnerid:
        # equal documents
        return []
    document = protocol.findings_from_path(documentpath)
    partner = protocol.findings_from_path(partnerpath)
    compared = []
    for number, content in utila.sync_pages((document, partner)):
        left = content[0] if content[0] else []
        right = content[1] if content[1] else []
        # run selected filter
        if operation == Comperator.EQUAL:
            left = [finding for finding in left if finding in right]
        elif operation == Comperator.DIFF:
            left_ = [finding for finding in left if finding not in right]
            right = [finding for finding in right if finding not in left]
            left = left_
        current = ComparedFinding(number, left, right)
        compared.append(current)
    return compared


def compare_raw(pages: ComparedListFinding):
    result = []
    for page in pages:
        raw = {
            'page': page.page,
            'current': viewo.api.utils.simple_recursive(page.current),
            'other': viewo.api.utils.simple_recursive(page.other),
        }
        result.append(raw)
    return result


def convert_style_markup(findings: iamraw.PageFinding) -> iamraw.PageFinding:
    for finding in findings.content:
        finding.solution.description = viewo.result.json.message_replace(
            finding.solution.description)
    return findings
